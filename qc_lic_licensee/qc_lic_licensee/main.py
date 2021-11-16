from report2sqaaas import utils as sqaaas_utils


class LicenseeValidator(sqaaas_utils.BaseValidator):
    def validate(self, file_name):
        print('Running LicenseeValidator..')
