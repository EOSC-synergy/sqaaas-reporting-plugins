import logging

from report2sqaaas import utils as sqaaas_utils


logger = logging.getLogger('sqaaas.reporting.plugins.boolean')


class BooleanValidator(sqaaas_utils.BaseValidator):
    valid = False
