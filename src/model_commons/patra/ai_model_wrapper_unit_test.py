import unittest
import json
from patra_toolkit.patra_model_card import ModelCard
from patra_toolkit.patra_model_card import AIModel
from patra_toolkit.patra_model_card import BiasAnalysis
from patra_toolkit.patra_model_card import ExplainabilityAnalysis
from patra_toolkit.patra_model_card import Metric
from src.model_commons.patra.ai_model_wrapper import AIModelWrapper
from src.model_commons.patra.validator_unit_test import ValidModelCardDict
from src.model_commons.patra.validator_unit_test import ValidAIModelDict

class TestAIModelWrapperClass(unittest.TestCase):
	def test_ai_model_wrapper_no_init_parameters(self):
		with self.assertRaises(ValueError):
			ai_model_wrapper = AIModelWrapper()

	def test_ai_model_wrapper_bad_init_inputs_type(self):
		with self.assertRaises(TypeError):
			ai_model_wrapper = AIModelWrapper(inputs=[1.23, 2.23, 3.23])

	def test_ai_model_wrapper_bad_init_ai_model_type(self):
		with self.assertRaises(TypeError):
			ai_model_wrapper = AIModelWrapper(ai_model={"a":1,"b":2,"c":3})

	def test_ai_model_wrapper_bad_init_file_path_type(self):
		with self.assertRaises(TypeError):
			ai_model_wrapper = AIModelWrapper(file_path=123)

	def test_init_ai_model_wrapper_inputs(self):
		try:
			ai_model_wrapper = AIModelWrapper(inputs=ValidAIModelDict())
			if not hasattr(ai_model_wrapper, "ai_model"):
				self.fail("expected 'ai_model' instance variable")
		except Exception as e:
			self.fail(f"unexpected error: {e}")

	def test_init_ai_model_wrapper_ai_model(self):
		try:
			ai_model_wrapper = AIModelWrapper(ai_model = AIModel(**ValidAIModelDict()))
			if not hasattr(ai_model_wrapper, "ai_model"):
				self.fail("expected 'ai_model' instance variable")
		except Exception as e:
			self.fail(f"unexpected error: {e}")

	def test_init_ai_model_wrapper_file_path(self):
		try:
			ai_model_wrapper = AIModelWrapper(
				file_path = "src/model_commons/patra/nfl_game_score_ai_model_dict.json")
			if not hasattr(ai_model_wrapper, "ai_model"):
				self.fail("expected 'ai_model' instance variable")
		except Exception as e:
			self.fail(f"unexpected error: {e}")

	def test_ai_model_wrapper_get_ai_model(self):
		ai_model_wrapper = AIModelWrapper(file_path = 
			"src/model_commons/patra/nfl_game_score_ai_model_dict.json")
		if not isinstance(ai_model_wrapper.GetAIModel(), AIModel):
			self.fail("expected to get AIModel type")

	def test_ai_model_wrapper_add_metric_bad_key(self):
		with self.assertRaises(TypeError):
			ai_model_wrapper = AIModelWrapper(file_path =
				"src/model_commons/patra/nfl_game_score_ai_model_dict.json")
			ai_model_wrapper.AddMetric(123, "123")

	def test_ai_model_wrapper_add_metric_bad_value(self):
		with self.assertRaises(TypeError):
			ai_model_wrapper = AIModelWrapper(file_path =
				"src/model_commons/patra/nfl_game_score_ai_model_dict.json")
			ai_model_wrapper.AddMetric("mse", 170.85015487670898)


