<!--
SPDX-FileCopyrightText: Copyright contributors to the Software Quality Assurance as a Service (SQAaaS) project <sqaaas@ibergrid.eu>
SPDX-FileContributor: 2017-2024 Pablo Orviz <orviz@ifca.unican.es>

SPDX-License-Identifier: GPL-3.0-only
-->

# SQAaaS reporting validator plugin for the cffconvert tool

[![License](https://img.shields.io/github/license/fzhu2e/GraphEM)](https://opensource.org/licenses/GPL-3.0)

* [Description](#description)
* [Quick start](#quick-start)
* [Developing and Testing](#development-and-testing)
* [Contribution](#contribution)
* [License](#license)


## Description
This plugin validates the output of the [cffconvert](https://github.com/citation-file-format/cff-converter-python) tool."

## Quick start
The plugin can be installed from this repository using `pip`:
```
$ pip install git+https://github.com/EOSC-synergy/sqaaas-reporting-plugins@main#egg=report2sqaaas-plugin-cff&subdirectory=qc_met_cff
```
### Configuration
No additional configuration is needed. The plugin is added to the
`sqaaas.validators` namespace, which is scoped by the
[report2sqaaas](https://github.com/eosc-synergy/sqaaas-reporting) application.
### Trying it out
The plugin can be readily used through the CLI offered by the
[report2sqaaas](https://github.com/eosc-synergy/sqaaas-reporting) module:
```
$ report2sqaaas cff cffconvert.stdout
```

Note that you will need to have the
[report2sqaaas](https://github.com/eosc-synergy/sqaaas-reporting) module
deployed in your environment for the plugin to work. To this end, you can
use the [requirements.txt](requirements.txt) file included with this package:
```
$ pip install -r requirements.txt
```

## Development and Testing
While on development, deploy the plugin in editable mode:
```
pip install -r requirements.txt
pip install -e .
```

Use [pytest](https://pytest.org/) module to run the test cases:
```
$ pip install -r test-requirements.txt
$ pytest -svv
```
### About validate() method
The `validate()` method has to be implemented for the tests to pass successfully.
If pytest returns the exception:
```TypeError: Can't instantiate abstract class FooValidator with abstract method validate```
then this means that the method is not implemented in the generated validator class.


## Contribution
Please check our [guidelines](CONTRIBUTING.md) on how to contribute.

## License
[GNU GENERAL PUBLIC LICENSE v3](LICENSE)
