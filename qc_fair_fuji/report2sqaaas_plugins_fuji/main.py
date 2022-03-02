import logging

from report2sqaaas import utils as sqaaas_utils


logger = logging.getLogger('sqaaas.reporting.plugins.fuji')


class FujiValidator(sqaaas_utils.BaseValidator):
    valid = False

    def parse(self, file_name):
        return sqaaas_utils.load_json(file_name)    

    def validate(self):
        """
            We have adopted the therin defined three tiers (initial, managed, defined) but due to the different scope renamed them and included level 0 (undefined).
            These compliance levels have been adapted for the scope of F-UJI as: incomplete (0), initial (1) , moderate (2) and advanced (3).
            https://zenodo.org/record/5336159#.Yh8u2t8o9zU
        """
        logger.debug('Running SQAaaS\' <%s> validator' % self.name)
        json_res = self.parse(self.opts.stdout)
        subcriteria = []
        for principle in ['F', 'A', 'I', 'R']:
            json_res["summary"]["maturity"][principle]
            subcriteria.append({ principle + "_maturity": json_res["summary"]["maturity"][principle] })

        if len(subcriteria) > 0:
            self.valid = True

        result = {
            'valid': self.valid,            
            "id": json_res["test_id"],
            "evidence": json_res["test_id"],
            "fuji_software_version": json_res["software_version"],
            "fuji_test_timestamp": json_res["timestamp"],
            "object_identifier": json_res["request"]["normalized_object_identifier"],
            "FAIR_maturity": json_res["summary"]["maturity"]["FAIR"],
            'subcriteria': subcriteria
        }

        # print(result)

        return result