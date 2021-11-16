from report2sqaaas import utils as sqaaas_utils


class LicenseeValidator(sqaaas_utils.BaseValidator):
    valid = False
    valid_threshold = 50

    def parse(self, file_name):
        return sqaaas_utils.load_json(file_name)

    def validate(self, file_name):
        print('Running LicenseeValidator..')
        data = self.parse(file_name)
        at_least_one_license = False
        trusted_licenses_no = 0
        for license_data in data['matched_files']:
            if license_data['matcher']['confidence'] > self.valid_threshold:
                at_least_one_license = True
                trusted_licenses_no += 1
        if at_least_one_license:
            self.valid = True

        return {
            'valid': self.valid,
            'data_unstructured': data
        }
