import logging

from report2sqaaas import utils as sqaaas_utils


logger = logging.getLogger('sqaaas.reporting.plugins.markdownlint')


class MarkdownLintValidator(sqaaas_utils.BaseValidator):
    valid = False
    standard = {
        'title': (
            'A set of Common Software Quality Assurance Baseline Criteria for '
            'Research Projects'
        ),
        'version': 'v4.0',
        'url': 'https://github.com/indigo-dc/sqa-baseline/releases/tag/v4.0',
    }

    def parse_markdownlint(self, data):
        data_to_return = {}
        for rule_issue in data:
            file_name = rule_issue['filename']
            rule_code = rule_issue['rule']
            line = rule_issue['line']

            if rule_code in list(data_to_return.get(file_name, {})):
                data_to_return[file_name][rule_code]['line'].append(line)
            else:
                d_rule = {
                    'description': rule_issue['description'],
                    'line': [line]
                }
                try:
                    data_to_return[file_name][rule_code] = d_rule
                except KeyError:
                    data_to_return[file_name] = {
                        rule_code: d_rule
                    }
        return data_to_return

    def validate(self):
        criterion = 'QC.Doc'
        criterion_data = sqaaas_utils.load_criterion_from_standard(
            criterion
        )
        subcriteria = []
        # QC.Doc02.X
        subcriterion = 'QC.Doc02.X'
        subcriterion_data = criterion_data[subcriterion]
        subcriterion_valid = False
        evidence = None

        try:
            data = sqaaas_utils.load_json(self.opts.stdout)
        except ValueError:
            data = {}
            logger.error('Input data does not contain a valid JSON')

        if not data:
            subcriterion_valid = True
            evidence = subcriterion_data['evidence']['success']
        else:
            evidence = subcriterion_data['evidence']['failure']

        doc_file_type = self.opts.doc_file_type
        doc_file_standard = self.opts.doc_file_standard

        evidence = evidence % doc_file_standard
        if evidence:
            logger.info(evidence)

        requirement_level = subcriterion_data['requirement_level']
        subcriteria.append({
            'id': subcriterion,
            'description': subcriterion_data['description'] % doc_file_type,
            'hint': subcriterion_data['hint'],
            'valid': subcriterion_valid,
            'evidence': evidence,
            'requirement_level': requirement_level
        })

        if (
            (not subcriterion_valid) and
            (requirement_level in ['MUST'])
        ):
            self.valid = False
        else:
            self.valid = True

        if doc_file_type in ['Markdown']:
            data_to_return = self.parse_markdownlint(data)
        else:
            data_to_return = data

        return {
            'valid': self.valid,
            'subcriteria': subcriteria,
            'standard': self.standard,
            'data_unstructured': data_to_return
        }
