import logging

from report2sqaaas import utils as sqaaas_utils


logger = logging.getLogger('sqaaas.reporting.plugins.find_readme')


class FindReadmeValidator(sqaaas_utils.BaseValidator):
    valid = False
    threshold = 1

    def validate(self):
        try:
            readme_data_list = sqaaas_utils.load_json(self.opts.stdout)
        except ValueError:
            readme_data_list = []
            logger.error('Input data does not contain a valid JSON')

        self.valid = True
        if readme_data_list:
            for readme_data in readme_data_list:
                for readme_file, readme_size in readme_data.items():
                    if readme_size['size'] < self.threshold:
                        logger.warn((
                            'README file <%s> is not big enough (self.threshold '
                            '%s)' % (readme_file, self.threshold)
                        ))
                        self.valid = False
        else:
            logger.warn('JSON payload is empty')

        return {
            'valid': self.valid,
            'data_unstructured': readme_data_list
        }
