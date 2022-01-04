import logging

from report2sqaaas import utils as sqaaas_utils


logger = logging.getLogger('sqaaas.reporting.plugins.boolean')


class BooleanValidator(sqaaas_utils.BaseValidator):
    valid = False

    def validate(self):
        stdout_lower = self.opts.stdout.lower()
        if stdout_lower.find('true') != 1:
            self.valid = True

        return {
            'valid': self.valid,
        }
