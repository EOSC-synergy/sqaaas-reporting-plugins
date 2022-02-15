import logging
import pathlib
import requests

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
    }
    criterion_data = None

    def validate_qc_lic01(self, license_type, license_file):
        subcriteria = []
        # QC.Lic01
        subcriterion = 'QC.Lic01'
        subcriterion_data = self.criterion_data[subcriterion]
        subcriterion_valid = False
        evidence = None
        if self.valid:
            subcriterion_valid = True
            evidence = subcriterion_data['evidence']['success'] % license_type
        else:
            evidence = subcriterion_data['evidence']['failure']
        subcriteria.append({
            'id': subcriterion,
            'description': subcriterion_data['description'],
            'valid': subcriterion_valid,
            'evidence': evidence,
            'standard': self.standard
        })
        # QC.Lic01.1
        subcriterion = 'QC.Lic01.1'
        subcriterion_data = self.criterion_data[subcriterion]
        subcriterion_valid = False
        license_path = pathlib.Path(license_file)
        evidence = None
        if license_path.parent.as_posix() in ['.']:
            subcriterion_valid = True
            evidence = subcriterion_data['evidence']['success'] % license_file
        else:
            evidence = subcriterion_data['evidence']['failure'] % license_file
        subcriteria.append({
            'id': subcriterion,
            'description': subcriterion_data['description'],
            'valid': subcriterion_valid,
            'evidence': evidence,
            'standard': self.standard
        })
        return subcriteria

    def validate_qc_lic02(self, license_type):
        subcriteria = []
        for subcriterion in [
                {
                    'id': 'QC.Lic02',
                    'keyword': 'approved',
                    'osi_endpoint': 'osi-approved'
                },
                {
                    'id': 'QC.Lic02.1',
                    'keyword': 'popular',
                    'osi_endpoint': 'popular'
                }
        ]:
            _id = subcriterion['id']
            _endpoint = subcriterion['osi_endpoint']
            _keyword = subcriterion['keyword']
            subcriterion_data = self.criterion_data[_id]
            subcriterion_valid = False
            OSI_ENDPOINT = 'https://api.opensource.org/licenses/%s' % _endpoint
            r = requests.get(OSI_ENDPOINT)
            try:
                r.raise_for_status()
            except requests.exceptions.HTTPError as e:
                logger.error((
                    'Cannot check compliance with Open Source Initiative\'s '
                    '%s licenses: %s' % (e, _keyword)
                ))
            else:
                license_list = r.json()
                licenses = [
                    license_data['id'] for license_data in license_list
                ]
                if license_type in licenses:
                    subcriterion_valid = True
                    evidence = subcriterion_data['evidence']['success']
                else:
                    evidence = subcriterion_data['evidence']['failure']
                evidence = evidence % license_type
                logger.info(evidence)

            subcriteria.append({
                'id': _id,
                'description': subcriterion_data['description'],
                'valid': subcriterion_valid,
                'evidence': evidence,
                'standard': self.standard
            })
        return subcriteria

    def validate(self):
        criterion = 'QC.Lic'
        self.criterion_data = sqaaas_utils.load_criterion_from_standard(
            criterion
        )
        subcriteria = []

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
                matched_license = license_data['matched_license']
                confidence_level = license_data['matcher']['confidence']
                if confidence_level > self.threshold:
                    at_least_one_license = True
                    trusted_licenses_no += 1
            if at_least_one_license:
                self.valid = True
                logger.info((
                    'Open source\'s <%s> license found (file: %s, confidence '
                    'level: %s)' % (
                        matched_license, confidence_level, file_name
                    )
                ))
            else:
                logger.warn('No valid LICENSE found')

        subcriteria.extend(self.validate_qc_lic01(matched_license, file_name))
        # FIXME QC.Lic02 is NOT part of parsing licensee output, but for the
        # time being it is easier to be checked here as it requires to know
        # (have as input) the license found
        subcriteria.extend(self.validate_qc_lic02(matched_license))

        return {
            'valid': self.valid,
            'subcriteria': subcriteria,
            'data_unstructured': data
        }
