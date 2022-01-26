import logging

from report2sqaaas import utils as sqaaas_utils


logger = logging.getLogger('sqaaas.reporting.plugins.find_doc_files')


class FindDocFilesValidator(sqaaas_utils.BaseValidator):
    valid = False
    threshold = 1

    def validate(self):
        reason = None
        try:
            data_list = sqaaas_utils.load_json(self.opts.stdout)
            logger.debug('Parsing output: %s' % data_list)
        except ValueError:
            data_list = []
            reason = 'Input data does not contain a valid JSON'
            logger.error(reason)
        else:
            if data_list:
                self.valid = True
                for data in data_list:
                    for file_name, size in data.items():
                        if size['size'] < self.threshold:
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
            'data_unstructured': data_list
        }
        if reason:
            out['reason'] = reason

        return  out
