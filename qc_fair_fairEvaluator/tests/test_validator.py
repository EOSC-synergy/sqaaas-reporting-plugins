import pytest
from types import SimpleNamespace

from report2sqaaas_plugins_fairEvaluator.main import fairEvaluatorValidator


@pytest.fixture
def fairEvaluator_stdout():
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
         "indicator":"rda_a1_01m"
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
         "indicator":"rda_f1_01d"
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
         "indicator":"rda_i1_01d"
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
         "indicator":"rda_r1_01m"
      },
      "result":{
         "points":17.5,
         "color":"#E74C3C"
      }
   }
}
    """


@pytest.fixture
def validator_opts(fairEvaluator_stdout):
    class_args = {
        'validator': 'fairEvaluator',
        'stdout': fairEvaluator_stdout
    }
    return SimpleNamespace(**class_args)


@pytest.fixture
def validator(validator_opts):
    return fairEvaluatorValidator(validator_opts)


@pytest.mark.dependency()
def test_is_validate_method_defined(validator_opts):
    assert fairEvaluatorValidator(validator_opts).validate()


@pytest.mark.dependency(depends=["test_is_validate_method_defined"])
def test_validate_method_output(validator):
    result = validator.validate()
    assert type(result) is dict
    assert 'valid' in list(result)
    assert 'subcriteria' in list(result)
    assert type(result['subcriteria']) is list
    
