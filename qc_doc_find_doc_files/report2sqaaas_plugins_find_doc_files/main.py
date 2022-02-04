import logging

from report2sqaaas import utils as sqaaas_utils


logger = logging.getLogger('sqaaas.reporting.plugins.find_doc_files')


class FindDocFilesValidator(sqaaas_utils.BaseValidator):
    valid = False
    threshold = 1

    def validate(self):
        report = []
        try:
            data_list = sqaaas_utils.load_json(self.opts.stdout)
            logger.debug('Parsing output: %s' % data_list)
        except ValueError:
            data_list = []
            report.append('Input data does not contain a valid JSON')
        else:
            if data_list:
                self.valid = True
                for data in data_list:
                    for file_type, file_data in data.items():
                        if not file_type:
                            report.append('%s file not found' % file_type)
                        for file_name, size in file_data.items():
                            if size['size'] < self.threshold:
                                self.valid = False
                                report.append(
                                    '%s file found, but size (%s bytes) is '
                                    'considered insufficient: %s (threshold '
                                    '%s)' % (
                                        file_type,
                                        file_name,
                                        size,
                                        self.threshold
                                    )
                                )
                            else:
                                report.append('%s file found: %s (size %s)' % (
                                    file_type, file_name, size
                                ))
            else:
                report.append('JSON payload is empty')

        # Print report messages
        for reason in report:
            logger.debug(reason)

        out = {
            'valid': self.valid,
            'report': report,
            'data_unstructured': data_list
        }

        return out
