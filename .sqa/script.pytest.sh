#!/usr/bin/env bash
for plugin in qc_*
do
    pip install -r $plugin/requirements.txt
    pip install $plugin/
    pip install -r $plugin/test-requirements.txt
    pytest -svv $plugin
done
