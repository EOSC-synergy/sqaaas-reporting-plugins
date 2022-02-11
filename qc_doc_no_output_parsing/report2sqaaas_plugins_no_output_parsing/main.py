import logging

from report2sqaaas import utils as sqaaas_utils


logger = logging.getLogger('sqaaas.reporting.plugins.no_output_parsing')


class NoOutputParsingValidator(sqaaas_utils.BaseValidator):
    valid = False
    stdin = None

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

        return {
            'id': subcriterion,
            'description': subcriterion_data['description'],
            'valid': subcriterion_valid,
            'evidence': evidence
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
