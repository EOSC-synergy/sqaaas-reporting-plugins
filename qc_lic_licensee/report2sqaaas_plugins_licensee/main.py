import logging

from report2sqaaas import utils as sqaaas_utils


logger = logging.getLogger('sqaaas.reporting.plugins.licensee')


class LicenseeValidator(sqaaas_utils.BaseValidator):
    name = 'licensee'
    valid = False
    valid_threshold = 50

    @staticmethod
    def populate_parser(parser):
        parser.add_argument(
            '--threshold',
            metavar='NUMBER',
            type=int,
            help=(
                'Optional argument required by some plugins in order to state '
                'whether the validation is successful'
            )
        )

    def parse(self, file_name):
        return sqaaas_utils.load_json(file_name)

    def validate(self, stdout_input):
        logger.debug('Running SQAaaS\' <%s> validator' % self.name)
        data = self.parse(stdout_input)
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
