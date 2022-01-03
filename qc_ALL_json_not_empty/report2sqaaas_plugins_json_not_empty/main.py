import logging

from report2sqaaas import utils as sqaaas_utils


logger = logging.getLogger('sqaaas.reporting.plugins.json_not_empty')


class JsonNotEmptyValidator(sqaaas_utils.BaseValidator):
    valid = False

    def validate(self):
        try:
            data = sqaaas_utils.load_json(self.opts.stdout)
        except ValueError:
            data = {}
            logger.error('Input data does not contain a valid JSON')

        if data:
            logger.info('Found a non-empty JSON payload')
            self.valid = True
        else:
            logger.info('JSON payload is empty')

        return {
            'valid': self.valid,
            'data_unstructured': data
        }
