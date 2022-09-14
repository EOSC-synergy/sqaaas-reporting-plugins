import logging

from report2sqaaas import utils as sqaaas_utils


logger = logging.getLogger('sqaaas.reporting.plugins.jenkins_exit_status')


class JenkinsExitStatusValidator(sqaaas_utils.BaseValidator):
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

    def validate(self):
        criterion_data = sqaaas_utils.load_criterion_from_standard(
            self.opts.criterion
        )
        subcriterion_name = self.get_subcriterion()
        subcriteria = []
        subcriterion_data = criterion_data[subcriterion_name]
        subcriterion_valid = False
        evidence = None

        # Only validate via Jenkins exit status
        if self.opts.status in ['SUCCESS']:
            subcriterion_valid = True
            evidence = subcriterion_data['evidence']['success']
        else:
            evidence = subcriterion_data['evidence']['failure']

        requirement_level = subcriterion_data['requirement_level']
        subcriteria.append({
            'id': subcriterion_name,
            'description': subcriterion_data['description'],
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
            'standard': self.standard
        }
