import logging

from report2sqaaas import utils as sqaaas_utils


logger = logging.getLogger('sqaaas.reporting.plugins.licensee')


class LicenseeValidator(sqaaas_utils.BaseValidator):
    valid = False

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

    def validate(self):
        logger.debug('Running SQAaaS\' <%s> validator' % self.name)
        data = self.parse(self.opts.stdout)
        at_least_one_license = False
        trusted_licenses_no = 0
        for license_data in data['matched_files']:
            if license_data['matcher']['confidence'] > self.opts.threshold:
                at_least_one_license = True
                trusted_licenses_no += 1
        if at_least_one_license:
            self.valid = True

        return {
            'valid': self.valid,
            'data_unstructured': data
        }
