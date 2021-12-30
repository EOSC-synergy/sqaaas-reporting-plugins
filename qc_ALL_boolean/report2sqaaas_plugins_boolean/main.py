import logging

from report2sqaaas import utils as sqaaas_utils


logger = logging.getLogger('sqaaas.reporting.plugins.boolean')


class BooleanValidator(sqaaas_utils.BaseValidator):
    valid = False

    def validate(self):
        if self.opts.stdout.lower() in [
            'true', 'false'
        ]:
            self.valid = True

        return {
            'valid': self.valid,
        }
