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

        subcriteria_groups = {
            'findable': 'QC.FAIR.F',
            'accessible': 'QC.FAIR.A',
            'interoperable': 'QC.FAIR.I',
            'reusable': 'QC.FAIR.R'
        }
        for group, criterion in subcriteria_groups.items():
            _criterion_data = sqaaas_utils.load_criterion_from_standard(
                criterion
            )
            for key in json_res[group]:
                _key = key.upper()
                try:
                    _subcriterion_data = _criterion_data[_key]
                except KeyError:
                    logger.error(
                        'Could not find <%s> RDA indicator in the '
                        'standard' % _key
                    )
                else:
                    if key != 'result':
                        _evidence = _subcriterion_data['evidence']['failure']
                        if json_res[group][key]['test_status'] == "pass":
                            valid = True
                            _evidence = _subcriterion_data['evidence']['success']
                        else:
                            valid = False
                        result.append(
                            {
                                "id": _key,
                                "valid": valid,
                                "description": _subcriterion_data['description'],
                                "hint": _subcriterion_data['hint'],
                                "evidence": _evidence,
                                "requirement_level": _subcriterion_data['requirement_level']
                            }
                        )
        if len(result) > 0:
            self.valid = True

        return {
            'valid': 'true',
            'subcriteria': result,
            'standard': {'title': 'RDA Indicators',
                         'version': 'v1.0',
                         'url': 'https://doi.org/10.15497/rda00050'
                         },
            'data_unstructured': json_res
        }
