import unittest
import json
import torch
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

	def test_ai_model_wrapper_add_metric(self):
		ai_model_wrapper = AIModelWrapper(file_path = 
			"src/model_commons/patra/nfl_game_score_ai_model_dict.json")
		ai_model_wrapper.AddMetric("mse", "170.85015487670898")
		ai_model = ai_model_wrapper.GetAIModel()
		if not "mse" in ai_model.metrics or ai_model.metrics["mse"] != "170.85015487670898":
			self.fail("either metric wasn't there or it is not correct")

	def test_ai_model_wrapper_update_test_accuracy_bad_value(self):
		ai_model_wrapper = GenericAIModelWrapper()
		with self.assertRaises(TypeError):
			ai_model_wrapper.UpdateTestAccuracy([])

	def test_ai_model_wrapper_update_test_accuracy_float(self):
		ai_model_wrapper = GenericAIModelWrapper()
		try:
			ai_model_wrapper.UpdateTestAccuracy(1234.5)
			if ai_model_wrapper.GetAIModel().test_accuracy != 1234.5:
				self.fail(f"expected 1234.5")
		except Exception as e:
			self.fail(f"unexpected error: {e}")

	def test_ai_model_wrapper_update_metrics_no_params(self):
		ai_model_wrapper = GenericAIModelWrapper()
		with self.assertRaises(ValueError):
			ai_model_wrapper.UpdateMetrics()

	def test_ai_model_wrapper_update_metrics_only_key(self):
		ai_model_wrapper = GenericAIModelWrapper()
		with self.assertRaises(ValueError):
			ai_model_wrapper.UpdateMetrics(key="mse")

	def test_ai_model_wrapper_update_metrics_only_value(self):
		ai_model_wrapper = GenericAIModelWrapper()
		with self.assertRaises(ValueError):
			ai_model_wrapper.UpdateMetrics(value="190.0")

	def test_ai_model_wrapper_update_metrics_metrics(self):
		ai_model_wrapper = GenericAIModelWrapper()
		ai_model_wrapper.UpdateMetrics(metrics=GenericMetricsDict())
		ai_model = ai_model_wrapper.GetAIModel()
		metrics = ai_model.metrics
		if not ("mse" in metrics and "r2" in metrics and "abs" in metrics and "rmse" in metrics):
			self.fail("metrics weren't there or a metric wasn't included")

	def test_ai_model_wrapper_update_key_value(self):
		ai_model_wrapper = GenericAIModelWrapper()
		ai_model_wrapper.AddMetric("mse", "170.85015487670898")
		ai_model_wrapper.UpdateMetrics(key="mse", value="190.0")
		ai_model = ai_model_wrapper.GetAIModel()
		if not "mse" in ai_model.metrics or ai_model.metrics["mse"] != "190.0":
			self.fail("either metric wasn't there or it is not correct")

	def test_ai_model_wrapper_populate_model_structure(self):
		try:
			ai_model_wrapper = GenericAIModelWrapper()
			model = torch.load("src/model_commons/patra/nfl_game_score.pth",
				weights_only=False)
			ai_model_wrapper.PopulateModelStructure(model)
		except Exception as e:
			self.fail(f"received unexpected error: {e}")

	def test_ai_model_wrapper_update_name_bad(self):
		ai_model_wrapper = GenericAIModelWrapper()
		with self.assertRaises(TypeError):
			ai_model_wrapper.UpdateName({})

	def test_ai_model_wrapper_update_name(self):
		ai_model_wrapper = GenericAIModelWrapper()
		try:
			ai_model_wrapper.UpdateName("new name")
			if ai_model_wrapper.GetAIModel().name != "new name":
				self.fail(f"received unexpected name")
		except Exception as e:
			self.fail(f"unexpected error: {e}")

	def test_ai_model_update_version_bad(self):
		ai_model_wrapper = GenericAIModelWrapper()
		with self.assertRaises(TypeError):
			ai_model_wrapper.UpdateVersion([])

	def test_ai_model_update_version(self):
		ai_model_wrapper = GenericAIModelWrapper()
		try:
			ai_model_wrapper.UpdateVersion("new version")
			if ai_model_wrapper.GetAIModel().version != "new version":
				self.fail(f"received unexpected version")
		except Exception as e:
			self.fail(f"unexpected error: {e}")

	def test_ai_model_update_description_bad(self):
		ai_model_wrapper = GenericAIModelWrapper()
		with self.assertRaises(TypeError):
			ai_model_wrapper.UpdateDescription(1234)

	def test_ai_model_update_description(self):
		ai_model_wrapper = GenericAIModelWrapper()
		try:
			ai_model_wrapper.UpdateDescription("new description")
			if ai_model_wrapper.GetAIModel().description != "new description":
				self.fail("received an unexpected description")
		except Exception as e:
			self.fail(f"unexpected error {e}")

	def test_ai_model_update_owner_bad(self):
		ai_model_wrapper = GenericAIModelWrapper()
		with self.assertRaises(TypeError):
			ai_model_wrapper.UpdateOwner(1234.5)

	def test_ai_model_update_owner(self):
		ai_model_wrapper = GenericAIModelWrapper()
		try:
			ai_model_wrapper.UpdateOwner("new owner")
			if ai_model_wrapper.GetAIModel().owner != "new owner":
				self.fail("received an unexpected owner")
		except Exception as e:
			self.fail("unexpected error: {e}")

	def test_ai_model_update_location_bad(self):
		ai_model_wrapper = GenericAIModelWrapper()
		with self.assertRaises(TypeError):
			ai_model_wrapper.UpdateLocation({})

	def test_ai_model_update_location(self):
		ai_model_wrapper = GenericAIModelWrapper()
		try:
			ai_model_wrapper.UpdateLocation("new loc")
			if ai_model_wrapper.GetAIModel().location != "new loc":
				self.fail("received an unexpected location")
		except Exception as e:
			self.fail("unexpected error: {e}")

	def test_ai_model_update_license_bad(self):
		ai_model_wrapper = GenericAIModelWrapper()
		with self.assertRaises(TypeError):
			ai_model_wrapper.UpdateLicense([])

	def test_ai_model_update_license(self):
		ai_model_wrapper = GenericAIModelWrapper()
		try:
			ai_model_wrapper.UpdateLicense("new license")
			if ai_model_wrapper.GetAIModel().license != "new license":
				self.fail("received an unexpected license")
		except Exception as e:
			self.fail("unexpected error: {e}")
	
	def test_ai_model_update_framework_bad(self):
		ai_model_wrapper = GenericAIModelWrapper()
		with self.assertRaises(TypeError):
			ai_model_wrapper.UpdateFramework(1234.5)

	def test_ai_model_update_framework(self):
		ai_model_wrapper = GenericAIModelWrapper()
		try:
			ai_model_wrapper.UpdateFramework("tensorflow")
			if ai_model_wrapper.GetAIModel().framework != "tensorflow":
				self.fail("received an unexpected framework")
		except Exception as e:
			self.fail("unexpected error: {e}")

	def test_ai_model_update_model_type_bad(self):
		ai_model_wrapper = GenericAIModelWrapper()
		with self.assertRaises(TypeError):
			ai_model_wrapper.UpdateModelType({})

	def test_ai_model_update_model_type(self):
		ai_model_wrapper = GenericAIModelWrapper()
		try:
			ai_model_wrapper.UpdateModelType("model type")
			if ai_model_wrapper.GetAIModel().model_type != "model type":
				self.fail("received an unexpected framework")
		except:
			self.fail("unexpected error: {e}")

def GenericAIModelWrapper() -> AIModelWrapper:
	return AIModelWrapper(file_path = "src/model_commons/patra/nfl_game_score_ai_model_dict.json")

def GenericMetricsDict() -> dict:
	with open("src/model_commons/patra/nfl_game_score.json", "r") as file:
		return json.load(file)
