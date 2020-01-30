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

from urllib.parse import urljoin


init_logging()

_LOGGER = logging.getLogger("aicoe.sesheta")
_LOGGER.info(f"Qeb-Hwt GitHub App, v{qeb_hwt_version}")
logging.getLogger("octomachinery").setLevel(logging.DEBUG)

CHECK_RUN_NAME = "Thoth: Advise (Developer Preview)"

ADVISE_API_URL = os.getenv("ADVISE_API_URL", "https://khemenu.thoth-station.ninja/api/v1/advise/python/",)

USER_API_URL = os.getenv("USER_API_URL", "https://khemenu.thoth-station.ninja/api/v1/qeb-hwt/",)


@process_event("ping")
@process_webhook_payload
async def on_ping(*, hook, hook_id, zen):
    """React to ping webhook event."""
    app_id = hook["app_id"]

    _LOGGER.info(
        "Processing hwtping for App ID %s " "with Hook ID %s " "sharing Zen: %s", app_id, hook_id, zen,
    )

    _LOGGER.info(
        "GitHub App from context in ping handler: %s", RUNTIME_CONTEXT.github_app,
    )


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
    _LOGGER.info(f"on_pr_open_or_sync: working on PR {pull_request['html_url']}",)

    github_api = RUNTIME_CONTEXT.app_installation_client

    pr_head_sha = pull_request["head"]["sha"]
    repo_url = pull_request["head"]["repo"]["html_url"]
    check_runs_base_uri = f"{repo_url}/check-runs"

    if pr_head_sha is None:
        _LOGGER.error(f"on_pr_open_or_sync: no Pull Request head sha found, stopped working!")
        return

    _LOGGER.info(f"on_pr_open_or_sync: PR commit id {pr_head_sha} will be used for check-run")

    resp = await github_api.post(
        check_runs_base_uri,
        preview_api_version="antiope",
        data={
            "name": CHECK_RUN_NAME,
            "head_shhwta": pr_head_sha,
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
        "github_installation_id": installation,
        "origin": repo_url,
        "revision": pr_head_sha,
    }
    async with aiohttp.ClientSession() as session:
        session.post(USER_API_URL, json=json.dumps(data))

    resp = await github_api.patch(
        check_runs_updates_uri, preview_api_version="antiope", data={"name": CHECK_RUN_NAME, "status": "in_progress"},
    )


# We simply extend the GitHub Event set for our use case ;)
@process_event("thoth_thamos_advise", action="finished")
@process_webhook_payload
async def on_thamos_workflow_finished(*, action, repo_url, check_run_id, installation, payload, **kwargs):
    """Advise workflow has finished, now we need to send a check-run to the PR."""
    _LOGGER.info("on_thamos_workflow_finished: %s", kwargs)

    github_api: RawGitHubAPI = RUNTIME_CONTEXT.app_installation_client

    repo = repo_url.split("/", 3)[-1]  # i.e.: thoth-station/Qeb-Hwt
    check_runs_url = f"repos/{repo}/check-runs/{check_run_id}"

    conclusion: str
    justification: str

    report: str = "No report has been provided."

    async with aiohttp.ClientSession() as session:
        analysis_id: str = payload["analysis_id"]

        advise_url = urljoin(ADVISE_API_URL, analysis_id)

        async with session.get(advise_url) as response:
            if response.status != 200:
                conclusion = "failure"
                justification = "Could not retrieve analysis results."
            else:
                adviser_payload: dict = await response.json()

                adviser_result: dict = adviser_payload["result"]
                if adviser_result["error"]:
                    conclusion = "failure"

                    error_msg: str = adviser_result["error_msg"]
                    justification = f"Analysis has encountered errors."
                else:
                    conclusion = "success"

                    check_run: dict = await github_api.getitem(
                        check_runs_url, preview_api_version="antiope",
                    )
                    pull_number: int = check_run["pull_requests"][0]["number"]
                    pull_url: str = f"https://github.com/{repo}/pull/{pull_number}"

                    adviser_report: dict = adviser_result["report"]
                    justification = f'Analysis of <a href="{pull_url}">#{pull_number}</a> ' "finished successfully.\n\n"

                    report = json.dumps(adviser_report, indent=2)
                    # a hack to display indentation spaces in the resulting HTML
                    report = re.sub("\n {2,}", lambda m: "\n" + "&ensp;" * (len(m.group().strip("\n"))), report,)

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
                "text": f"Analysis report:\n{report}",
                "summary": (
                    f"Thoth's adviser finished with conclusion: '{conclusion}'\n\n"
                    f"Justification:\n{justification}\n\n"
                    "See the report below for more details."
                ),
            },
        },
    )

    _LOGGER.info(
        f"on_thamos_workflow_finished: finished with `thamos advise`, updated %s", check_run_id,
    )


if __name__ == "__main__":
    _LOGGER.setLevel(logging.DEBUG)
    _LOGGER.debug("Debug mode turned on")

    run_app(  # pylint: disable=expression-not-assigned
        name="Qeb-Hwt GitHub App", version=qeb_hwt_version, url="https://github.com/apps/qeb-hwt",
    )
