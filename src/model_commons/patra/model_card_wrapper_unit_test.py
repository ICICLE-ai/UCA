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
	
def get_model_card_wrapper() -> ModelCardWrapper:
	return ModelCardWrapper(file_path="src/model_commons/patra/nfl_game_score_model_card_dict.json")

def get_server_string() -> str:
	return "http://patraserver.pods.icicleai.tapis.io"

def get_server_string_2() -> str:
	return "https://ckn.d2i.tacc.cloud/patra/upload_mc"
