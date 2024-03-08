# SPDX-FileCopyrightText: Copyright contributors to the Software Quality Assurance as a Service (SQAaaS) project <sqaaas@ibergrid.eu>
# SPDX-FileContributor: 2017-2024 Pablo Orviz <orviz@ifca.unican.es>
#
# SPDX-License-Identifier: GPL-3.0-only

import os
from urllib.parse import urlparse

from setuptools import find_packages, setup


def load_requirements():
    """Install dependencies from 'requirements.txt'.

    If the file contains a pip-supported git+https' location for the
    package, this method transforms it to setuptools' way. Some code has
    been taken from
    https://stackoverflow.com/a/53069528
    """
    thelibFolder = os.path.dirname(os.path.realpath(__file__))
    requirementPath = thelibFolder + "/requirements.txt"
    install_requires = []
    if os.path.isfile(requirementPath):
        with open(requirementPath) as f:
            install_requires = f.read().splitlines()
    install_requires_filtered = []
    for req in install_requires:
        if not req.startswith("#"):
            url_parsed = urlparse(req)
            fragment = url_parsed.fragment
            if fragment:
                fragment = fragment.split("=")[-1]
                req = "@".join([fragment, req])
            install_requires_filtered.append(req)

    return install_requires_filtered


setup(
    name="report2sqaaas-plugin-is_semver",
    version="2.0.0",
    description="Output validator for the is_semver.py tool",
    author="Pablo Orviz",
    author_email="orviz@ifca.unican.es",
    url="https://github.com/eosc-synergy/sqaaas-reporting-plugins",
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[
        "Intended Audience :: Developers",
        (
            "License :: OSI Approved :: GNU General Public License v3 or later "
            "(GPLv3+)"
        ),
        "Environment :: Plugins",
        "Development Status :: 3 - Alpha",
    ],
    install_requires=load_requirements(),
    packages=find_packages(),
    entry_points={
        "sqaaas.validators": [
            "is_semver = report2sqaaas_plugins_is_semver.main:IsSemverValidator",  # noqa
        ],
    },
)
