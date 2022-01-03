import logging

from report2sqaaas import utils as sqaaas_utils


logger = logging.getLogger('sqaaas.reporting.plugins.markdownlint')


class MarkdownLintValidator(sqaaas_utils.BaseValidator):
    valid = False

    def validate(self):
        try:
            data = sqaaas_utils.load_json(self.opts.stdout)
        except ValueError:
            data = {}
            logger.error('Input data does not contain a valid JSON')

        if not data:
            logger.info('No issue found by markdownlint!')
            self.valid = True
        else:
            logger.info('Issues found by markdownlint')

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
            'data_unstructured': data_to_return
        }
