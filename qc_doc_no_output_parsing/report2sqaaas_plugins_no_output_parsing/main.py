import logging

from report2sqaaas import utils as sqaaas_utils


logger = logging.getLogger('sqaaas.reporting.plugins.no_output_parsing')


class NoOutputParsingValidator(sqaaas_utils.BaseValidator):
    valid = True
    stdin = None
    standard = {
        'title': (
            'A set of Common Software Quality Assurance Baseline Criteria for '
            'Research Projects'
        ),
        'version': 'v4.0',
        'url': 'https://github.com/indigo-dc/sqa-baseline/releases/tag/v4.0',
    }

    def set_valid(self, subcriterion_data, subcriterion_valid):
        requirement_level = subcriterion_data['requirement_level']
        if (
            (not subcriterion_valid) and
            (requirement_level in ['MUST'])
        ):
            self.valid = False

    def validate_qc_doc01(self, criterion_data):
        # QC.Doc01.1
        subcriterion = 'QC.Doc01.1'
        subcriterion_data = criterion_data[subcriterion]
        subcriterion_valid = False
        evidence = None
        has_doc_repo = self.stdin.get('repo_docs', None)
        if has_doc_repo:
            evidence = subcriterion_data['evidence']['failure']
        else:
            subcriterion_valid = True
            evidence = subcriterion_data['evidence']['success']
        self.set_valid(subcriterion_data, subcriterion_valid)

        return {
            'id': subcriterion,
            'description': subcriterion_data['description'],
            'valid': subcriterion_valid,
            'evidence': evidence,
            'standard': self.standard
        }

    def validate(self):
        # self.opts.stdin contains the input data given by the user through
        # the QAA module
        self.stdin = self.opts.stdin

        criterion = 'QC.Doc'
        criterion_data = sqaaas_utils.load_criterion_from_standard(criterion)
        subcriteria = []

        subcriteria.append(self.validate_qc_doc01(criterion_data))

        return {
            'valid': self.valid,
            'subcriteria': subcriteria,
            'data_unstructured': self.stdin
        }
