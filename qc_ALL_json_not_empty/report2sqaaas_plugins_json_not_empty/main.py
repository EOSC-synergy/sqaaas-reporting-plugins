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
            reason = 'Input data does not contain a valid JSON'
            logger.error(reason)
        else:
            if data:
                reason = 'Found a non-empty JSON payload'
                logger.info(reason)
                self.valid = True
            else:
                reason = 'JSON payload is empty'
                logger.info(reason)

        return {
            'valid': self.valid,
            'reason': reason,
            'data_unstructured': data
        }
