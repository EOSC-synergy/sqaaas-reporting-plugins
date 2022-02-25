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

    def validate(self):
        criterion = 'QC.Sty'
        criterion_data = sqaaas_utils.load_criterion_from_standard(
            criterion
        )
        subcriteria = []
        # QC.Sty01
        subcriterion = 'QC.Sty01'
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

        if evidence:
            logger.info(evidence)

        doc_file_type = 'Markdown'
        doc_file_standard = 'markdownlint'

        subcriteria.append({
            'id': subcriterion,
            'description': subcriterion_data['description'] % doc_file_type,
            'valid': subcriterion_valid,
            'evidence': evidence % (doc_file_type, doc_file_standard)
        })

        requirement_level = subcriterion_data['requirement_level']
        self.valid = subcriterion_valid
        if (
            (not subcriterion_valid) and
            (requirement_level in ['MUST'])
        ):
            self.valid = False

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

        return {
            'valid': self.valid,
            'subcriteria': subcriteria,
            'standard': self.standard,
            'data_unstructured': data_to_return
        }
