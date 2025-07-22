import json
import unittest

import torch
from patra_toolkit.patra_model_card import ModelCard

from src.model_commons.patra.ai_model_wrapper_unit_test import generic_ai_model_wrapper
from src.model_commons.patra.model_card_wrapper import ModelCardWrapper
from src.model_commons.patra.validator_unit_test import valid_ai_model_dict, valid_model_card_dict


class TestModelCardWrapperClass(unittest.TestCase):
	def test_model_card_wrapper_no_init_parameters(self):
		with self.assertRaises(ValueError):
			_ = ModelCardWrapper()

	def test_model_card_wrapper_bad_init_inputs_type(self):
		with self.assertRaises(TypeError):
			_ = ModelCardWrapper(inputs=["a","b","c"])
	
	def test_model_card_wrapper_bad_init_model_card_type(self):
		with self.assertRaises(TypeError):
			_ = ModelCardWrapper(model_card=[1.23, 2.23, 3.23])

	def test_model_card_wrapper_bad_init_file_path_type(self):
		with self.assertRaises(TypeError):
			_ = ModelCardWrapper(file_path=[1,2,3,4])

	def test_model_card_wrapper_inputs(self):
		try:
			model_card_wrapper = ModelCardWrapper(inputs=valid_model_card_dict())
			if not hasattr(model_card_wrapper, "model_card"):
				self.fail("expected 'ai_model' instance variable")
		except Exception as e:
			self.fail(f"unexpected error: {e}")

	def test_model_card_wrapper_model_card(self):
		try:
			model_card_wrapper = ModelCardWrapper(
				model_card = ModelCard(**valid_model_card_dict()))
			if not hasattr(model_card_wrapper, "model_card"):
				self.fail("expected 'model_card' instance variable")
		except Exception:
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
		if not isinstance(model_card_wrapper.get_model_card(), ModelCard):
			self.fail("expected ModelCard type")

	def test_update_ai_model_no_parameters(self):
		model_card_wrapper = get_model_card_wrapper()
		with self.assertRaises(ValueError):
			model_card_wrapper.update_ai_model()

	def test_update_ai_model_bad_inputs(self):
		model_card_wrapper = get_model_card_wrapper()
		with self.assertRaises(TypeError):
			model_card_wrapper.update_ai_model(inputs=[1,2,3])

	def test_update_ai_model_bad_ai_model(self):
		model_card_wrapper = get_model_card_wrapper()
		with self.assertRaises(TypeError):
			model_card_wrapper.update_ai_model(ai_model={"a":"b"})

	def test_update_ai_model_bad_file_path(self):
		model_card_wrapper = get_model_card_wrapper()
		with self.assertRaises(TypeError):
			model_card_wrapper.update_ai_model(file_path=123)

	def test_update_ai_model_bad_ai_model_wrapper(self):
		model_card_wrapper = get_model_card_wrapper()
		with self.assertRaises(TypeError):
			model_card_wrapper.update_ai_model(ai_model_wrapper=123.456789)

	def test_update_ai_model_inputs(self):
		model_card_wrapper = get_model_card_wrapper()
		try:
			model_card_wrapper.update_ai_model(inputs=valid_ai_model_dict())
		except Exception as e:
			self.fail(f"unexpected error: {e}")

	def test_update_ai_model_ai_model(self):
		model_card_wrapper = get_model_card_wrapper()
		try:
			model_card_wrapper.update_ai_model(
				ai_model=generic_ai_model_wrapper().get_ai_model())
		except Exception as e:
			self.fail(f"unexpected error: {e}")

	def test_update_ai_model_file_path(self):
		model_card_wrapper = get_model_card_wrapper()
		try:
			model_card_wrapper.update_ai_model(
				file_path="src/model_commons/patra/nfl_game_score_ai_model_dict.json")
		except Exception as e:
			self.fail(f"unexpected error: {e}")

	def test_update_ai_model_ai_model_wrapper(self):
		model_card_wrapper = get_model_card_wrapper()
		try:
			model_card_wrapper.update_ai_model(ai_model_wrapper=generic_ai_model_wrapper())
		except Exception as e:
			self.fail(f"unexpected error: {e}")

	def test_update_model_structure_no_ai_model(self):
		model_card_wrapper = get_model_card_wrapper()
		model = torch.load("src/model_commons/patra/nfl_game_score.pth", weights_only=False)
		with self.assertRaises(ValueError):
			model_card_wrapper.update_model_structure(model)

	def test_update_model_structure(self):
		model_card_wrapper = get_model_card_wrapper()
		model = torch.load("src/model_commons/patra/nfl_game_score.pth", weights_only=False)
		model_card_wrapper.update_ai_model(
			file_path="src/model_commons/patra/nfl_game_score_ai_model_dict.json")
		try:
			model_card_wrapper.update_model_structure(model)
		except Exception as e:
			self.fail(f"unexpected error: {e}")

	def test_write_model_to_patra_server_bad_patra_server_url(self):
		model_card_wrapper = get_model_card_wrapper()
		with self.assertRaises(TypeError):
			model_card_wrapper.write_model_to_patra_server(123)

	def test_write_model_to_patra_server_bad_token(self):
		model_card_wrapper = get_model_card_wrapper()
		with self.assertRaises(TypeError):
			model_card_wrapper.write_model_to_patra_server(get_server_string(), token=[1,2,3])

	def test_write_model_to_patra_server_only_patra_server_url(self):
		model_card_wrapper = get_model_card_wrapper()
		model_card_wrapper.update_ai_model(ai_model_wrapper=generic_ai_model_wrapper())
		model = torch.load("src/model_commons/patra/nfl_game_score.pth", weights_only=False)
		model_card_wrapper.update_model_structure(model)
		try:
			response_dict = model_card_wrapper.write_model_to_patra_server(
				get_server_string_2())
			print(type(response_dict))
			for value in response_dict:
				print(value)
		except Exception as e:
			self.fail(f"unexpected error: {e}")

	def test_write_model_to_file_bad_file_location(self):
		model_card_wrapper = get_model_card_wrapper()
		with self.assertRaises(TypeError):
			model_card_wrapper.write_to_file(file_location={"a":1,"b":2})

	def test_write_model_to_file(self):
		model_card_wrapper = get_model_card_wrapper()
		model_card_wrapper.update_ai_model(ai_model_wrapper=generic_ai_model_wrapper())
		model = torch.load("src/model_commons/patra/nfl_game_score.pth", weights_only=False)
		model_card_wrapper.update_model_structure(model)
		try:
			model_card_wrapper.write_to_file(file_location=
				"src/model_commons/patra/nfl_game_score_model_card_write_test.json")
		except Exception as e:
			self.fail(f"unexpected error: {e}")

	def test_get_name(self):
		pmc_wrapper = get_model_card_with_ai_model()
		try:
			self.assertEqual(pmc_wrapper.get_name(), json_field(MODEL_CARD_JSON, "name"))
		except Exception as e:
			self.fail(f"❌ unexpected exception {e}")

	def test_get_version(self):
		pmc_wrapper = get_model_card_with_ai_model()
		try:
			self.assertEqual(pmc_wrapper.get_version(),json_field(MODEL_CARD_JSON, "version"))
		except Exception as e:
			self.fail(f"❌ unexpected exception: {e}")

	def test_get_short_description(self):
		pmc_wrapper = get_model_card_with_ai_model()
		try:
			self.assertEqual(pmc_wrapper.get_short_description(),
				json_field(MODEL_CARD_JSON, "short_description"))
		except Exception as e:
			self.fail(f"❌ unexpected exception: {e}")

	def test_get_full_description(self):
		pmc_wrapper = get_model_card_with_ai_model()
		try:
			self.assertEqual(pmc_wrapper.get_full_description(),
				json_field(MODEL_CARD_JSON, "full_description"))
		except Exception as e:
			self.fail(f"❌ unexpected exception: {e}")

	def test_get_keywords(self):
		pmc_wrapper = get_model_card_with_ai_model()
		try:
			self.assertEqual(pmc_wrapper.get_keywords(),
				json_field(MODEL_CARD_JSON, "keywords"))
		except Exception as e:
			self.fail(f"❌ unexpected exception: {e}")

	def test_get_author(self):
		pmc_wrapper = get_model_card_with_ai_model()
		try:
			self.assertEqual(pmc_wrapper.get_author(),
				json_field(MODEL_CARD_JSON, "author"))
		except Exception as e:
			self.fail(f"❌ unexpected exception: {e}")
	
	def test_get_input_type(self):
		pmc_wrapper = get_model_card_with_ai_model()
		try:
			self.assertEqual(pmc_wrapper.get_input_type(),
				json_field(MODEL_CARD_JSON, "input_type"))
		except Exception as e:
			self.fail(f"❌ unexpected exception: {e}")

	def test_get_category(self):
		pmc_wrapper = get_model_card_with_ai_model()
		try:
			self.assertEqual(pmc_wrapper.get_category(),
				json_field(MODEL_CARD_JSON, "category"))
		except Exception as e:
			self.fial(f"❌ unexpected exception: {e}")

	def test_get_input_data(self):
		wrapper = get_model_card_with_ai_model()
		try:
			self.assertEqual(wrapper.get_input_data(),
				json_field(MODEL_CARD_JSON, "input_data"))
		except Exception as e:
			self.fail(f"❌ unexpected exception: {e}")

	def test_get_output_data(self):
		wrapper = get_model_card_with_ai_model()
		try:
			self.assertEqual(wrapper.get_output_data(),
				json_field(MODEL_CARD_JSON, "output_data"))
		except Exception as e:
			self.fail(f"❌ unexpected exception: {e}")

	def test_get_foundational_model(self):
		wrapper = get_model_card_with_ai_model()
		try:
			self.assertEqual(wrapper.get_foundational_model(),
				json_field(MODEL_CARD_JSON, "foundational_model"))
		except Exception as e:
			self.fail(f"❌ unexpected exception: {e}")

	def test_get_documentation(self):
		wrapper = get_model_card_with_ai_model()
		try:
			self.assertEqual(wrapper.get_documentation(),
				json_field(MODEL_CARD_JSON, "documentation"))
		except Exception as e:
			self.fail(f"❌ unexpected exception: {e}")

	def test_get_ai_model_name(self):
		wrapper = get_model_card_with_ai_model()
		try:
			self.assertEqual(wrapper.get_ai_model_name(),
				json_field(AI_MODEL_CARD_JSON, "name"))
		except Exception:
			self.fail("❌ unexpected exception: {e}")

	def test_get_ai_model_version(self):
		wrapper = get_model_card_with_ai_model()
		try:
			self.assertEqual(wrapper.get_ai_model_version(),
				json_field(AI_MODEL_CARD_JSON, "version"))
		except Exception as e:
			self.fail(f"❌ unexpected exception: {e}")

	def test_get_ai_model_description(self):
		wrapper = get_model_card_with_ai_model()
		try:
			self.assertEqual(wrapper.get_ai_model_description(),
				json_field(AI_MODEL_CARD_JSON, "description"))
		except Exception as e:
			self.fail(f"❌ unexpected exception: {e}")

	def test_get_ai_model_owner(self):
		wrapper = get_model_card_with_ai_model()
		try:
			self.assertEqual(wrapper.get_ai_model_owner(),
				json_field(AI_MODEL_CARD_JSON, "owner"))
		except Exception as e:
			self.fail(f"❌ unexpected exception: {e}")

	def test_get_ai_model_location(self):
		wrapper = get_model_card_with_ai_model()
		try:
			self.assertEqual(wrapper.get_ai_model_location(),
				json_field(AI_MODEL_CARD_JSON, "location"))
		except Exception as e:
			self.fail(f"❌ unexpected exception: {e}")

	def test_get_ai_model_license(self):
		wrapper = get_model_card_with_ai_model()
		try:
			self.assertEqual(wrapper.get_ai_model_license(),
				json_field(AI_MODEL_CARD_JSON, "license"))
		except Exception as e:
			self.fail(f"❌ unexpected exception: {e}")

	def test_get_ai_model_framework(self):
		wrapper = get_model_card_with_ai_model()
		try:
			self.assertEqual(wrapper.get_ai_model_framework(),
				json_field(AI_MODEL_CARD_JSON, "framework"))
		except Exception as e:
			self.fail(f"❌ unexpected exception: {e}")

	def test_get_ai_model_model_type(self):
		wrapper = get_model_card_with_ai_model()
		try:
			self.assertEqual(wrapper.get_ai_model_model_type(),
				json_field(AI_MODEL_CARD_JSON, "model_type"))
		except Exception as e:
			self.fail(f"❌ unexpected exception: {e}")

	def test_get_ai_model_test_accuracy(self):
		wrapper = get_model_card_with_ai_model()
		try:
			self.assertEqual(wrapper.get_ai_model_test_accuracy(),
				json_field(AI_MODEL_CARD_JSON, "test_accuracy"))
		except Exception as e:
			self.fail(f"❌ unexpected exception: {e}")

	def test_get_ai_model_metrics(self):
		wrapper = get_model_card_with_ai_model()
		metrics = {"Optimizer":"Adam", "mae":10.20810866355896}
		wrapper.update_ai_model_metrics(metrics=metrics)
		self.assertEqual(wrapper.get_ai_model_metrics(), metrics)

	def test_update_ai_model_metrics_no_params(self):
		wrapper = get_model_card_with_ai_model()
		with self.assertRaises(ValueError):
			wrapper.update_ai_model_metrics()

	def test_update_ai_model_metrics_only_key(self):
		wrapper = get_model_card_with_ai_model()
		with self.assertRaises(ValueError):
			wrapper.update_ai_model_metrics(key="test")

	def test_update_ai_model_metrics_only_value(self):
		wrapper = get_model_card_with_ai_model()
		with self.assertRaises(ValueError):
			wrapper.update_ai_model_metrics(value="test")

	def test_update_ai_model_metrics_model_card_not_set(self):
		with open(MODEL_CARD_JSON, "r") as file:
			wrapper = ModelCardWrapper(inputs=json.load(file))
		with self.assertRaises(ValueError):
			wrapper.update_ai_model_metrics(key="test", value="test")

	def test_update_ai_metrics_bad_metrics_type(self):
		wrapper = get_model_card_with_ai_model()
		with self.assertRaises(TypeError):
			metrics = [1233,56774]
			wrapper.update_ai_model_metrics(metrics=metrics)
	
	def test_update_ai_metrics_bad_key_type(self):
		wrapper = get_model_card_with_ai_model()
		with self.assertRaises(TypeError):
			wrapper.update_ai_model_metrics(key=12445.6, value="good")

	def test_update_ai_model_metrics_pass_metrics(self):
		wrapper = get_model_card_with_ai_model()
		try:
			metrics = {"test":"test"}
			wrapper.update_ai_model_metrics(metrics=metrics)
			self.assertEqual(wrapper.get_ai_model_metrics(), metrics)
		except Exception as e:
			self.fail(f"❌ unexpected exception: {e}")

	def test_update_ai_model_metrics_pass_key_value(self):
		wrapper = get_model_card_with_ai_model()
		try:
			wrapper.update_ai_model_metrics(key="test", value="test_value")
			self.assertEqual(wrapper.get_ai_model_metrics(), {"test":"test_value"})
		except Exception as e:
			self.fail(f"❌ unexpected exception: {e}")

MODEL_CARD_JSON = "src/model_commons/patra/nfl_game_score_model_card_dict.json"

AI_MODEL_CARD_JSON = "src/model_commons/patra/nfl_game_score_ai_model_dict.json"

def get_model_card_wrapper() -> ModelCardWrapper:
	return ModelCardWrapper(file_path = MODEL_CARD_JSON)

def json_field(file_path:str, field:str) -> str:
	with open(file_path, "r") as file:
		data = json.load(file)
		if field in data.keys():
			return data[field]
		return None

def get_model_card_with_ai_model() -> ModelCardWrapper:
	pmc_wrapper = get_model_card_wrapper()
	pmc_wrapper.update_ai_model(ai_model_wrapper=generic_ai_model_wrapper())
	return pmc_wrapper

def get_server_string() -> str:
	return "http://patraserver.pods.icicleai.tapis.io"

def get_server_string_2() -> str:
	return "https://ckn.d2i.tacc.cloud/patra/upload_mc"
