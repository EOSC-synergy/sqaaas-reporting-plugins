import pytest
from types import SimpleNamespace

from report2sqaaas_plugins_fairEva.main import fairEva


@pytest.fixture
def fairEva_stdout():
    return """
    {
   "accessible":{
      "rda_a1_01m":{
         "points":0,
         "score":{
            "earned":0,
            "total":100,
            "weight":2
         },
         "test_status":"fail",
         "name":"rda_a1_01m",
         "msg":"rda_a1_01m"
      }
   },
   "findable":{
      "rda_f1_01d":{
         "points":100,
         "score":{
            "earned":100,
            "total":100,
            "weight":3
         },
         "test_status":"pass",
         "name":"rda_f1_01d",
         "msg":"rda_f1_01d"
      }
   },
   "interoperable":{
      "rda_i1_01d":{
         "points":0,
         "score":{
            "earned":0,
            "total":100,
            "weight":2
         },
         "test_status":"fail",
         "name":"rda_i1_01d",
         "msg":"rda_i1_01d"
      }
   },
   "reusable":{
      "rda_r1_01m":{
         "points":40.0,
         "score":{
            "earned":40.0,
            "total":100,
            "weight":3
         },
         "test_status":"fail",
         "name":"rda_r1_01m",
         "msg":"rda_r1_01m"
      },
      "result":{
         "points":17.5,
         "color":"#E74C3C"
      }
   }
}
    """


@pytest.fixture
def validator_opts(fairEva_stdout):
    class_args = {
        'validator': 'fairEva',
        'stdout': fairEva_stdout
    }
    return SimpleNamespace(**class_args)


@pytest.fixture
def validator(validator_opts):
    return fairEva(validator_opts)


@pytest.mark.dependency()
def test_is_validate_method_defined(validator_opts):
    assert fairEva(validator_opts).validate()


@pytest.mark.dependency(depends=["test_is_validate_method_defined"])
def test_validate_method_output(validator):
    result = validator.validate()
    assert type(result) is dict
    assert 'valid' in list(result)
    assert 'subcriteria' in list(result)
    assert type(result['subcriteria']) is list
