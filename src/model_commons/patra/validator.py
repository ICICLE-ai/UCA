from patra_toolkit.patra_model_card import ModelCard
from patra_toolkit.patra_model_card import AIModel
from patra_toolkit.patra_model_card import BiasAnalysis
from patra_toolkit.patra_model_card import ExplainabilityAnalysis
from patra_toolkit.patra_model_card import Metric
from huggingface_hub import ModelCard as HFModelCard
from pathlib import Path

class Validator():
	@staticmethod
	def Validate(var, expec:str, error_type=None):
		# types checked for
		types = ["ModelCard","BiasAnalysis","AIModel","ExplainabilityAnalysis","Metric",
			"str","int","list","dict","list[str]","number","list[int]","bool",
			"HFModelCard"]
		if not expec in types:
			raise ValueError(f"🛑 '{expec}' is not a supported type")
	
		# validating	
		if expec == "ModelCard":
			if not isinstance(var, ModelCard):
				Validator.ThrowTypeError(var, expec, error_type)
		if expec == "BiasAnalysis":
			if not isinstance(var, BiasAnalysis):
				Validator.ThrowTypeError(var, expec, error_type)
		if expec == "AIModel":
			if not isinstance(var, AIModel):
				Validator.ThrowTypeError(var, expec, error_type)
		if expec == "ExplainabilityAnalysis":
			if not isinstance(var, ExplainabilityAnalysis):
				Validator.ThrowTypeError(var, expec, error_type)
		if expec == "Metric":
			if not isinstance(var, Metric):
				Validator.ThrowTypeError(var, expec, error_type)
		if expec == "str":
			if not isinstance(var, str):
				Validator.ThrowTypeError(var, expec, error_type)
		if expec == "list":
			if not isinstance(var, list):
				Validator.ThrowTypeError(var, expec, error_type)
		if expec == "int":
			if not isinstance(var, int):
				Validator.ThrowTypeError(var, expec, error_type)
		if expec == "number":
			if not isinstance(var, int) and not isinstance(var, float):
				Validator.ThrowTypeError(var, expec, error_type)
		if expec == "dict":
			if not isinstance(var, dict):
				Validator.ThrowTypeError(var, expec, error_type)
		if expec == "bool":
			if not isinstance(var, bool):
				Validator.ThrowTypeError(var, expec, error_type)
		if expec == "HFModelCard":
			if not isinstance(var, HFModelCard):
				Validator.ThrowTypeError(var, expec, error_type)
		if expec == "list[str]":
			Validator.Validate(var, "list", error_type)
			for val in var:
				Validator.Validate(val, "str", error_type)
		if expec == "list[int]":
			Validator.Validate(var, "list", error_type)
			for val in var:
				Validator.Validate(val, "int", error_type)

	@staticmethod
	def ThrowTypeError(var, expec, error_type=None):
		error_message = Validator.ErrorMessage(var, expec)
		if error_type is not None:
			raise error_type(error_message)
		raise TypeError(error_message)

	@staticmethod
	def ErrorMessage(var, expec:str) -> str:
		return f"🛑 expected type '{expec}' got type '{type(var)}'"

	@staticmethod
	def ValidateMandatoryDictKeys(input_dict:dict, keys_mandatory:list):
		# validating inputs
		Validator.Validate(input_dict, "dict")
		Validator.Validate(keys_mandatory, "list")
		
		# validating inputs are not empty
		if not input_dict: raise ValueError(f"🛑 input_dict is empty")
		if not keys_mandatory: raise ValueError(f"🛑 keys_mandatory is empty")
				
		# validating every mandatory key is in the input_dict
		for key in keys_mandatory:
			if key not in input_dict.keys():
				raise ValueError(f"🛑 mandatory key {key} not present in dictionary")

	@ staticmethod
	def ValidateMandatoryKeyTypes(input_dict:dict, keys_mandatory:list, keys_mandatory_types:list):
		# validating inputs
		Validator.Validate(input_dict, "dict")
		Validator.Validate(keys_mandatory, "list")
		Validator.Validate(keys_mandatory_types, "list[str]")

		# ensuring inputs are not empty
		if not input_dict: raise ValueError(f"🛑 input_dict is empty")
		if not keys_mandatory: raise ValueError(f"🛑 keys_mandatory is empty")
		if not keys_mandatory_types: raise ValueError(f"🛑 keys_mandatory_types is empty")
		if len(keys_mandatory) != len(keys_mandatory_types):
			raise ValueError(f"🛑 keys_mandatory and keys_mandatory_types are not the"
				+ " same length")

		# validating key types
		for index in range(len(keys_mandatory)):
			Validator.Validate(input_dict[keys_mandatory[index]], keys_mandatory_types[index])

	@staticmethod
	def ValidateOptionalKeyTypes(input_dict:dict, keys_optional:list, keys_optional_types:list):
		# validate
		Validator.Validate(input_dict, "dict")
		Validator.Validate(keys_optional, "list")
		Validator.Validate(keys_optional_types, "list[str]")
		
		# ensuring inputs are not empty
		if not input_dict: raise ValueError("🛑 input_dict is empty")
		if not keys_optional: raise ValueError("🛑 keys_optional is empty")
		if not keys_optional_types: raise ValueError("🛑 keys_optional_types is empty")
		if len(keys_optional) != len(keys_optional_types):
			raise ValueError("🛑 keys_optional and keys_optional_types are not the same " + 
				"length")
		
		# validating optional key types
		for index in range(len(keys_optional)):
			if keys_optional[index] in input_dict.keys():
				Validator.Validate(input_dict[keys_optional[index]],
					keys_optional_types[index])
	
	@staticmethod
	def ValidateDict(input_dict:dict, keys_mandatory:list=[], keys_mandatory_types:list=[],
		keys_optional:list=[], keys_optional_types:list=[]):

		# validating inputs
		Validator.Validate(input_dict, "dict")
		Validator.Validate(keys_mandatory, "list")
		Validator.Validate(keys_mandatory_types, "list[str]")
		Validator.Validate(keys_optional, "list")
		Validator.Validate(keys_optional_types, "list[str]")

		# validating input_dict is not empty
		if not input_dict:
			raise ValueError(f"🛑 input_dict is empty")
		
		# validating got at least 1 correct series of inputs
		optional = keys_optional and keys_optional_types
		mandatory = keys_mandatory or (keys_mandatory and keys_mandatory_types)
		if not optional and not mandatory:
			raise ValueError(f"🛑 expected input_dict + keys_mandatory or " + 
				"input dict + keys_mandatory + keys_mandatory_types or " +
				"input dict + keys_optional + keys_optional_types")

		# validating keys_mandatory inputs
		if keys_mandatory:
			Validator.ValidateMandatoryDictKeys(input_dict, keys_mandatory)
			if keys_mandatory_types:
				Validator.ValidateMandatoryKeyTypes(input_dict, keys_mandatory,
					keys_mandatory_types)
		
		# validating optional key types
		if keys_optional and keys_optional_types:
			Validator.ValidateOptionalKeyTypes(input_dict, keys_optional,
				keys_optional_types)

	@staticmethod
	def ValidateFileExists(file_path:str):
		Validator.Validate(file_path, "str")
		if not Path(file_path).is_file():
			raise ValueError(f"🛑 expected a file at '{file_path}' but did not find 1")

	@staticmethod
	def ValidateDirectoryExists(dir_path:str):
		Validator.Validate(dir_path, "str")
		if not Path(dir_path).is_dir():
			raise ValueError(f"🛑 expected a directory at '{dir_path}' but did not find 1")
		
