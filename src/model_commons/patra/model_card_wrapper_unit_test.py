import unittest
import torch
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
from src.model_commons.patra.ai_model_wrapper_unit_test import GenericAIModelWrapper

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

	def test_update_ai_model_no_parameters(self):
		model_card_wrapper = GetModelCardWrapper()
		with self.assertRaises(ValueError):
			model_card_wrapper.UpdateAIModel()

	def test_update_ai_model_bad_inputs(self):
		model_card_wrapper = GetModelCardWrapper()
		with self.assertRaises(TypeError):
			model_card_wrapper.UpdateAIModel(inputs=[1,2,3])

	def test_update_ai_model_bad_ai_model(self):
		model_card_wrapper = GetModelCardWrapper()
		with self.assertRaises(TypeError):
			model_card_wrapper.UpdateAIModel(ai_model={"a":"b"})

	def test_update_ai_model_bad_file_path(self):
		model_card_wrapper = GetModelCardWrapper()
		with self.assertRaises(TypeError):
			model_card_wrapper.UpdateAIModel(file_path=123)

	def test_update_ai_model_bad_ai_model_wrapper(self):
		model_card_wrapper = GetModelCardWrapper()
		with self.assertRaises(TypeError):
			model_card_wrapper.UpdateAIModel(ai_model_wrapper=123.456789)

	def test_update_ai_model_inputs(self):
		model_card_wrapper = GetModelCardWrapper()
		try:
			model_card_wrapper.UpdateAIModel(inputs=ValidAIModelDict())
		except Exception as e:
			self.fail(f"unexpected error: {e}")

	def test_update_ai_model_ai_model(self):
		model_card_wrapper = GetModelCardWrapper()
		try:
			model_card_wrapper.UpdateAIModel(ai_model = GenericAIModelWrapper().GetAIModel())
		except Exception as e:
			self.fail(f"unexpected error: {e}")

	def test_update_ai_model_file_path(self):
		model_card_wrapper = GetModelCardWrapper()
		try:
			model_card_wrapper.UpdateAIModel(
				file_path="src/model_commons/patra/nfl_game_score_ai_model_dict.json")
		except Exception as e:
			self.fail(f"unexpected error: {e}")

	def test_update_ai_model_ai_model_wrapper(self):
		model_card_wrapper = GetModelCardWrapper()
		try:
			model_card_wrapper.UpdateAIModel(ai_model_wrapper=GenericAIModelWrapper())
		except Exception as e:
			self.fail(f"unexpected error: {e}")

	def test_update_model_structure_no_ai_model(self):
		model_card_wrapper = GetModelCardWrapper()
		model = torch.load("src/model_commons/patra/nfl_game_score.pth", weights_only=False)
		with self.assertRaises(ValueError):
			model_card_wrapper.UpdateModelStructure(model)

	def test_update_model_structure(self):
		model_card_wrapper = GetModelCardWrapper()
		model = torch.load("src/model_commons/patra/nfl_game_score.pth", weights_only=False)
		model_card_wrapper.UpdateAIModel(
			file_path="src/model_commons/patra/nfl_game_score_ai_model_dict.json")
		try:
			model_card_wrapper.UpdateModelStructure(model)
		except Exception as e:
			self.fail(f"unexpected error: {e}")


def GetModelCardWrapper():
	return ModelCardWrapper(file_path="src/model_commons/patra/nfl_game_score_model_card_dict.json")
