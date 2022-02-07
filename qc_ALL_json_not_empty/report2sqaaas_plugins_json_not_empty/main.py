import logging

from report2sqaaas import utils as sqaaas_utils


logger = logging.getLogger('sqaaas.reporting.plugins.json_not_empty')


class JsonNotEmptyValidator(sqaaas_utils.BaseValidator):
    valid = False

    def validate(self):
        evidence = []
        try:
            data = sqaaas_utils.load_json(self.opts.stdout)
        except ValueError as e:
            data = {}
            evidence.append(
                'Input data does not contain a valid JSON: %s' % e
            )
        else:
            if data:
                self.valid = True
                evidence.append('Found a non-empty JSON payload')
            else:
                evidence.append('JSON payload is empty')

        return {
            'valid': self.valid,
            'evidence': evidence,
            'data_unstructured': data
        }
