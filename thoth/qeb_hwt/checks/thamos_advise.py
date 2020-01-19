"""Thamos Advise check run."""

import os

from argo.workflows import models

from argo.workflows.sdk import Workflow
from argo.workflows.sdk.tasks import *
from argo.workflows.sdk.templates import *

REPOSITORY_ARTIFACT = "/mnt/inputs/artifacts/repository"
"""A Path to repository artifact."""

# TODO: Remove the default url used for debugging purposes
WEBHOOK_RECEIVER_URL = os.getenv("WEBHOOK_RECEIVER_URL", "http://macermak.aicoe.ultrahook.com/kebechet/")
"""Webhook receiver endpoint URL."""


class ThamosAdviseCheckRun(Workflow):
    """Thamos Advise check run Workflow."""

    arguments = V1alpha1Arguments(
        parameters=[
            V1alpha1Parameter(name="event", default="thoth_thamos_advise"),
            V1alpha1Parameter(name="check_run_id"),
            V1alpha1Parameter(name="installation"),
            V1alpha1Parameter(name="repo_url"),
            V1alpha1Parameter(name="revision", default="master"),
            V1alpha1Parameter(name="finished_webhook", default=WEBHOOK_RECEIVER_URL),
        ]
    )

    service_account_name = "argo"

    volumes = [models.V1Volume(name="cache", empty_dir={})]

    @property
    def id(self) -> str:
        """Get Workflow ID."""
        prefix: str = self.name or getattr(self.metadata, "generate_name")
        digest: str = str(abs(self.__hash__()))
        return f"{prefix}-{digest}"

    @task
    def thamos_advise(self) -> V1alpha1Template:
        return self.thamos_advise_template()

    @closure(
        # TODO: use thoth-station thamos image
        image="quay.io/cermakm/thamos:latest",
        resources=models.V1ResourceRequirements(limits={"memory": "128Mi", "cpu": "100m"},),
        volume_mounts=[models.V1VolumeMount(name="cache", mount_path="/mnt/outputs/parameters")],
    )
    @inputs.artifact(
        git=models.V1alpha1GitArtifact(
            repo="{{workflow.parameters.repo_url}}", revision="{{workflow.parameters.revision}}"
        ),
        name="repository",
        path=REPOSITORY_ARTIFACT,
    )
    @outputs.parameter(name="payload", global_name="payload", value_from={"path": "/mnt/outputs/parameters/payload"})
    def thamos_advise_template():
        import logging

        import json
        import os
        import subprocess

        from pathlib import Path

        logging.getLogger("thamos").setLevel("DEBUG")

        os.chdir("{{inputs.artifacts.repository.path}}")

        subprocess.call(["thamos", "config", "-I"])
        subprocess.call(["thamos", "advise", "--no-write"])

        analysis_id: str = Path(".thoth_last_analysis_id").read_text()

        payload: str = json.dumps({"analysis_id": analysis_id})

        Path("/mnt/outputs/parameters/payload").write_text(payload)

    @task
    @dependencies(["thamos-advise"])
    def trigger_finished_webhook(self) -> V1alpha1Template:
        return self.trigger_finished_webhook_template()

    @closure(
        scope="webhook",
        image="quay.io/cermakm/octomachinery:latest",
        resources=models.V1ResourceRequirements(limits={"memory": "128Mi", "cpu": "100m"},),
        env=[
            models.V1EnvVar(
                name="WEBHOOK_SECRET",
                value_from=models.V1EnvVarSource(
                    secret_key_ref={"name": "qeb-hwt-github-app", "key": "WEBHOOK_SECRET"}
                ),
            ),
        ],
    )
    def trigger_finished_webhook_template():
        import os
        import requests
        import uuid

        uuid = str(uuid.uuid4())

        data: dict = {
            "event": "{{workflow.parameters.event}}",
            "check_run_id": "{{workflow.parameters.check_run_id}}",
            "installation": {"id": int("{{workflow.parameters.installation}}")},
            "repo_url": "{{workflow.parameters.repo_url}}",
            "revision": "{{workflow.parameters.revision}}",
            "payload": json.loads("{{workflow.outputs.parameters.payload}}"),
        }

        signature: str = webhook.get_signature(data, key=os.environ["WEBHOOK_SECRET"])

        headers = {
            "Accept": "application/vnd.github.antiope-preview+json",
            "Content-Type": "application/json",
            "User-Agent": "Workflow/{{workflow.name}}",
            "X-GitHub-Delivery": uuid,
            "X-GitHub-Event": "{{workflow.parameters.event}}",
            "X-Hub-Signature": f"sha1={signature}",
        }

        print("Headers:\n", headers)
        print("Payload:\n", data)

        response = requests.post("{{workflow.parameters.finished_webhook}}", json=data, headers=headers)
        response.raise_for_status()

    @scope("webhook")
    def get_signature(data: bytes, key: str) -> str:
        import hmac
        import json

        if not isinstance(data, bytes):
            data = json.dumps(data).encode("UTF-8")

        secret = key.encode("UTF-8")
        signature = hmac.new(secret, data, digestmod="sha1")

        return signature.hexdigest()
