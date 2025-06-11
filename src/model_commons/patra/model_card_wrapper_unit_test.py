import unittest
from patra_toolkit.patra_model_card import ModelCard
from patra_toolkit.patra_model_card import AIModel
from patra_toolkit.patra_model_card import BiasAnalysis
from patra_toolkit.patra_model_card import ExplainabilityAnalysis
from patra_toolkit.patra_model_card import Metric
from src.model_commons.patra.validator import Validator
from src.model_commons.patra.model_card_wrapper import ModelCardWrapper
from src.model_commons.patra.ai_model_wrapper import AIModelWrapper
from src.model_commons.patra.validator_unit_test import ValidModelCardDict
from src.model_commons.patra.validator_unit_test import ValidAIModelDict
from src.model_commons.patra.validator_unit_test import ValidMetricDict
from src.model_commons.patra.validator_unit_test import ValidExplainabilityAnalysisDict
from src.model_commons.patra.validator_unit_test import ValidBiasAnalysisDict

class TestModelCardWrapperClass(unittest.TestCase):
	def test_model_card_wrapper_no_init_parameters(self):
		with self.assertRaises(ValueError):
			model_card_wrapper = ModelCardWrapper()

	def test_model_card_wrapper_bad_init_inputs_type(self):
		with self.assertRaises(TypeError):
			model_card_wrapper = ModelCardWrapper(inputs=["a","b","c"])
	
	def test_model_card_wrapper_bad_init_model_card_type(self):
		with self.assertRaises(TypeError):
			model_card_wrapper = ModelCardWrapper(model_card=[1.23, 2.23, 3.23])

	def test_model_card_wrapper_bad_init_file_path_type(self):
		with self.assertRaises(TypeError):
			model_card_wrapper = ModelCardWrapper(file_path=[1,2,3,4])

	def test_model_card_wrapper_inputs(self):
		try:
			model_card_wrapper = ModelCardWrapper(inputs=ValidModelCardDict())
			if not hasattr(model_card_wrapper, "model_card"):
				self.fail("expected 'ai_model' instance variable")
		except Exception as e:
			self.fail(f"unexpected error: {e}")

	def test_model_card_wrapper_model_card(self):
		try:
			model_card_wrapper = ModelCardWrapper(
				model_card = ModelCard(**ValidModelCardDict()))
			if not hasattr(model_card_wrapper, "model_card"):
				self.fail("expected 'model_card' instance variable")
		except Exception as e:
			self.fail("unexpected error: {e}")

	def test_model_card_wrapper_file_path(self):
		try:
			model_card_wrapper = ModelCardWrapper(
				file_path = "src/model_commons/patra/nfl_game_score_model_card_dict.json")
			if not hasattr(model_card_wrapper, "model_card"):
				self.fail("expected 'model_card' instance variable")
		except Exception as e:
			self.fail(f"unexpected error: {e}")

	def test_model_card_wrapper_get_model_card(self):
		model_card_wrapper = ModelCardWrapper(
			file_path="src/model_commons/patra/nfl_game_score_model_card_dict.json")
		if not isinstance(model_card_wrapper.GetModelCard(), ModelCard):
			self.fail(f"expected ModelCard type")


