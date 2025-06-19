from patra_toolkit.patra_model_card import ModelCard
from patra_toolkit.patra_model_card import AIModel
from patra_toolkit.patra_model_card import BiasAnalysis
from patra_toolkit.patra_model_card import ExplainabilityAnalysis
from patra_toolkit.patra_model_card import Metric

class Validator():
	@staticmethod
	def Validate(var, expec:str):
		# types checked for
		types = ["ModelCard","BiasAnalysis","AIModel","ExplainabilityAnalysis","Metric",
			"str","int","list","dict","list[str]","number"]
		if not expec in types:
			raise ValueError(f"🛑 '{expec}' is not a supported type")
	
		# validating	
		if expec == "ModelCard":
			if not isinstance(var, ModelCard):
				raise TypeError(Validator.ErrorMessage(var, expec))
		if expec == "BiasAnalysis":
			if not isinstance(var, BiasAnalysis):
				raise TypeError(Validator.ErrorMessage(var, expec))
		if expec == "AIModel":
			if not isinstance(var, AIModel):
				raise TypeError(Validator.ErrorMessage(var, expec))
		if expec == "ExplainabilityAnalysis":
			if not isinstance(var, ExplainabilityAnalysis):
				raise TypeError(Validator.ErrorMessage(var, expec))
		if expec == "Metric":
			if not isinstance(var, Metric):
				raise TypeError(Validator.ErrorMessage(var, expec))
		if expec == "str":
			if not isinstance(var, str):
				raise TypeError(Validator.ErrorMessage(var, expec))
		if expec == "list":
			if not isinstance(var, list):
				raise TypeError(Validator.ErrorMessage(var, expec))
		if expec == "int":
			if not isinstance(var, int):
				raise TypeError(Validator.ErrorMessage(var, expec))
		if expec == "number":
			if not isinstance(var, int) and not isinstance(var, float):
				raise TypeError(Validator.ErrorMessage(var, expec))
		if expec == "dict":
			if not isinstance(var, dict):
				raise TypeError(Validator.ErrorMessage(var, expec))
		if expec == "list[str]":
			Validator.Validate(var, "list")
			for val in var:
				Validator.Validate(val, "str")

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
