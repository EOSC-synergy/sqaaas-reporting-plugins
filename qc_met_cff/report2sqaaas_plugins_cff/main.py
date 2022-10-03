import logging

from report2sqaaas import utils as sqaaas_utils


logger = logging.getLogger('sqaaas.reporting.plugins.cff')


class CFFConvertValidator(sqaaas_utils.BaseValidator):
    valid = False
    standard = {
        'title': (
            'A set of Common Software Quality Assurance Baseline Criteria for '
            'Research Projects'
        ),
        'version': 'v4.0',
        'url': 'https://github.com/indigo-dc/sqa-baseline/releases/tag/v4.0',
    }

    def validate(self):
        criterion = 'QC.Met'
        criterion_data = sqaaas_utils.load_criterion_from_standard(
            criterion
        )
        subcriteria = []

        subcriterion = 'QC.Met01'
        subcriterion_data = criterion_data[subcriterion]
        subcriterion_valid = True
        evidence = None

        data = sqaaas_utils.load_data(self.opts.stdout.strip())
        lines = data.split('\n')
        lines = list(filter(None, lines))

        for line in lines:
            if line.find('ValidationError') != -1:
                subcriterion_valid = False

        if subcriterion_valid:
            evidence = subcriterion_data['evidence']['success']
        else:
            evidence = subcriterion_data['evidence']['failure']

        requirement_level = subcriterion_data['requirement_level']
        subcriteria.append({
            'id': subcriterion,
            'description': subcriterion_data['description'],
            'hint': subcriterion_data['hint'],
            'valid': subcriterion_valid,
            'evidence': evidence,
            'requirement_level': requirement_level
        })

        self.valid = subcriterion_valid
        if (
            (not subcriterion_valid) and
            (requirement_level in ['MUST'])
        ):
            self.valid = False

        return {
            'valid': self.valid,
            'subcriteria': subcriteria,
            'standard': self.standard,
            'data_unstructured': data
        }
