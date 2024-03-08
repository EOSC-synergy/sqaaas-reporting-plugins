#!/usr/bin/env bash

# SPDX-FileCopyrightText: Copyright contributors to the Software Quality Assurance as a Service (SQAaaS) project <sqaaas@ibergrid.eu>
# SPDX-FileContributor: 2017-2024 Pablo Orviz <orviz@ifca.unican.es>
#
# SPDX-License-Identifier: GPL-3.0-only

for plugin in qc_*
do
    pip install -r $plugin/requirements.txt
    pip install $plugin/
    pip install -r $plugin/test-requirements.txt
    pytest -svv $plugin
done
