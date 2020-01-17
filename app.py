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
import asyncio
import pathlib
import logging
import random
import time

from datetime import datetime

import gidgethub

from octomachinery.app.server.runner import run as run_app
from octomachinery.app.routing import process_event_actions, process_event
from octomachinery.app.routing.decorators import process_webhook_payload
from octomachinery.app.runtime.context import RUNTIME_CONTEXT
from octomachinery.github.config.app import GitHubAppIntegrationConfig
from octomachinery.github.api.app_client import GitHubApp
from octomachinery.utils.versiontools import get_version_from_scm_tag

from thoth.common import init_logging

from thoth.qeb_hwt.version import __version__ as qeb_hwt_version


init_logging()

_LOGGER = logging.getLogger("aicoe.sesheta")
_LOGGER.info(f"Qeb-Hwt GitHub App, v{qeb_hwt_version}")
logging.getLogger("octomachinery").setLevel(logging.DEBUG)

CHECK_RUN_NAME = "Thoth: Advise (Developer Preview)"


@process_event("ping")
@process_webhook_payload
async def on_ping(*, hook, hook_id, zen):
    """React to ping webhook event."""
    app_id = hook["app_id"]

    _LOGGER.info("Processing ping for App ID %s " "with Hook ID %s " "sharing Zen: %s", app_id, hook_id, zen)

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

    pr_head_sha = pull_request["merge_commit_sha"]
    if pr_head_sha is None:
        pr_head_sha = pull_request["head"]["sha"]

    repo_url = pull_request["base"]["repo"]["url"]

    check_runs_base_uri = f"{repo_url}/check-runs"

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

    check_runs_updates_uri = f'{check_runs_base_uri}/{resp["id"]:d}'

    resp = await github_api.patch(
        check_runs_updates_uri, preview_api_version="antiope", data={"name": CHECK_RUN_NAME, "status": "in_progress"},
    )

    _LOGGER.info(
        f"on_pr_open_or_sync: working on PR %s: sleeping a random time between 5 and 15 seconds...",
        pull_request["html_url"],
    )

    timeDelay = random.randrange(5, 15)
    time.sleep(timeDelay)


# We simply extend the GitHub Event set for our use case ;)
@process_event("thoth_thamos_advise", action="finished")
@process_webhook_payload
async def on_thamos_workflow_finished(*, action, repo_url, check_run_id, installation, adviser_result, **kwargs):
    """Advise workflow has finished, now we need to send a check-run to the PR."""
    _LOGGER.info("on_thamos_workflow_finished: %s", kwargs)

    github_api = RUNTIME_CONTEXT.app_installation_client

    # TODO: get the check-run id
    check_runs_updates_uri = f"{repo_url}/check-runs/{check_run_id}"

    # TODO: get advise result and patch the check-run
    await github_api.patch(
        check_runs_updates_uri,
        preview_api_version="antiope",
        data={
            "name": CHECK_RUN_NAME,
            "status": "completed",
            "conclusion": "neutral",
            "completed_at": f"{datetime.utcnow().isoformat()}Z",
            "output": {
                "title": "Thoth's Advise",
                "text": "This text goes into the details section of the Check.\n\n"
                f"Ut quis occaecat commodo incididunt aliquip aliquip occaecat sit anim irure.",
                "summary": "This is a Developer Preview Service.\n\n"
                f"Id exercitation cillum ex labore. Culpa culpa minim aute ad nulla nostrud elit"
                f"amet. Ea velit commodo magna incididunt sint eiusmod excepteur quis. Commodo est culpa"
                f"culpa do commodo. Lorem minim consequat exercitation culpa sint mollit minim veniam"
                f"id Lorem fugiat tempor duis.",
            },
        },
    )

    _LOGGER.info(
        f"on_thamos_workflow_finished: finished with `thamos advise`, updated %s", check_runs_updates_uri,
    )


if __name__ == "__main__":
    _LOGGER.setLevel(logging.DEBUG)
    _LOGGER.debug("Debug mode turned on")

    run_app(  # pylint: disable=expression-not-assigned
        name="Qeb-Hwt GitHub App", version=qeb_hwt_version, url="https://github.com/apps/qeb-hwt",
    )
