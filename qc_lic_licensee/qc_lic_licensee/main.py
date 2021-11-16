class BaseValidator(object):
    def validate(self):
        return NotImplementedError


class LicenseeValidator(BaseValidator):
    def validate(self):
        print('Running LicenseeValidator..')
