from report2sqaaas import utils as sqaaas_utils


class LicenseeValidator(sqaaas_utils.BaseValidator):
    def parse(self, file_name):
        return sqaaas_utils.load_json(file_name)

    def validate(self, file_name):
        print('Running LicenseeValidator..')
        data = self.parse(file_name)
