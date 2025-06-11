import unittest
from patra_toolkit.patra_model_card import ModelCard
from patra_toolkit.patra_model_card import AIModel
from patra_toolkit.patra_model_card import BiasAnalysis
from patra_toolkit.patra_model_card import ExplainabilityAnalysis
from patra_toolkit.patra_model_card import Metric
from src.model_commons.patra.validator import Validator
from src.model_commons.patra.model_card_wrapper import ModelCardWrapper
from src.model_commons.patra.ai_model_wrapper import AIModelWrapper

class TestValidatorClass(unittest.TestCase):
	def test_error_message(self):
		s1 = Validator.ErrorMessage("123", "int")
		s2 = "expected type 'int' got type '<class 'str'>'"
		self.assertEquals(s1, s2)

	def test_not_supported_type(self):
		with self.assertRaises(ValueError):
			Validator.Validate("123", "test")

	def test_model_card_correct(self):
		try:
			mc = ModelCardWrapper(inputs=ValidModelCardDict()).GetModelCard()
			Validator.Validate(mc,"ModelCard")
		except Exception as e:
			self.fail(f"unexpected exception: {e}")

	def test_model_card_wrong(self):
		with self.assertRaises(TypeError):
			Validator.Validate("123", "ModelCard")

	def test_bias_analysis_correct(self):
		try:
			Validator.Validate(BiasAnalysis(**ValidBiasAnalysisDict()), "BiasAnalysis")
		except Exception as e:
			self.fail(f"unexpected exception {e}")

	def test_bias_analysis_wrong(self):
		with self.assertRaises(TypeError):
			Validator.Validate(123.4, "BiasAnalysis")

	def test_ai_model_correct(self):
		try:
			ai_model = AIModelWrapper(inputs=ValidAIModelDict()).GetAIModel()
			Validator.Validate(ai_model, "AIModel")
		except Exception as e:
			self.fail(f"unexpected exception: {e}")

	def test_ai_model_wrong(self):
		with self.assertRaises(TypeError):
			Validator.Validate([], "AIModel")

	def test_explainability_analysis_correct(self):
		try:
			Validator.Validate(ExplainabilityAnalysis(**ValidExplainabilityAnalysisDict()),
				"ExplainabilityAnalysis")
		except Exception as e:
			self.fail(f"unexpected exception: {e}")

	def test_explainability_analysis_wrong(self):
		with self.assertRaises(TypeError):
			Validator.Validate({}, "ExplainabilityAnalysis")

	def test_metric_correct(self):
		try:
			Validator.Validate(Metric(**ValidMetricDict()), "Metric")
		except Exception as e:
			self.fail(f"unexpected exception: {e}")

	def test_metric_wrong(self):
		with self.assertRaises(TypeError):
			Validator.Validate(1, "Metric")

	def test_str_correct(self):
		try:
			Validator.Validate("string", "str")
		except Exception as e:
			self.fail(f"unexpected error: {e}")

	def test_str_wrong(self):
		with self.assertRaises(TypeError):
			Validator.Validate(1.23, "str")

	def test_list_correct(self):
		try:
			Validator.Validate([1,2,3], "list")
		except Exception as e:
			self.fail(f"unexpected error: {e}")

	def test_list_wrong(self):
		with self.assertRaises(TypeError):
			Validator.Validate({}, "list")

	def test_int_correct(self):
		try:
			Validator.Validate(1, "int")
		except Exception as e:
			self.fail(f"unexpected error: {e}")

	def test_int_wrong(self):
		with self.assertRaises(TypeError):
			Validator.Validate(1.234, "int")

	def test_dict_correct(self):
		try:
			Validator.Validate({"a":"b"}, "dict")
		except Exception as e:
			self.fail(f"unexpected error: {e}")

	def test_dict_wrong(self):
		with self.assertRaises(TypeError):
			Validator.Validate([], "dict")

	def test_list_of_str_correct(self):
		try:
			Validator.Validate(["a","b","c"], "list[str]")
		except Exception as e:
			self.fail(f"unexpected error: {e}")

	def test_list_of_str_not_list(self):
		with self.assertRaises(TypeError):
			Validator.Validate({}, "list[str]")

	def test_list_of_str_not_str(self):
		with self.assertRaises(TypeError):
			Validator.Validate(["a","b","c",5,"d"], "list[str]")

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
				file_path = "src/patra/nfl_game_score_model_card_dict.json")
			if not hasattr(model_card_wrapper, "model_card"):
				self.fail("expected 'model_card' instance variable")
		except Exception as e:
			self.fail(f"unexpected error: {e}")

	def test_model_card_wrapper_get_model_card(self):
		model_card_wrapper = ModelCardWrapper(
			file_path="src/patra/nfl_game_score_model_card_dict.json")
		if not isinstance(model_card_wrapper.GetModelCard(), ModelCard):
			self.fail(f"expected ModelCard type")

def ValidModelCardDict() -> dict:
	return {
		"name":"game_score",
		"version":"1.0",
		"short_description":"model to predict nfl game score",
		"full_description":"mlp model to predict nfl game score",
		"keywords":"nfl, nas, hill climb",
		"author":"nick cliffel",
		"input_type":"tabular",
		"category":"real-life",
		"input_data":"team averages",
		"output_data":"home team points - away team points",
		"foundational_model":"None",
	}

def ValidAIModelDict() -> dict:
	return {
		"name":"game_score_mlp",
		"version":"1.0",
		"description":"model to predict nfl game score",
		"owner":"Nick Cliffel",
		"location":"file path",
		"license":"MIT",
		"framework":"pytorch",
		"model_type":"MLP",
		"test_accuracy":"10.08",
		"model_structure":"afuigihug",
		"metrics":"abs"
	}

def ValidMetricDict() -> dict:
	return {
		"key":"abs",
		"value":"1.3456"
	}

def ValidExplainabilityAnalysisDict() -> dict:
	return {
		"name":"valid dict",
		"metrics":[Metric(**ValidMetricDict())]
	}

def ValidBiasAnalysisDict() -> dict:
	return {
		"demographic_parity_difference":12.34,
		"equal_odds_difference":12.34
	}

