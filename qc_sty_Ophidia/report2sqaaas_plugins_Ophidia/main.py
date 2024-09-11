# SPDX-FileCopyrightText: Copyright contributors to the Software Quality Assurance as a Service (SQAaaS) project.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from report2sqaaas import utils as sqaaas_utils
from PyOphidia import client

logger = logging.getLogger('sqaaas.reporting.plugins.Ophidia')


class OphidiaValidator(sqaaas_utils.BaseValidator):
    valid = False
    threshold = 1
    def validate(self):
        res= False
        data =sqaaas_utils.load_data(self.opts.stdout.strip())
        
        ophclient = client.Client(username="oph-user",password="oph-passwd",local_mode=True)
        res,msg= ophclient.wisvalid(data)
        print(res,msg)
        
        return({'valid':res})





