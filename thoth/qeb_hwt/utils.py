#!/usr/bin/env python3
# Qeb-Hwt GitHub App webhook receiver
# Copyright(C) 2020 Francesco Murdaca
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

"""This files contains methods for Qeb-Hwt GitHub App."""

import json
import pandas as pd
from typing import Optional


def create_pretty_report_from_json(report: dict, is_justification: bool = False) -> Optional[str]:
    """Create Markdown output from adviser report input."""
    if not report:
        return

    products = report.get("products")
    if not products:
        return

    md = "Report"

    md += "\n\n" + "Justifications"

    final_df = pd.DataFrame(columns=["message", "type"])

    counter = 0
    for product in products:
        if "justification" in product.keys():
            justifications = product["justification"]
            if justifications:
                for justification in justifications:
                    final_df.loc[counter] = pd.DataFrame([justification]).iloc[0]
                    counter += 1

    md += "\n\n" + final_df.to_markdown()

    if is_justification:
        return md

    md += "\n\n" + "Packages in Advised Pipfile"

    packages_names = []
    packages_versions = []

    for package_name, requested_version in report["products"][0]['project']["requirements"]["packages"].items():
        packages_names.append(package_name)
        packages_versions.append(requested_version)

    data = {
        "package_name": packages_names,
        "pakage_version": packages_versions,
    }

    df = pd.DataFrame(data)
    md += "\n\n" + df.to_markdown()

    md += "\n\n" + "Dev-Packages in Advised Pipfile"

    packages_names = []
    packages_versions = []

    for package_name, requested_version in report["products"][0]['project']["requirements"]["dev-packages"].items():
        packages_names.append(package_name)
        packages_versions.append(requested_version)

    data = {
        "package_name": packages_names,
        "package_version": packages_versions,
    }

    df = pd.DataFrame(data)
    md += "\n\n" + df.to_markdown()

    md += "\n\n" + "Requires in Advised Pipfile"
    df = pd.DataFrame([report["products"][0]['project']['requirements']['requires']])
    md += "\n\n" + df.to_markdown()

    md += "\n\n" + "Source in Advised Pipfile"
    df = pd.DataFrame(report["products"][0]['project']['requirements']['source'])
    md += "\n\n" + df.to_markdown()

    md += "\n\n" + "Packages in Advised Pipfile.lock"
    packages_names = []
    packages_versions = []
    packages_indexes = []

    for package_name, data in report["products"][0]['project']["requirements_locked"]["default"].items():
        packages_names.append(package_name)
        packages_versions.append(data["version"])
        packages_indexes.append(data["index"])

    data = {
        "package_name": packages_names,
        "package_version": packages_versions,
        "index": packages_indexes,
    }
    df = pd.DataFrame(data)
    md += "\n\n" + df.to_markdown()

    md += "\n\n" + "Dev-Packages in Advised Pipfile.lock"
    packages_names = []
    packages_versions = []
    packages_indexes = []

    for package_name, data in report["products"][0]['project']["requirements_locked"]["develop"].items():
        packages_names.append(package_name)
        packages_versions.append(data["version"])
        packages_indexes.append(data["index"])

    data = {
        "package_name": packages_names,
        "package_version": packages_versions,
        "index": packages_indexes,
    }
    df = pd.DataFrame(data)
    md += "\n\n" + df.to_markdown()

    md += "\n\n" + "Runtime Environment"

    md += "\n\n" + "Runtime Environment - Name"
    df = pd.DataFrame([{"name": report["products"][0]['project']['runtime_environment']['name']}])
    md += "\n\n" + df.to_markdown()

    md += "\n\n" + "Runtime Environment - CUDA"
    df = pd.DataFrame([{"cuda_version": report["products"][0]['project']['runtime_environment']['cuda_version']}])
    md += "\n\n" + df.to_markdown()

    md += "\n\n" + "Runtime Environment - Hardware"
    df = pd.DataFrame([report["products"][0]['project']['runtime_environment']['hardware']])
    md += "\n\n" + df.to_markdown()

    md += "\n\n" + "Software Stack Score"
    df = pd.DataFrame([{"score": report["products"][0]['score']}])
    md += "\n\n" + df.to_markdown()

    return md
