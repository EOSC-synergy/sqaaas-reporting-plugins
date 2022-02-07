import logging

from report2sqaaas import utils as sqaaas_utils


logger = logging.getLogger('sqaaas.reporting.plugins.find_doc_files')


class FindDocFilesValidator(sqaaas_utils.BaseValidator):
    valid = False
    threshold = 1

    def validate(self):
        evidence = []
        try:
            data_list = sqaaas_utils.load_json(self.opts.stdout)
            logger.debug('Parsing output: %s' % data_list)
        except ValueError:
            data_list = []
            evidence.append('Input data does not contain a valid JSON')
        else:
            if data_list:
                self.valid = True
                for data in data_list:
                    for file_type, file_data in data.items():
                        if not file_data:
                            evidence.append((
                                '%s file not found in the '
                                'repository' % file_type
                            ))
                        for file_name, size in file_data.items():
                            if size['size'] < self.threshold:
                                self.valid = False
                                evidence.append(
                                    '%s file found, but size (%s bytes) is '
                                    'considered insufficient: %s (threshold '
                                    '%s)' % (
                                        file_type,
                                        file_name,
                                        size['size'],
                                        self.threshold
                                    )
                                )
                            else:
                                evidence.append(
                                    '%s file found: %s (size: %s bytes)' % (
                                        file_type, file_name, size['size']
                                    )
                                )
            else:
                evidence.append('JSON payload is empty')

        # Print evidence messages
        for reason in evidence:
            logger.debug(reason)

        out = {
            'valid': self.valid,
            'evidence': evidence,
            'data_unstructured': data_list
        }

        return out
