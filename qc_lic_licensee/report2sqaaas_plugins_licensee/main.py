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

    def validate_qc_lic01():
        # QC.Lic01
        subcriterion = 'QC.Lic01'
        subcriterion_data = criterion_data[subcriterion]
        subcriterion_valid = False
        evidence = None
        if self.valid:
            subcriterion_valid = True
            evidence = subcriterion_data['evidence']['success']
        else:
            evidence = subcriterion_data['evidence']['failure']

        return {
            'id': subcriterion,
            'description': subcriterion_data['description'],
            'valid': subcriterion_valid,
            'evidence': evidence,
            'standard': self.standard
        }

    def parse(self, file_name):
        return sqaaas_utils.load_json(file_name)

    def validate(self):
        criterion = 'QC.Lic'
        criterion_data = sqaaas_utils.load_criterion_from_standard(criterion)
        subcriteria = []

        evidence = None
        try:
            data = sqaaas_utils.load_json(self.opts.stdout)
        except ValueError as e:
            data = {}
            logger.error('Input data does not contain a valid JSON: %s' % e)
        else:
            at_least_one_license = False
            trusted_licenses_no = 0
            for license_data in data['matched_files']:
                if not license_data.get('matcher', None):
                    logger.warn(
                        'Matcher data not found for file <%s>. '
                        'Skipping..' % file_name
                    )
                    continue
                file_name = license_data['filename']
                confidence_level = license_data['matcher']['confidence']
                if confidence_level > self.threshold:
                    at_least_one_license = True
                    trusted_licenses_no += 1
            if at_least_one_license:
                self.valid = True
                logger.info(
                    'Valid LICENSE found (confidence level: %s): %s' % (
                        confidence_level, file_name
                    )
                )
            else:
                logger.warn('No valid LICENSE found')

        subcriteria.append(self.validate_qc_lic01())

        return {
            'valid': self.valid,
            'subcriteria': subcriteria,
            'data_unstructured': data
        }
