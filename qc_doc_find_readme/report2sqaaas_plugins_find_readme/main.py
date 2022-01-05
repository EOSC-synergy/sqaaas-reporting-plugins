import logging

from report2sqaaas import utils as sqaaas_utils


logger = logging.getLogger('sqaaas.reporting.plugins.find_readme')


class FindReadmeValidator(sqaaas_utils.BaseValidator):
    valid = False

    @staticmethod
    def populate_parser(parser):
        parser.add_argument(
            '--threshold-find_readme',
            metavar='NUMBER',
            type=int,
            default=0,
            help='Minimum size of the README file (in bytes)'
        )

    def validate(self):
        threshold = self.opts.threshold_find_readme
        try:
            readme_data_list = sqaaas_utils.load_json(self.opts.stdout)
        except ValueError:
            readme_data_list = []
            logger.error('Input data does not contain a valid JSON')

        self.valid = True
        if readme_data_list:
            for readme_data in readme_data_list:
                for readme_file, readme_size in readme_data.items():
                    if readme_size['size'] <= threshold:
                        logger.warn((
                            'README file <%s> is not big enough (threshold '
                            '%s)' % (readme_file, threshold)
                        ))
                        self.valid = False
        else:
            logger.warn('JSON payload is empty')

        return {
            'valid': self.valid,
            'data_unstructured': readme_data_list
        }
