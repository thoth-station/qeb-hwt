#!/usr/bin/env python3
# Qeb-Hwt GitHub App webhook receiver
# Copyright(C) 2019, 2020 Red Hat, Inc.
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""This is Qeb-Hwt GitHub App webhook receiver."""

import os

import json
import logging
import pathlib
import random
import re
import time

import aiohttp
import asyncio

import gidgethub

from datetime import datetime
from urllib.parse import urljoin

from octomachinery.app.server.runner import run as run_app
from octomachinery.app.routing import process_event_actions, process_event
from octomachinery.app.routing.decorators import process_webhook_payload
from octomachinery.app.runtime.context import RUNTIME_CONTEXT
from octomachinery.github.config.app import GitHubAppIntegrationConfig
from octomachinery.github.api.app_client import GitHubApp
from octomachinery.github.api.raw_client import RawGitHubAPI
from octomachinery.utils.versiontools import get_version_from_scm_tag

from thoth.common import init_logging
from thoth.common import WorkflowManager

from thoth.qeb_hwt.version import __version__ as qeb_hwt_version


init_logging()


_LOGGER = logging.getLogger("aicoe.sesheta")
_LOGGER.info(f"Qeb-Hwt GitHub App, v{qeb_hwt_version}")
logging.getLogger("octomachinery").setLevel(logging.DEBUG)

CHECK_RUN_NAME = "Thoth: Advise (Developer Preview)"

# no trailing / !
ADVISE_API_URL = os.getenv("ADVISE_API_URL", "https://khemenu.thoth-station.ninja/api/v1/advise/python/adviser_id")
USER_API_URL = os.getenv("USER_API_URL", "https://khemenu.thoth-station.ninja/api/v1/qeb-hwt")

MAX_CHARACTERS_LENGTH = 65535

tracer = None


@process_event("ping")
@process_webhook_payload
async def on_ping(*, hook, hook_id, zen):
    """React to ping webhook event."""
    app_id = hook["app_id"]

    _LOGGER.info("Processing hwtping for App ID %s " "with Hook ID %s " "sharing Zen: %s", app_id, hook_id, zen)

    _LOGGER.info("GitHub App from context in ping handler: %s", RUNTIME_CONTEXT.github_app)


@process_event("integration_installation", action="created")
@process_webhook_payload
async def on_install(
    action,  # pylint: disable=unused-argument
    installation,
    sender,  # pylint: disable=unused-argument
    repositories=None,  # pylint: disable=unused-argument
):
    """React to GitHub App integration installation webhook event."""
    _LOGGER.info("installed event install id %s", installation["id"])
    _LOGGER.info("installation=%s", RUNTIME_CONTEXT.app_installation)


@process_event_actions("pull_request", {"opened", "reopened", "synchronize", "edited"})
@process_webhook_payload
async def on_pr_open_or_sync(*, action, number, pull_request, repository, sender, installation, **kwargs):
    """React to an opened or changed PR event.

    Send a status update to GitHub via Checks API.
    """
    _LOGGER.info(f"on_pr_open_or_sync: working on PR {pull_request['html_url']}")

    github_api = RUNTIME_CONTEXT.app_installation_client

    pr_head_sha = pull_request["head"]["sha"]
    base_repo_url = pull_request["base"]["repo"]["url"]
    repo_url = pull_request["head"]["repo"]["html_url"]
    check_runs_base_uri = f"{base_repo_url}/check-runs"

    if pr_head_sha is None:
        _LOGGER.error(f"on_pr_open_or_sync: no Pull Request head sha found, stopped working!")
        return

    _LOGGER.info(f"on_pr_open_or_sync: base_repo_url {base_repo_url} will be used for check-run")
    _LOGGER.info(f"on_pr_open_or_sync: PR commit id {pr_head_sha} will be used for check-run")

    resp = await github_api.post(
        check_runs_base_uri,
        preview_api_version="antiope",
        data={
            "name": CHECK_RUN_NAME,
            "head_sha": pr_head_sha,
            "status": "queued",
            "started_at": f"{datetime.utcnow().isoformat()}Z",
        },
    )

    check_run_id = int(resp["id"])  # TODO do we need some marshaling here?

    check_runs_updates_uri = f"{check_runs_base_uri}/{check_run_id}"
    _LOGGER.info(f"on_pr_open_or_sync: check_run_id: {check_run_id}")

    data = {
        "github_event_type": "thoth_thamos_advise",
        "github_check_run_id": check_run_id,
        "github_installation_id": installation["id"],
        "github_base_repo_url": base_repo_url,
        "github_head_repo_url": repo_url,
        "origin": repo_url,
        "revision": pr_head_sha,
    }
    async with aiohttp.ClientSession() as session:
        resp = await session.post(USER_API_URL, json=data)
        _LOGGER.info(f"on_pr_open_or_sync: user-api resp: {resp}")

    # TODO: add timeout to keep the github check status sane
    resp = await github_api.patch(
        check_runs_updates_uri,
        preview_api_version="antiope",
        data={"name": CHECK_RUN_NAME, "head_sha": pr_head_sha, "status": "in_progress"},
    )


# We simply extend the GitHub Event set for our use case ;)
@process_event("thoth_thamos_advise", action="finished")
@process_webhook_payload
async def on_thamos_workflow_finished(*, action, base_repo_url, check_run_id, installation, payload, **kwargs):
    """Advise workflow has finished, now we need to send a check-run to the PR."""
    _LOGGER.info("on_thamos_workflow_finished: %s", kwargs)

    github_api: RawGitHubAPI = RUNTIME_CONTEXT.app_installation_client
    _LOGGER.info("on_thamos_workflow_finished: github_api=%s", github_api)

    repo = base_repo_url.split("/", 4)[-1]  # i.e.: thoth-station/Qeb-Hwt
    check_runs_url = f"https://api.github.com/repos/{repo}/check-runs/{check_run_id}"
    _LOGGER.info("on_thamos_workflow_finished: check_runs_url=%s", check_runs_url)

    conclusion: str
    justification: str
    report: str
    text: str
    report_message: str

    async with aiohttp.ClientSession() as session:
        analysis_id: str = payload["analysis_id"]
        _LOGGER.info("on_thamos_workflow_finished: analysis_id=%s", analysis_id)

        advise_url = urljoin(ADVISE_API_URL, analysis_id)
        _LOGGER.info("on_thamos_workflow_finished: advise_url=%s", advise_url)

        if "exception" in payload:
            exception: str = payload["exception"]
            _LOGGER.info("on_thamos_workflow_finished: exception=%s", exception)
            conclusion = "failure"
            justification = exception
            report = "Report not produced."
            text = report
            report_message = ""

        if analysis_id:

            # TODO: Find alternative solution to this workround
            attempts = 1
            max_attempts = 6
            while attempts < max_attempts:
                try:
                    async with session.get(advise_url) as response:
                        _LOGGER.info("on_thamos_workflow_finished: response=%s", response)
                        _LOGGER.info("on_thamos_workflow_finished: attempts=%s", attempts)
                    if response.status == 200:
                        attempts = max_attempts
                    else:
                        attempts += 1
                except Exception:
                    continue

            async with session.get(advise_url) as response:
                if response.status != 200:
                    conclusion = "failure"
                    justification = "Could not retrieve analysis results."
                    report = ""
                    text = "Report cannot be provided, Please open an issue on Qeb-Hwt."
                    report_message = ""
                else:
                    adviser_payload: dict = await response.json()

                    adviser_result: dict = adviser_payload["result"]
                    if adviser_result["error"]:
                        conclusion = "failure"

                        error_msg: str = adviser_result["error_msg"]
                        justification = f"Analysis has encountered errors: {error_msg}."
                        if adviser_result["report"]:
                            report = adviser_result["report"]
                            text = "See the report below for more details."
                            report_message = "See the document below for more details."
                        else:
                            text = "Analysis report is missing."
                            report_message = "See the document below for more details."

                    else:
                        conclusion = "success"

                        adviser_report: dict = adviser_result["report"]

                        justification = adviser_report["products"][0]["justification"]
                        justification = json.dumps(justification, indent=2)

                        user_report = adviser_report["products"][0]
                        user_report.pop("justification", None)
                        if adviser_report["stack_info"]:
                            user_report["stack_info"] = adviser_report["stack_info"]

                        # Complete report
                        report = json.dumps(user_report, indent=2)
                        _LOGGER.info("on_thamos_workflow_finished: len(report)=%s", len(report))

                        # TODO: Split report results to include only relevant information
                        if len(report) > MAX_CHARACTERS_LENGTH:
                            user_report.pop("project", None)
                            # Reduced report
                            report = json.dumps(user_report, indent=2)
                            _LOGGER.info("on_thamos_workflow_finished: reduced len(report)=%s", len(report))

                        text = f"Analysis report:\n{report}"
                        report_message = "See the document below for more details."

    try:
        _LOGGER.info("on_thamos_workflow_finished: installation_id=%s, check_run_url=%s", installation, check_runs_url)

        await github_api.patch(
            check_runs_url,
            preview_api_version="antiope",
            data={
                "name": CHECK_RUN_NAME,
                "status": "completed",
                "conclusion": conclusion,
                "completed_at": f"{datetime.utcnow().isoformat()}Z",
                "details_url": advise_url,
                "external_id": analysis_id,
                "output": {
                    "title": "Thoth's Advise",
                    "text": text,
                    "summary": (
                        f"Thoth's adviser finished with conclusion: '{conclusion}'\n\n"
                        f"Justification:\n{justification}\n\n"
                        f"{report_message}"
                    ),
                },
            },
        )
    except gidgethub.BadRequest as exc:
        _LOGGER.error(exc)

    _LOGGER.info(f"on_thamos_workflow_finished: finished with `thamos advise`, updated %s", check_run_id)


if __name__ == "__main__":
    _LOGGER.setLevel(logging.DEBUG)
    _LOGGER.debug("Debug mode turned on")

    run_app(  # pylint: disable=expression-not-assigned
        name="Qeb-Hwt GitHub App", version=qeb_hwt_version, url="https://github.com/apps/qeb-hwt"
    )
