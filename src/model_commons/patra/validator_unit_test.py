import unittest

from huggingface_hub import ModelCard as HFModelCard
from patra_toolkit.patra_model_card import BiasAnalysis, ExplainabilityAnalysis, Metric

from src.model_commons.hugging_face.hugging import Hugging
from src.model_commons.patra.ai_model_wrapper import AIModelWrapper
from src.model_commons.patra.model_card_wrapper import ModelCardWrapper
from src.model_commons.patra.validator import Validator


class TestValidatorClass(unittest.TestCase):
	def test_error_message(self):
		s1 = Validator.error_message("123", "int")
		s2 = "🛑 expected type 'int' got type '<class 'str'>'"
		self.assertEquals(s1, s2)

	def test_not_supported_type(self):
		with self.assertRaises(ValueError):
			Validator.validate("123", "test")

	def test_model_card_correct(self):
		try:
			mc = ModelCardWrapper(inputs=valid_model_card_dict()).get_model_card()
			Validator.validate(mc,"ModelCard")
		except Exception as e:
			self.fail(f"❌ unexpected exception: {e}")

	def test_hf_model_card_wrong(self):
		with self.assertRaises(TypeError):
			Validator.validate(1345.6, "HFModelCard")
	
	def test_hf_model_card_pass(self):
		try:
			Validator.validate(get_hf_model_card(), "HFModelCard")
		except Exception as e:
			self.fail(f"❌ unexpected exception: {e}")

	def test_model_card_wrong(self):
		with self.assertRaises(TypeError):
			Validator.validate("123", "ModelCard")

	def test_bias_analysis_correct(self):
		try:
			Validator.validate(BiasAnalysis(**valid_bias_analysis_dict()), "BiasAnalysis")
		except Exception as e:
			self.fail(f"❌ unexpected exception {e}")

	def test_bias_analysis_wrong(self):
		with self.assertRaises(TypeError):
			Validator.validate(123.4, "BiasAnalysis")

	def test_ai_model_correct(self):
		try:
			ai_model = AIModelWrapper(inputs=valid_ai_model_dict()).get_ai_model()
			Validator.validate(ai_model, "AIModel")
		except Exception as e:
			self.fail(f"❌ unexpected exception: {e}")

	def test_ai_model_wrong(self):
		with self.assertRaises(TypeError):
			Validator.validate([], "AIModel")

	def test_explainability_analysis_correct(self):
		try:
			Validator.validate(ExplainabilityAnalysis(**valid_explainability_analysis_dict()),
				"ExplainabilityAnalysis")
		except Exception as e:
			self.fail(f"❌ unexpected exception: {e}")

	def test_explainability_analysis_wrong(self):
		with self.assertRaises(TypeError):
			Validator.validate({}, "ExplainabilityAnalysis")

	def test_metric_correct(self):
		try:
			Validator.validate(Metric(**valid_metric_dict()), "Metric")
		except Exception as e:
			self.fail(f"❌ unexpected exception: {e}")

	def test_metric_wrong(self):
		with self.assertRaises(TypeError):
			Validator.validate(1, "Metric")

	def test_str_correct(self):
		try:
			Validator.validate("string", "str")
		except Exception as e:
			self.fail(f"❌ unexpected error: {e}")
	
	def test_valdate_bool_wrong(self):
		with self.assertRaises(TypeError):
			Validator.validate("1324", "bool")

	def test_validate_bool_true_correct(self):
		try:
			Validator.validate(True, "bool")
		except Exception as e:
			self.fail(f"❌ unexpected error: {e}")

	def test_validate_bool_false_correct(self):
		try:
			Validator.validate(False, "bool")
		except Exception as e:
			self.fail(f"❌ unexpected error: {e}")

	def test_str_wrong(self):
		with self.assertRaises(TypeError):
			Validator.validate(1.23, "str")

	def test_list_correct(self):
		try:
			Validator.validate([1,2,3], "list")
		except Exception as e:
			self.fail(f"❌ unexpected error: {e}")

	def test_list_wrong(self):
		with self.assertRaises(TypeError):
			Validator.validate({}, "list")

	def test_int_correct(self):
		try:
			Validator.validate(1, "int")
		except Exception as e:
			self.fail(f"❌ unexpected error: {e}")

	def test_int_wrong(self):
		with self.assertRaises(TypeError):
			Validator.validate(1.234, "int")

	def test_dict_correct(self):
		try:
			Validator.validate({"a":"b"}, "dict")
		except Exception as e:
			self.fail(f"❌ unexpected error: {e}")

	def test_dict_wrong(self):
		with self.assertRaises(TypeError):
			Validator.validate([], "dict")

	def test_list_of_str_correct(self):
		try:
			Validator.validate(["a","b","c"], "list[str]")
		except Exception as e:
			self.fail(f"❌ unexpected error: {e}")

	def test_list_of_str_not_list(self):
		with self.assertRaises(TypeError):
			Validator.validate({}, "list[str]")

	def test_number_bad_number(self):
		with self.assertRaises(TypeError):
			Validator.validate("", "number")

	def test_number_int(self):
		try:
			Validator.validate(123, "number")
		except Exception as e:
			self.fail(f"❌ unexpected error: {e}")

	def test_number_float(self):
		try:
			Validator.validate(1234.5, "number")
		except Exception as e:
			self.fail(f"❌ unexpected error: {e}")

	def test_list_of_str_not_str(self):
		with self.assertRaises(TypeError):
			Validator.validate(["a","b","c",5,"d"], "list[str]")

	def test_not_str(self):
		with self.assertRaises(TypeError):
			Validator.validate(123, "str")

	def test_validate_dict_input_dict_wrong_type(self):
		with self.assertRaises(TypeError):
			Validator.validate_dict(input_dict=123, keys_mandatory=["a"])

	def test_validate_dict_keys_mandatory_wrong_type(self):
		with self.assertRaises(TypeError):
			Validator.validate_dict(input_dict={"a":"b"}, keys_mandatory="1234")

	def test_validate_dict_bad_wrong_keys_mandatory_types_type(self):
		with self.assertRaises(TypeError):
			Validator.validate_dict(input_dict={"a":"b"}, keys_manatory=["a","b"],
				keys_mandatory_types=1234)

	def test_validate_dict_wrong_keys_optional_type(self):
		with self.assertRaises(TypeError):
			Validator.validate_dict(input_dict={"a":"b"}, keys_optional=1234.5,
				keys_optional_types=["str", "str"])

	def test_validate_dict_empty_input_dict(self):
		with self.assertRaises(ValueError):
			Validator.validate_dict(input_dict={}, keys_mandatory=["a","b"])

	def test_validate_dict_no_params(self):
		with self.assertRaises(ValueError):
			Validator.validate_dict(input_dict={"a":"b"})

	def test_validate_dict_only_keys_optional_types(self):
		with self.assertRaises(ValueError):
			Validator.validate_dict(input_dict={"a":1}, keys_mandatory_types=["str","str"])

	def test_validate_dict_only_keys_optional(self):
		with self.assertRaises(ValueError):
			Validator.validate_dict(input_dict={"a":1}, keys_optional=["a","b"])

	def test_validate_dict_only_keys_optional_types_two(self):
		with self.assertRaises(ValueError):
			Validator.validate_dict(input_dict={"a":1}, keys_optional_types=["str","str"])

	def test_validate_dict_missing_mandatory_key(self):
		keys = ["a","b","c","d","e"]
		working = {}
		for index in range(len(keys)):
			working[keys[index]] = index
		keys.append("f")
		with self.assertRaises(ValueError):
			Validator.validate_dict(input_dict=working, keys_mandatory=keys)

	def test_validate_dict_mandatory_keys(self):
		keys = ["a","b","c","d","e"]
		working = {}
		for index in range(len(keys)):
			working[keys[index]] = index
		try:
			Validator.validate_dict(input_dict=working, keys_mandatory=keys)
		except Exception as e:
			self.fail(f"❌ got unexpected exception {e}")

	def test_validate_dict_keys_mandatory_and_keys_mandatory_types_length_mismatch(self):
		types = ["int","int","int","int"]
		keys = ["a","b","c","d","e"]
		working = {}
		for index in range(len(keys)):
			working[keys[index]] = index
		with self.assertRaises(ValueError):
			Validator.validate_dict(input_dict=working, keys_mandatory=keys,
				keys_mandatory_types=types)

	def test_validate_dict_bad_keys_mandatory_types(self):
		types = ["int","int","int","str"]
		keys = ["a","b","c","d"]
		working = {}
		for index in range(len(keys)):
			working[keys[index]] = index
		with self.assertRaises(TypeError):
			Validator.validate_dict(input_dict=working, keys_mandatory=keys,
				keys_mandatory_types=types)

	def test_validate_dict_mandatory_key_types(self):
		types = ["str","str","str","str","str","str","str","str","str","str","str"]
		keys = ["name","version","short_description","full_description","keywords",
			"author","input_type","category","input_data","output_data",
			"foundational_model"]
		print(f"types length: {len(types)}")
		print(f"keys length: {len(keys)}")
		try:
			Validator.validate_dict(input_dict=valid_model_card_dict(), keys_mandatory=keys,
				keys_mandatory_types=types)
		except Exception as e:
			self.fail(f"❌ got unexpected exception: {e}")

	def test_validate_dict_bad_optional_key_types(self):
		opt_keys = ["b","c"]
		opt_types = ["int", "str"]
		working = {"a":1,"b":2,"c":3,"d":4}
		with self.assertRaises(TypeError):
			Validator.validate_dict(input_dict=working, keys_optional=opt_keys,
				keys_optional_types=opt_types)

	def test_validate_dict_optional_key_types(self):
		opt_keys = ["c","d","e"]
		opt_types = ["int", "str", "list"]
		working = {
			"a":5,
			"b":90.1,
			"c":5000,
			"d":"test str",
			"e":[1,2,34]
		}
		try:
			Validator.validate_dict(input_dict=working, keys_optional=opt_keys,
				keys_optional_types=opt_types)
		except Exception as e:
			self.fail(f"❌ got unexpected exception: {e}")

	def test_validate_dict_optional_unequal_lengths(self):
		opt_keys=["a","b","c"]
		opt_types=["int","int","int","int"]
		working = {"a":1,"b":2,"c":3,"d":4}
		with self.assertRaises(ValueError):
			Validator.validate_dict(input_dict=working, keys_optional=opt_keys,
				keys_optional_types=opt_types)

	def test_validate_dict_mandatory_and_opt_keys(self):
		opt_keys = ["a","b","c"]
		man_keys = ["k","l","m","n"]
		working = {}
		for index in range(len(man_keys)):
			working[man_keys[index]] = index
		for index in range(len(opt_keys)):
			working[opt_keys[index]] = index + 10
		with self.assertRaises(ValueError):
			Validator.validate_dict(input_dict=working, keys_optional=opt_keys)

	def test_validate_dict_mandatory_and_opt_types(self):
		opt_key_types = ["int","int","int","int"]
		man_keys = ["k","l","m","n"]
		working = {}
		for index in range(len(man_keys)):
			working[man_keys[index]] = index
		with self.assertRaises(ValueError):
			Validator.validate_dict(input_dict=working, keys_optional_types=opt_key_types)

	def test_validate_dict_everything_together_missing_mandatory(self):
		man_keys = ["name","version","short_description"]
		man_types = ["str","str","str"]
		opt_keys = ["full_description","keywords","author","input_type","category","input_data",
			"output_data","foundational_model"]
		opt_types = ["str","str","str","str","str","str","str","str"]
		working = valid_model_card_dict()
		del working["short_description"]
		with self.assertRaises(ValueError):
			Validator.validate_dict(input_dict=working, keys_mandatory=man_keys,
				keys_mandatory_types=man_types, keys_optional=opt_keys,
				keys_optional_types=opt_types)

	def test_validate_dict_everything_together_wrong_mandatory_type(self):
		man_keys = ["name","version","short_description"]
		man_types = ["str","int","str"]
		opt_keys = ["full_description","keywords","author","input_type","category","input_data",
			"output_data","foundational_model"]
		opt_types = ["str","str","str","str","str","str","str","str"]
		working = valid_model_card_dict()
		working["version"] = 2
		working["short_description"] = 4
		with self.assertRaises(TypeError):
			Validator.validate_dict(input_dict=working, keys_mandatory=man_keys,
				keys_mandatory_types=man_types, keys_optional=opt_keys,
				keys_optional_types=opt_types)

	def test_validate_mandatory_dict_keys_wrong_input_dict_type(self):
		man_keys = ["name","version","short_description"]
		with self.assertRaises(TypeError):
			Validator.validate_mandatory_dict_keys(input_dict=[1,2,3,4],
				keys_mandatory=man_keys)

	def test_validate_mandatory_dict_keys_wrong_keys_mandatory_type(self):
		man_keys = {"a":1,"b":2,"c":3}
		with self.assertRaises(TypeError):
			Validator.validate_mandatory_dict_keys(input_dict={"a":1,"b":2},
				keys_mandatory=man_keys)

	def test_validate_mandatory_dict_keys_empty_input_dict(self):
		man_keys = ["name","version","short_description"]
		with self.assertRaises(ValueError):
			Validator.validate_mandatory_dict_keys(input_dict={},
				keys_mandatory=man_keys)

	def test_validate_mandatory_dict_keys_empty_mandatory_keys(self):
		with self.assertRaises(ValueError):
			Validator.validate_mandatory_dict_keys(input_dict={"a":1,"b":2,"c":3},
				keys_mandatory=[])

	def test_validate_mandatory_dict_keys_pass(self):
		try:
			man_keys = ["name","author","input_data"]
			Validator.validate_mandatory_dict_keys(input_dict=valid_model_card_dict(),
				keys_mandatory=man_keys)
		except Exception as e:
			self.fail(f"❌ unexpected exception: {e}")

	def test_validate_mandatory_dict_keys_fail(self):
		man_keys = ["full_description","author","category"]
		input_dict = valid_model_card_dict()
		del input_dict["author"]
		with self.assertRaises(ValueError):
			Validator.validate_mandatory_dict_keys(input_dict=input_dict,
				keys_mandatory=man_keys)

	def test_validate_mandatory_key_types_wrong_input_dict_type(self):
		man_keys = ["name","author","input_data"]
		man_types = ["str","str","str"]
		with self.assertRaises(TypeError):
			Validator.validate_mandatory_key_types(input_dict=[1,2,3],
				keys_mandatory=man_keys, keys_mandatory_types=man_types)

	def test_validate_mandatory_key_types_wrong_keys_mandatory_type(self):
		man_types = ["str","str","str"]
		with self.assertRaises(TypeError):
			Validator.validate_mandatory_key_types(input_dict=valid_model_card_dict(),
				keys_mandatory=1234.5, keys_mandatory_types=man_types)

	def test_validate_mandatory_key_types_wrong_keys_mandatory_types_type(self):
		man_keys = ["name","author","input_data"]
		with self.assertRaises(TypeError):
			Validator.validate_mandatory_key_types(input_dict=valid_model_card_dict(),
				keys_mandatory=man_keys, keys_mandatory_types={"a":1,"b":2})

	def test_validate_mandatory_key_types_empty_input_dict(self):
		man_keys = ["name","author","input_data"]
		man_types = ["str","str","str"]
		with self.assertRaises(ValueError):
			Validator.validate_mandatory_key_types(input_dict={},
				keys_mandatory=man_keys, keys_mandatory_types=man_types)

	def test_validate_mandatory_key_types_empty_keys_mandatory(self):
		man_types = ["str","str","str"]
		with self.assertRaises(ValueError):
			Validator.validate_mandatory_key_types(input_dict=valid_model_card_dict(),
				keys_mandatory=[], keys_mandatory_types=man_types)

	def test_validate_mandatory_key_types_empty_keys_mandatory_types(self):
		man_keys = ["name","author","input_data"]
		with self.assertRaises(ValueError):
			Validator.validate_mandatory_key_types(input_dict=valid_model_card_dict(),
				keys_mandatory=man_keys, keys_mandatory_types=[])

	def test_validate_mandatory_key_types_mismatch_lengths(self):
		man_keys = ["name","author","input_data"]
		man_types = ["str","str","str","str"]
		with self.assertRaises(ValueError):
			Validator.validate_mandatory_key_types(input_dict=valid_model_card_dict(),
				keys_mandatory=man_keys, keys_mandatory_types=man_types)

	def test_validate_mandatory_key_types_pass(self):
		man_keys = ["name","version","output_data"]
		man_types = ["str","int","list[int]"]
		working = valid_model_card_dict()
		working["version"] = 5
		working["output_data"] = [1,2,3,10,15]
		try:
			Validator.validate_mandatory_key_types(input_dict=working,
				keys_mandatory=man_keys, keys_mandatory_types=man_types)
		except Exception as e:
			self.fail(f"unexpected exception: {e}")

	def test_validate_mandatory_key_types_fail(self):
		man_keys = ["name","version","output_data"]
		man_types = ["str","list","str"]
		with self.assertRaises(TypeError):
			Validator.validate_mandatory_key_types(input_dict=valid_model_card_dict(),
				keys_mandatory=man_keys, keys_mandatory_types=man_types)

	def test_validate_optional_key_types_wrong_input_dict_type(self):
		opt_keys=["short_description"]
		opt_types=["str"]
		with self.assertRaises(TypeError):
			Validator.validate_optional_key_types(input_dict=[],
				keys_optional=opt_keys, keys_optional_types=opt_types)

	def test_validate_optional_key_types_wrong_keys_optional_type(self):
		opt_keys = 12345.678
		opt_types = ["int"]
		with self.assertRaises(TypeError):
			Validator.validate_optional_key_types(input_dict=valid_model_card_dict(),
				keys_optional=opt_keys, keys_optional_types=opt_types)

	def test_validate_optional_key_types_wrong_keys_optional_types_type(self):
		opt_keys = ["name","version"]
		opt_types = {"str":1,"int":2}
		with self.assertRaises(TypeError):
			Validator.validate_optional_key_types(input_dict=valid_model_card_dict(),
				keys_optional=opt_keys, keys_optional_types=opt_types)

	def test_validate_optional_key_types_empty_input_dict(self):
		opt_keys=["name","version"]
		opt_types=["str","str"]
		with self.assertRaises(ValueError):
			Validator.validate_optional_key_types(input_dict={},
				keys_optional=opt_keys, keys_optional_types=opt_types)

	def test_validate_optional_key_types_empty_keys_optional(self):
		opt_types=["str","str"]
		with self.assertRaises(ValueError):
			Validator.validate_optional_key_types(input_dict=valid_model_card_dict(),
				keys_optional=[], keys_optional_types=opt_types)

	def test_validate_optional_key_types_empty_keys_optional_types(self):
		opt_keys=["name","version"]
		with self.assertRaises(ValueError):
			Validator.validate_optional_key_types(input_dict=valid_model_card_dict(),
				keys_optional=opt_keys, keys_optional_types=[])

	def test_validate_optional_key_types_unequal_lengths(self):
		opt_keys=["name","version"]
		opt_types=["str","str","int"]
		with self.assertRaises(ValueError):
			Validator.validate_optional_key_types(input_dict=valid_model_card_dict(),
				keys_optional=opt_keys, keys_optional_types=opt_types)
	
	def test_validate_optional_key_types_pass(self):
		working = valid_model_card_dict()
		working["version"] = 3
		opt_keys = ["name","version","career"]
		opt_types = ["str","int","str"]
		try:
			Validator.validate_optional_key_types(input_dict=working,
				keys_optional=opt_keys, keys_optional_types=opt_types)
		except Exception as e:
			self.fail(f"unexpected exception: {e}")

	def test_validate_optional_key_types_fail(self):
		working = valid_model_card_dict()
		working["version"] = 5
		opt_keys = ["name","version"]
		opt_types = ["str", "str"]
		with self.assertRaises(TypeError):
			Validator.validate_optional_key_types(inputDict=working,
				keys_optional=opt_keys, keys_optional_types=opt_types)

	def test_validate_file_exists_bad_file_path_type(self):
		with self.assertRaises(TypeError):
			Validator.validate_file_exists(file_path={"a":1,"b":2})

	def test_validate_file_exists_pass(self):
		try:
			Validator.validate_file_exists("src/model_commons/hugging_face/test_file.txt")
		except Exception as e:
			self.fail(f"❌ receivied unexpected exception: {e}")

	def test_validate_file_exists_bad(self):
		with self.assertRaises(ValueError):
			Validator.validate_file_exists("src/model_commons/hugging_face")

	def test_validate_directory_bad_dir_path_type(self):
		with self.assertRaises(TypeError):
			Validator.validate_directory_exists(1234.5678)

	def test_validate_directory_exists_pass(self):
		try:
			Validator.validate_directory_exists("src/model_commons/hugging_face")
		except Exception as e:
			self.fail(f"❌ receivied unexpected exception: {e}")

	def test_validate_directory_exists_bad(self):
		with self.assertRaises(ValueError):
			Validator.validate_directory_exists("src/model_commons/hugging_face/test_file.txt")

def valid_model_card_dict() -> dict:
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

def valid_ai_model_dict() -> dict:
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

def valid_metric_dict() -> dict:
	return {
		"key":"abs",
		"value":"1.3456"
	}

def valid_explainability_analysis_dict() -> dict:
	return {
		"name":"valid dict",
		"metrics":[Metric(**valid_metric_dict())]
	}

def valid_bias_analysis_dict() -> dict:
	return {
		"demographic_parity_difference":12.34,
		"equal_odds_difference":12.34
	}

def public_repo_id() -> str:
	return "NickCliffel/PublicUCATestRepo"

def get_hf_model_card() -> HFModelCard:
	return Hugging.get_model_card(repo_id=public_repo_id())
