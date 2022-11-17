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

    def set_valid(self, subcriterion_data, subcriterion_valid):
        requirement_level = subcriterion_data['requirement_level']
        if (
            (not subcriterion_valid) and
            (requirement_level in ['MUST'])
        ):
            self.valid = False

    def validate_qc_lic01(self, license_type, license_file):
        subcriteria = []
        # QC.Lic01
        subcriterion = 'QC.Lic01'
        subcriterion_data = self.criterion_data[subcriterion]
        subcriterion_valid = False
        evidence = None
        standard_kwargs = {
            'license_type': license_type,
            'license_file': license_file
        }

        if self.valid:
            subcriterion_valid = True
            evidence = subcriterion_data['evidence']['success']
        else:
            evidence = subcriterion_data['evidence']['failure']
        requirement_level = subcriterion_data['requirement_level']
        subcriteria.append({
            'id': subcriterion,
            'description': subcriterion_data['description'],
            'hint': subcriterion_data['hint'],
            'valid': subcriterion_valid,
            'evidence': evidence.format(**standard_kwargs),
            'requirement_level': requirement_level
        })
        self.set_valid(subcriterion_data, subcriterion_valid)
        # QC.Lic01.1
        subcriterion = 'QC.Lic01.1'
        subcriterion_data = self.criterion_data[subcriterion]
        subcriterion_valid = False
        license_path = pathlib.Path(license_file)
        evidence = None
        if license_path.parent.as_posix() in ['.']:
            subcriterion_valid = True
            evidence = subcriterion_data['evidence']['success']
        else:
            evidence = subcriterion_data['evidence']['failure']
        requirement_level = subcriterion_data['requirement_level']
        subcriteria.append({
            'id': subcriterion,
            'description': subcriterion_data['description'],
            'hint': subcriterion_data['hint'],
            'valid': subcriterion_valid,
            'evidence': evidence.format(**standard_kwargs),
            'requirement_level': requirement_level
        })
        self.set_valid(subcriterion_data, subcriterion_valid)
        return subcriteria

    def validate_qc_lic02(self, license_type):
        def do_request(osi_endpoint):
            r = None
            try:
                r = requests.get(osi_endpoint, verify=False)  # nosec
                r.raise_for_status()
            except requests.exceptions.HTTPError as e:
                evidence = ((
                    'Cannot access Open Source Initiative\'s API endpoint '
                    '<%s>: %s' % (osi_endpoint, e)
                ))
                logger.error(evidence)
            finally:
                return r

        standard_kwargs = {
            'license_type': license_type
        }
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
            subcriterion_data = self.criterion_data[_id]
            subcriterion_valid = False

            OSI_ENDPOINTS = [
                'https://api.opensource.org/licenses/%s' % _endpoint,
                'https://api.opensource.org.s3.amazonaws.com/licenses/'
                'licenses.json'
            ]
            osi_request_succeed = False
            for osi_endpoint in OSI_ENDPOINTS:
                r = do_request(osi_endpoint)
                if r:
                    osi_request_succeed = True
                    license_list = r.json()
                    licenses = [
                        license_data['id'] for license_data in license_list
                    ]
                    if license_type in licenses:
                        license_osi = license_type
                    else:
                        license_osi = None
                        for license_data in license_list:
                            for identifiers in license_data['identifiers']:
                                if identifiers['identifier'] == license_type:
                                    license_osi = license_data['id']
                                    break
                    if license_osi in licenses:
                        subcriterion_valid = True
                        evidence = subcriterion_data['evidence']['success']
                    else:
                        evidence = subcriterion_data['evidence']['failure']
                    evidence = evidence % license_type
                    logger.info(evidence)
                    break
            if not osi_request_succeed:
                evidence = ((
                    'Could not access any of the available Open Source '
                    'Initiative\'s endpoints: %s' % OSI_ENDPOINTS
                ))

            requirement_level = subcriterion_data['requirement_level']
            subcriteria.append({
                'id': _id,
                'description': subcriterion_data['description'],
                'hint': subcriterion_data['hint'],
                'valid': subcriterion_valid,
                'evidence': evidence.format(**standard_kwargs),
                'requirement_level': requirement_level
            })
            self.set_valid(subcriterion_data, subcriterion_valid)
        return subcriteria

    def validate(self):
        criterion = 'QC.Lic'
        self.criterion_data = sqaaas_utils.load_criterion_from_standard(
            criterion
        )
        subcriteria = []
        matched_license = None

        try:
            data = sqaaas_utils.load_json(self.opts.stdout)
        except ValueError as e:
            data = {}
            logger.error('Input data does not contain a valid JSON: %s' % e)
        else:
            at_least_one_license = False
            confidence_level = 0
            file_name = None
            for license_data in data['matched_files']:
                matched_license = license_data.get('matched_license', None)
                if not matched_license or matched_license in ['NONE']:
                    logger.warning('Matched license\'s value is NONE. Skipping..')
                    continue

                matcher_data = license_data.get('matcher', None)
                if not matcher_data:
                    logger.warning(
                        'Matcher data not found for file <%s>. '
                        'Skipping..' % file_name
                    )
                else:
                    confidence_level = matcher_data['confidence']
                    if confidence_level > self.threshold:
                        logger.debug(license_data['filename'])
                        file_name = license_data['filename']
                        at_least_one_license = True
                    break
            if at_least_one_license:
                self.valid = True
                logger.info((
                    'Open source\'s <%s> license found (file: %s, confidence '
                    'level: %s)' % (
                        matched_license, file_name, confidence_level
                    )
                ))
            else:
                logger.warning('No valid LICENSE found')

        subcriteria.extend(self.validate_qc_lic01(matched_license, file_name))
        # FIXME QC.Lic02 is NOT part of parsing licensee output, but for the
        # time being it is easier to be checked here as it requires to know
        # (have as input) the license found
        subcriteria.extend(self.validate_qc_lic02(matched_license))

        return {
            'valid': self.valid,
            'subcriteria': subcriteria,
            'standard': self.standard,
            'data_unstructured': data
        }
