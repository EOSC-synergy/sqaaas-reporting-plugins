import logging

from report2sqaaas import utils as sqaaas_utils


logger = logging.getLogger('sqaaas.reporting.plugins.markdownlint')


class MarkdownLintValidator(sqaaas_utils.BaseValidator):
    valid = False

    def validate(self):
        report = []
        try:
            data = sqaaas_utils.load_json(self.opts.stdout)
        except ValueError:
            data = {}
            report.append('Input data does not contain a valid JSON')

        if not data:
            report.append('No issues found by <markdownlint> tool')
            self.valid = True
        else:
            report.append('Issues found by <markdownlint> tool')

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

        # Print report messages
        for reason in report:
            logger.debug(reason)

        return {
            'valid': self.valid,
            'report': report,
            'data_unstructured': data_to_return
        }
