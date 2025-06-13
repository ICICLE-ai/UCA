import unittest
from patra_toolkit.patra_model_card import ModelCard
from patra_toolkit.patra_model_card import AIModel
from patra_toolkit.patra_model_card import BiasAnalysis
from patra_toolkit.patra_model_card import ExplainabilityAnalysis
from patra_toolkit.patra_model_card import Metric
from src.model_commons.patra.validator import Validator
from src.model_commons.patra.model_card_wrapper import ModelCardWrapper
from src.model_commons.patra.ai_model_wrapper import AIModelWrapper
import torch

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

	def test_number_bad_number(self):
		with self.assertRaises(TypeError):
			Validator.Validate("", "number")

	def test_number_int(self):
		try:
			Validator.Validate(123, "number")
		except Exception as e:
			self.fail(f"unexpected error: {e}")

	def test_number_float(self):
		try:
			Validator.Validate(1234.5, "number")
		except Exception as e:
			self.fail(f"unexpected error: {e}")

	def test_list_of_str_not_str(self):
		with self.assertRaises(TypeError):
			Validator.Validate(["a","b","c",5,"d"], "list[str]")

	def test_not_str(self):
		with self.assertRaises(TypeError):
			Validator.Validate(123, "str")

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

