import logging

from report2sqaaas import utils as sqaaas_utils

logger = logging.getLogger("sqaaas.reporting.plugins.fuji")


class FujiValidator(sqaaas_utils.BaseValidator):
    valid = False
    rda_useful = {
        "rda_f1_01d": "Data is identified by a persistent identifier",
        "rda_f1_01m": "Metadata is identified by a persistent identifier",
        "rda_f1_02d": "Data is identified by a globally unique identifier",
        "rda_f1_02m": "Metadata is identified by a globally unique identifier",
        "rda_f2_01m": "Rich metadata is provided to allow discovery",
        "rda_f3_01m": "Metadata includes the identifier for the data",
        "rda_f4_01m": "Metadata is offered in such a way that it can be "
        "harvested and indexed",
        "rda_a1_02d": "Data can be accessed manually (i.e. with human " "intervention)",
        "rda_a1_02m": "Metadata can be accessed manually (i.e. with human "
        "intervention)",
        "rda_a1_03d": "Data identifier resolves to a digital object",
        "rda_a1_03m": "Metadata identifier resolves to a metadata record",
        "rda_a1_04d": "Data is accessible through standardised protocol",
        "rda_a1_04m": "Metadata is accessed through standardised protocol",
        "rda_a1_1_01m": "Metadata is accessible through a free access " "protocol",
        "rda_a2_01m": "Metadata is guaranteed to remain available after data "
        "is no longer available",
        "rda_r1_01m": "Plurality of accurate and relevant attributes are "
        "provided to allow reuse",
        "da_r1_1_01m": "Metadata includes information about the licence under "
        "which the data canbe reused",
        "rda_r1_3_01d": "Data complies with a community standard",
        "rda_r1_3_01m": "Metadata complies with a community standard",
        "rda_r1_3_02m": "Metadata is expressed in compliance with a "
        "machine-understandable community standard",
    }
    rda_important = {
        "rda_a1_01m": "Metadata contains information to enable the user to "
        "get access to the data",
        "rda_a1_05d": "Data can be accessed automatically (i.e. by a computer"
        " program)",
        "rda_a1_1_01d": "Data is accessible through a free access protocol",
        "rda_i1_01d": "Data uses knowledge representation expressed in "
        "standardised format",
        "rda_i1_01m": "Metadata uses knowledge representation expressed in "
        "standardised format",
        "rda_i1_02d": "Data uses machine-understandable knowledge " "representation",
        "rda_i1_02m": "Metadata uses machine-understandable knowledge "
        "representation",
        "rda_i2_01m": "Metadata uses FAIR-compliant vocabularies",
        "rda_i3_01m": "Metadata includes references to other metadata",
        "rda_i3_03m": "Metadata includes qualified references to other " "metadata",
        "rda_r1_1_02m": "Metadata refers to a standard reuse licence",
        "rda_r1_1_03m": "Metadata refers to a machine-understandable reuse " "licence",
        "rda_r1_2_01m": "Metadata includes provenance information according "
        "to community-specific standards",
        "rda_r1_3_02d": "Data is expressed in compliance with a "
        "machine-understandable community standard",
    }
    rda_essential = {
        "rda_a1_2_01d": "Data is accessible through an access protocol that "
        "supports authentication and authorisation",
        "rda_i2_01d": "Data uses FAIR-compliant vocabularies",
        "rda_i3_01d": "Data includes references to other data",
        "rda_i3_02d": "Data includes qualified references to other data",
        "rda_i3_02m": "Metadata includes references to other data",
        "rda_i3_04m": "Metadata include qualified references to other data",
        "rda_r1_2_02m": "Metadata includes provenance information according "
        "to a cross-community language",
    }
    rda_all = {**rda_useful, **rda_important, **rda_essential}

    def parse(self, file_name):
        return sqaaas_utils.load_json(file_name)

    def validate(self):
        """

        We have adopted the therin defined three tiers (initial, managed,
        defined) but due to the different scope renamed them and included
        level 0 (undefined).
        These compliance levels have been adapted for the scope of F-UJI
        as: incomplete (0), initial (1) , moderate (2) and advanced (3).
        https://zenodo.org/record/5336159#.Yh8u2t8o9zU
        "In case at least one metric of a given principle has reached level
         ‘initial’, the corresponding principle cannot have a lower level
         even if all other metrics are scored lower thus is considered to
         have reached the ‘initial’ level. All levels above ‘initial’ are
         calculated as the rounded mean of all metrics scores for a given
         principle.
        The overall F-UJI FAIR level for a given research data object would
         analogously be calculated as a rounded mean of all principle
         scores."

        These compliance levels can be mapped to a badge as follows:
        maturity < 0.5: NO badge
        0.5 <= maturity < 1.5: BRONZE badge
        1.5 <= maturity < 2.5: SILVER badge
        maturity >= 2.5: GOLDEN badge

        FUJI does NOT use the RDA indicators that have been classified
        with a Priority level: Useful, Important, Essential.
        Neither does it use the RDA 'Measure of FAIRness' defined in 6
        levels (0,1,2,3,4,5). See: https://joinup.ec.europa.eu/sites/defaul
        t/files/solution/documentation/2020-07/FAIR%20Data%20Maturity%20Mod
        el_%20specification%20and%20guidelines_v1.00_0.pdf
        These levels meet the need for more flexible assignment of the badg
        es, by looking at "half of the indicators are satisfied".
        These six levels can (fairly) be mapped to the three badges:
        level 0 : NO badge
        Level 1 : BRONZE badge
        Level 2 or 3: SILVER badge
        Level 4 or 5: GOLDEN badge

        FAIR EVA does also not use the RDA 'Measure of FAIRness', but maps
        the Useful, Important, Essential indicators 1:1 to a badge.

        """

        logger.debug("Running SQAaaS' <%s> validator" % self.name)
        json_res = self.parse(self.opts.stdout)
        fuji_maturity = json_res["summary"]["maturity"]["FAIR"]

        if fuji_maturity < 0.5:
            logger.debug("No badge earned. FAIR level: %s" % fuji_maturity)
            passed_rd_indicators = {}
        elif fuji_maturity < 1.5:
            logger.debug("Bronze badge earned. FAIR level: %s" % fuji_maturity)
            passed_rd_indicators = self.rda_useful
        elif fuji_maturity <= 2.5:
            logger.debug("SILVER badge earned. FAIR level: %s" % fuji_maturity)
            passed_rd_indicators = {**self.rda_useful, **self.rda_important}
        else:
            logger.debug("GOLDEN badge earned. FAIR level: %s" % fuji_maturity)
            passed_rd_indicators = self.rda_all
        subcriteria = []

        for rda_criteria in self.rda_all:
            evidence = (
                "Found: "
                if passed_rd_indicators.get(rda_criteria) is not None
                else "Not found: "
            )
            subcriteria.append(
                {
                    "id": rda_criteria,
                    "valid": (passed_rd_indicators.get(rda_criteria) is not None),
                    "description": self.rda_all[rda_criteria],
                    "evidence": evidence + self.rda_all[rda_criteria],
                }
            )

        if len(subcriteria) > 0:
            self.valid = True

        result = {
            "valid": self.valid,
            "subcriteria": subcriteria,
            "standard": {
                "title": "FAIRsFAIR Data Object Assessment Metrics",
                "version": json_res["metric_version"][
                    8 : json_res["metric_version"].rfind(".")
                ],
                "url": json_res["metric_specification"],
            },
            "data_unstructured": {
                "fuji_software_version": json_res["software_version"],
                "fuji_test_timestamp": json_res["timestamp"],
                "object_identifier": json_res["request"][
                    "normalized_object_identifier"
                ],
                "fuji_maturity": json_res["summary"]["maturity"],
            },
        }

        logger.debug("Validation results: %s" % result)

        return result
