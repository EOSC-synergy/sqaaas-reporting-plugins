import logging

from report2sqaaas import utils as sqaaas_utils


logger = logging.getLogger('sqaaas.reporting.plugins.fairEva')


class fairEva(sqaaas_utils.BaseValidator):
    valid = False

    def parse(self, file_name):
        return sqaaas_utils.load_json(file_name)

    def validate(self):
        logger.debug('Running SQAaaS\' <%s> validator' % self.name)

        # FIXME Same hint for all
        criterion = 'QC.FAIR'
        criterion_data = sqaaas_utils.load_criterion_from_standard(
            criterion
        )
        hint = criterion_data['QC.FAIR01']['hint']

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
                    url = "https://doi.org/10.15497/rda00050"
                    evidence = "Indicator: %s | Check: %s" % (key, url)
                    result.append({"id": json_res[sb][key]['name'],
                                   "valid": valid,
                                   "description": json_res[sb][key]['msg'],
                                   "hint": hint,
                                   "evidence": evidence})
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
