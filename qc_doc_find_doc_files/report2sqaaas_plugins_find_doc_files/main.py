import logging

from report2sqaaas import utils as sqaaas_utils


logger = logging.getLogger('sqaaas.reporting.plugins.find_doc_files')


class FindDocFilesValidator(sqaaas_utils.BaseValidator):
    valid = False
    threshold = 1
    criteria_mapping = {
        'README': 'QC.Doc06.1',
        'CONTRIBUTING': 'QC.Doc06.2',
        'CODE_OF_CONDUCT': 'QC.Doc06.3'
    }
    standard = {
        'title': (
            'A set of Common Software Quality Assurance Baseline Criteria for '
            'Research Projects'
        ),
        'version': 'v4.0',
        'url': 'https://github.com/indigo-dc/sqa-baseline/releases/tag/v4.0',
    }

    def validate(self):
        criterion = 'QC.Doc'
        criterion_data = sqaaas_utils.load_criterion_from_standard(
            criterion
        )
        subcriteria = []
        try:
            data = sqaaas_utils.load_json(self.opts.stdout)
            logger.debug('Parsing output: %s' % data)
        except ValueError:
            data = {}
            logger.error('Input data does not contain a valid JSON')
        else:
            if data:
                self.valid = True
                for file_type, file_list in data.items():
                    subcriterion = self.criteria_mapping[file_type]
                    subcriterion_data = criterion_data[subcriterion]
                    subcriterion_valid = False
                    evidence = None
                    if not file_list:
                        evidence = subcriterion_data['evidence']['failure']
                    for file_data in file_list:
                        file_name = file_data['file_name']
                        size = file_data['size']
                        if size < self.threshold:
                            evidence = ((
                                'README file <%s> exists in the code '
                                'repository, but not big enough (threshold '
                                '%s)' % (file_name, self.threshold)
                            ))
                            logger.warn(evidence)
                        else:
                            evidence = subcriterion_data['evidence']['success']
                            subcriterion_valid = True

                    requirement_level = subcriterion_data['requirement_level']
                    if evidence:
                        subcriteria.append({
                            'id': subcriterion,
                            'description': subcriterion_data['description'],
                            'hint': subcriterion_data['hint'],
                            'valid': subcriterion_valid,
                            'evidence': evidence,
                            'requirement_level': requirement_level
                        })
                        logger.info(evidence)

                    if (
                        (not subcriterion_valid) and
                        (requirement_level in ['MUST'])
                    ):
                        self.valid = False
            else:
                logger.error('JSON payload is empty!')

        return {
            'valid': self.valid,
            'subcriteria': subcriteria,
            'standard': self.standard,
            'data_unstructured': data
        }
