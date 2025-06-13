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
			raise ValueError(f"'{expec}' is not a supported type")
	
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
		return f"expected type '{expec}' got type '{type(var)}'"


