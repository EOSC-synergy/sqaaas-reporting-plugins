# Reporting plugins (aka validators) for the SQAaaS platform

This repository hosts the official set of plugins used to validate the output
of the tools used by the SQAaaS solution in order to assess the quality of
software, services and their data.

## Developer guidelines
As described in
[Implement the validate() method](https://github.com/eosc-synergy/sqaaas-reporting-cookiecutter#implement-the-validate-method),
the `validate()` method is the pivotal part of the plugin, containing the
business logic that parses and assesses the validity of the tool's output.

### What shall the validate() method return?
The object (dict) returned by the `validate()` method must have:
- `valid` (type: boolean): sets the criterion validation as successful(`True`)
  or unsuccessful (`False`)
- `subcriteria` (type: list): contains a list of objects with the results of
  the validation for a given subcriterion. The expected properties of those
  objects are:
  - `id` (type: str): identifier of the subcriterion (e.g. `QC.Sty01`,
    `QC.Doc06.1`)
  - `valid` (type: boolean): whether the subcriterion has passed the validation
    (`True`) or not (`False`)
  - `description` (type: str): short statement about the subcriterion purpuse
    (e.g. *"Is LICENSE file placed in the root path of the code repository?"*)
  - `evidence` (type: str): short statement about the findings (e.g. *LICENSE
    file is visible at the root path of the code repository* )
- `standard` (type: dict): object with the pointers to the standard where the
   criteria belongs to. Expected properties:
  - `title` (type: str): the standard title (e.g. *"A set of Common Software
    Quality Assurance Baseline Criteria for Research Projects"*)
  - `version` (type: str): the standard version (e.g. *"v4.0"*)
  - `url` (type: str): URL with the standard location (e.g.
    *"https://github.com/indigo-dc/sqa-baseline/releases/tag/v4.0"*)
- `data_unstructured` (type: dict): object with additional data that will be
  shown as it is by the SQAaaS API


## How to contribute

Follow the [contribution guidelines](CONTRIBUTING.md) in order to add a new
plugin to the list of supported ones. A peer review of the new contributions
is particularly important to ensure the accuracy of the implementation and
avoid false positives.
