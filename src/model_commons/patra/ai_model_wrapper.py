import json

from patra_toolkit.patra_model_card import AIModel

from src.model_commons.patra.validator import Validator


class AIModelWrapper():
	def __init__(self, inputs:dict | None = None, ai_model:AIModel=None, file_path:str=""):
		# raise error if no parameters are given
		if not inputs and not ai_model and not file_path:
			raise ValueError("no parameters were given")
		# creating ai_model parameter
		if ai_model:
			Validator.validate(ai_model, "AIModel")
			self.ai_model = ai_model
		elif inputs:
			Validator.validate(inputs, "dict")
			self.ai_model = AIModel(**inputs)
		elif file_path:
			Validator.validate(file_path, "str")
			with open(file_path, "r") as file:
				self.ai_model = AIModel(**json.load(file))

	def get_ai_model(self) -> AIModel:
		return self.ai_model

	def update_name(self, name:str):
		Validator.validate(name, "str")
		self.ai_model.name = name

	def update_version(self, version:str):
		Validator.validate(version, "str")
		self.ai_model.version = version

	def update_description(self, description:str):
		Validator.validate(description, "str")
		self.ai_model.description = description

	def update_owner(self, owner:str):
		Validator.validate(owner, "str")
		self.ai_model.owner = owner

	def update_location(self, location:str):
		Validator.validate(location, "str")
		self.ai_model.location = location

	def update_license(self, license:str):
		Validator.validate(license, "str")
		self.ai_model.license = license

	def update_framework(self, framework:str):
		Validator.validate(framework, "str")
		self.ai_model.framework = framework

	def update_model_type(self, model_type:str):
		Validator.validate(model_type, "str")
		self.ai_model.model_type = model_type

	def update_test_accuracy(self, test_accuracy:float):
		Validator.validate(test_accuracy, "number")
		self.ai_model.test_accuracy = test_accuracy

	def update_model_structure(self, model_structure):
		Validator.validate(model_structure, "dict")
		self.ai_model.model_structure = model_structure

	def update_metrics(self, metrics:dict | None = None, key:str="", value:str=""):
		if not metrics and (not key or not value):
			raise ValueError("expecting either metrics or key and value")
		if metrics:
			Validator.validate(metrics, "dict")
			self.ai_model.metrics = metrics
		else:
			self.add_metric(key, value)

	def add_metric(self, key:str, value:str):
		Validator.validate(key, "str")
		Validator.validate(value, "str")
		self.ai_model.add_metric(key, value)

	def populate_model_structure(self, trained_model):
		self.ai_model.populate_model_structure(trained_model)	
