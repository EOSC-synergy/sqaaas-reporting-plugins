import logging
import re

from report2sqaaas import utils as sqaaas_utils


logger = logging.getLogger('sqaaas.reporting.plugins.flake8')


class Flake8Validator(sqaaas_utils.BaseValidator):
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
        criterion = 'QC.Sty'
        criterion_data = sqaaas_utils.load_criterion_from_standard(
            criterion
        )
        subcriteria = []
        # QC.Sty01
        subcriterion = 'QC.Sty01'
        subcriterion_data = criterion_data[subcriterion]
        subcriterion_valid = True
        evidence = None

        data = sqaaas_utils.load_data(self.opts.stdout.strip())
        lines = data.split('\n')
        lines = list(filter(None, lines))
        pattern = '(.+):(\d+):(\d+): ([A-Z]\d{3}) (.+)'
        summary = {
            'stylistic': {
                'warnings': 0,
                'errors': 0
            },
            'logical': 0,
            'analytical': 0
        }
        if not lines:
            logger.error('No flake8 output has been generated')
        else:
            for line in lines:
                try:
                    matches = re.match(pattern, line)
                except re.error:
                    matches = None
                if matches:
                    try:
                        path, row, col, code, text = re.findall(
                            pattern, line
                        )[0]
                    except IndexError:
                        logger.warning(
                            'Could not parse flake8 output line: "%s"' % line
                        )
                    else:
                        if code[0] in ['W']:
                            summary['stylistic']['warnings'] += 1
                        else:
                            subcriterion_valid = False
                            if code[0] in ['E']:
                                summary['stylistic']['errors'] += 1
                            if code[0] in ['F']:
                                summary['logical'] += 1
                            if code[0] in ['C']:
                                summary['analytical'] += 1

            if subcriterion_valid:
                evidence = subcriterion_data['evidence']['success']
            else:
                evidence = subcriterion_data['evidence']['failure']
            logger.info(evidence)

            file_type = 'Python'
            file_standard = 'flake8 (pycodestyle, pyflakes, mccabe)'

            for linting_type, metrics in summary.items():
                logger.info('Linting %s issues found: %s' % (
                    linting_type, metrics
                ))

            subcriteria.append({
                'id': subcriterion,
                'description': subcriterion_data['description'] % file_type,
                'valid': subcriterion_valid,
                'evidence': evidence % (file_type, file_standard)
            })

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
