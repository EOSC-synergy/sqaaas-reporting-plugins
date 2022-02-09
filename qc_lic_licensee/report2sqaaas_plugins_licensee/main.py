import logging

from report2sqaaas import utils as sqaaas_utils


logger = logging.getLogger('sqaaas.reporting.plugins.licensee')


class LicenseeValidator(sqaaas_utils.BaseValidator):
    valid = False
    threshold = 50
    standard = {
        'title': (
            'A set of Common Software Quality Assurance Baseline Criteria for '
            'Research Projects'
        ),
        'version': 'v4.0',
        'url': 'https://github.com/indigo-dc/sqa-baseline/releases/tag/v4.0',
        'subcriteria': ['QC.Lic01']
    }

    def parse(self, file_name):
        return sqaaas_utils.load_json(file_name)

    def validate(self):
        evidence = None
        try:
            data = self.parse(self.opts.stdout)
            at_least_one_license = False
            trusted_licenses_no = 0
            for license_data in data['matched_files']:
                file_name = license_data['filename']
                if not license_data.get('matcher', None):
                    logger.warn(
                        'Matcher data not found for file <%s>. '
                        'Skipping..' % file_name
                    )
                    continue
                confidence_level = license_data['matcher']['confidence']
                if confidence_level > self.threshold:
                    at_least_one_license = True
                    trusted_licenses_no += 1
            if at_least_one_license:
                self.valid = True
                evidence = (
                    'Valid LICENSE found (confidence level: %s): %s' % (
                        confidence_level, file_name
                    )
                )
            else:
                evidence = 'No valid LICENSE found'
        except ValueError as e:
            data = {}
            evidence = 'Input data does not contain a valid JSON: %s' % e

        return {
            'valid': self.valid,
            'subcriteria': {
                'id': 'QC.Lic01',
                'evidence': evidence,
                'valid': self.valid,
                'standard': self.standard
            },
            'data_unstructured': data
        }
