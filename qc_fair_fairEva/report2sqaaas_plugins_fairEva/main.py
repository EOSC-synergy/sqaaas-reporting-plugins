import logging

from report2sqaaas import utils as sqaaas_utils


logger = logging.getLogger('sqaaas.reporting.plugins.fairEva')


class fairEva(sqaaas_utils.BaseValidator):
    valid = False

    def parse(self, file_name):
        return sqaaas_utils.load_json(file_name)

    def validate(self):
        logger.debug('Running SQAaaS\' <%s> validator' % self.name)
        json_res = self.parse(self.opts.stdout)
        result = []
        subcriteria_groups = ['findable', 'accessible',
                              'interoperable', 'reusable']
        for sb in subcriteria_groups:
            for key in json_res[sb]:
                if key != 'result':
                    if json_res[sb][key]['test_status'] == "pass":
                        valid = True
                    else:
                        valid = False

                    result.append({"id": json_res[sb][key]['name'],
                                   "valid": valid,
                                   "description": json_res[sb][key]['msg'],
                                   "evidence": "Indicator: %s | Check: https://doi.org/10.15497/rda00050"
                                   % json_res[sb][key]['name']})
        if len(result) > 0:
            self.valid = True

        return {
            'valid': 'true',
            'subcriteria': result,
            'standard': {'title': 'RDA Indicators',
                         'version': 'v1.0',
                         'url': 'https://doi.org/10.15497/rda00050'
            },
            'data_unstructured': 'TODO'
        }
