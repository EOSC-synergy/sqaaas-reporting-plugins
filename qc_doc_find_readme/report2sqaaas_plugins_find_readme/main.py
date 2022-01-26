import logging

from report2sqaaas import utils as sqaaas_utils


logger = logging.getLogger('sqaaas.reporting.plugins.find_readme')


class FindReadmeValidator(sqaaas_utils.BaseValidator):
    valid = False
    threshold = 1

    def validate(self):
        reason = None
        try:
            readme_data_list = sqaaas_utils.load_json(self.opts.stdout)
            logger.debug('Parsing output: %s' % readme_data_list)
        except ValueError:
            readme_data_list = []
            reason = 'Input data does not contain a valid JSON'
            logger.error(reason)
        else:
            if readme_data_list:
                self.valid = True
                for readme_data in readme_data_list:
                    for readme_file, readme_size in readme_data.items():
                        if readme_size['size'] < self.threshold:
                            logger.warn((
                                'File <%s> is not big enough (self.threshold '
                                '%s)' % (readme_file, self.threshold)
                            ))
                            self.valid = False
                        else:
                            logger.debug((
                                'Size good enough for <%s> collaboration-enabling '
                                'file: %s bytes' % (
                                    readme_file,
                                    readme_size
                                )
                            ))
            else:
                reason = 'JSON payload is empty'
                logger.warn(reason)

        out = {
            'valid': self.valid,
            'data_unstructured': readme_data_list
        }
        if reason:
            out['reason'] = reason

        return  out
