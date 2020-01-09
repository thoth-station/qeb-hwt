#!/usr/bin/env python3
# Qeb-Hwt
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

"""This is Qeb-Hwt."""

import os
import asyncio
import pathlib
import logging

import gidgethub

from octomachinery.app.server.runner import run as run_app
from octomachinery.app.routing import process_event_actions, process_event
from octomachinery.app.routing.decorators import process_webhook_payload
from octomachinery.app.runtime.context import RUNTIME_CONTEXT
from octomachinery.github.config.app import GitHubAppIntegrationConfig
from octomachinery.github.api.app_client import GitHubApp
from octomachinery.utils.versiontools import get_version_from_scm_tag

from thoth.common import init_logging

from thoth.qeb_hwt.version import __version__


init_logging()

_LOGGER = logging.getLogger("aicoe.sesheta")
_LOGGER.info(f"Qeb-Hwt GitHub App, v{__version__}")
logging.getLogger("octomachinery").setLevel(logging.DEBUG)


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


# We simply extend the GitHub Event set for our use case ;)
@process_event("thoth_thamos_advise", action="finished")
@process_webhook_payload
async def on_thamos_workflow_finished(*, action, analysis_id, repo_url, fetch_ref_spec, installation, **kwargs):
    """Advise workflow has finished, now we need to send a check-run to the PR."""
    _LOGGER.info("on_thamos_workflow_finished: %s", kwargs)


if __name__ == "__main__":
    _LOGGER.setLevel(logging.DEBUG)
    _LOGGER.debug("Debug mode turned on")

    run_app(  # pylint: disable=expression-not-assigned
        name="Qeb-Hwt GitHub App",
        version=get_version_from_scm_tag(root="./", relative_to=__file__),
        url="https://github.com/apps/qeb-hwt",
    )
