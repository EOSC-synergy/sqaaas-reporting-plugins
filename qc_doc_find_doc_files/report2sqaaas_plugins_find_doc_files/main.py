import logging

from report2sqaaas import utils as sqaaas_utils


logger = logging.getLogger('sqaaas.reporting.plugins.find_doc_files')


class FindDocFilesValidator(sqaaas_utils.BaseValidator):
    valid = False
    threshold = 1

    def validate(self):
        reason = None
        try:
            data = sqaaas_utils.load_json(self.opts.stdout)
            logger.debug('Parsing output: %s' % data)
        except ValueError:
            data = {}
            reason = 'Input data does not contain a valid JSON'
            logger.error(reason)
        else:
            if data:
                self.valid = True
                for file_type, file_list in data.items():
                    if not file_list:
                        logger.warn('%s file not found' % file_type)
                    for file_data in file_list:
                        file_name = file_data['file_name']
                        size = file_data['size']
                        if size < self.threshold:
                            logger.warn((
                                'File <%s> is not big enough (self.threshold '
                                '%s)' % (file_name, self.threshold)
                            ))
                            self.valid = False
                        else:
                            logger.debug((
                                'Size good enough for <%s> collaboration-enabling '
                                'file: %s bytes' % (
                                    file_name,
                                    size
                                )
                            ))
            else:
                reason = 'JSON payload is empty'
                logger.warn(reason)

        out = {
            'valid': self.valid,
            'data_unstructured': data
        }
        if reason:
            out['reason'] = reason

        return  out
