import logging
import re

from report2sqaaas import utils as sqaaas_utils


logger = logging.getLogger('sqaaas.reporting.plugins.bandit')


class BanditValidator(sqaaas_utils.BaseValidator):
    valid = False
    standard = {
        'title': (
            'A set of Common Software Quality Assurance Baseline Criteria for '
            'Research Projects'
        ),
        'version': 'v4.0',
        'url': 'https://github.com/indigo-dc/sqa-baseline/releases/tag/v4.0',
    }

    def remove_lines_matching(self, pattern):
        new_stdout_list = []
        stdout_lines = self.opts.stdout.split('\n')

        for line in stdout_lines:
            if not re.search(pattern, line):
                new_stdout_list.append(line)
            else:
                logger.debug((
                    'Removing line from stdout (matches pattern <%s>): '
                    '%s' % (pattern, line)
                ))

        return '\n'.join(new_stdout_list)

    def validate(self):
        criterion = 'QC.Sec'
        criterion_data = sqaaas_utils.load_criterion_from_standard(
            criterion
        )
        subcriteria = []
        new_stdout = self.remove_lines_matching(r'^\[\w+\]')
        logger.debug('New stdout: %s' % new_stdout)
        try:
            data = sqaaas_utils.load_json(new_stdout)
            logger.debug('Parsing output: %s' % data)
        except ValueError:
            data = {}
            logger.error('Input data does not contain a valid JSON')
        else:
            subcriterion = 'QC.Sec02'
            subcriterion_data = criterion_data[subcriterion]
            subcriterion_valid = False
            evidence = None
            if not data['results']:
                subcriterion_valid = True
                evidence = subcriterion_data['evidence']['success']
                logger.info(evidence)
            else:
                evidence = subcriterion_data['evidence']['failure']
                logger.warning((
                    'Bandit found %s high rated security '
                    'issues' % len(data['results'])
                ))
            subcriteria.append({
                'id': subcriterion,
                'description': subcriterion_data['description'],
                'valid': subcriterion_valid,
                'evidence': evidence
            })
            self.valid = subcriterion_valid
            requirement_level = subcriterion_data['requirement_level']
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
