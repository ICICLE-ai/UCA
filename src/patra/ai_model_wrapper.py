from patra_toolkit.patra_model_card import AIModel
from src.patra.validator import Validator

class AIModelWrapper():
	def __init__(self, inputs:dict={}, ai_model:AIModel=None, file_path:str=""):
		# raise error if no parameters are given
		if not inputs and not ai_model and not file_path:
			raise ValueError("no parameters were given")
		# creating ai_model parameter
		if ai_model:
			Validator.Validate(ai_model, "AIModel")
			self.ai_model = ai_model
		elif inputs:
			Validator.Validate(inputs, "dict")
			self.ai_model = AIModel(**inputs)
		elif file_path:
			Validator.Validate(inputs, "str")
			with open(file_path, "r") as file:
				self.ai_model = AIModel(**json.load(file_path))

	def GetAIModel(self) -> AIModel:
		return self.ai_model

	def UpdateName(self, name:str):
		Validator.Validate(name, "str")
		self.ai_model.name = name

	def UpdateVersion(self, version:str):
		Validator.Validate(version, "str")
		self.ai_model.version = version

	def UpdateDescription(self, description:str):
		Validator.Validate(description, "str")
		self.ai_model.description = description

	def UpdateOwner(self, owner:str):
		Validator.Validate(owner, "str")
		self.ai_model.owner = owner

	def UpdateLocation(self, location:str):
		Validator.Validate(location, "str")
		self.ai_model.location = location

	def UpdateLicense(self, license:str):
		Validator.Validate(license, "str")
		self.ai_model.license = license

	def UpdateFramework(self, framework:str):
		Validator.Validate(framework, "str")
		self.ai_model.framework = framework

	def UpdateModelType(self, model_type:str):
		Validator.Validate(model_type, "str")
		self.ai_model.model_type = model_type

	def UpdateTestAccuracy(self, test_accuracy:str):
		Validator.Validate(model_type, "str")
		self.ai_model.test_accuracy = test_accuracy

	def UpdateModelStructure(self, model_structure):
		Validator.Validate(model_structure, "dict")
		self.ai_model.model_structure = model_structure

	def UpdateMetrics(self, metrics:dict):
		Validator.Validate(metrics, "dict")
		self.ai_model.metrics = metrics

	def AddMetric(self, key:str, value:str):
		Validator.Validate(key, "str")
		Validator.Validate(value, "str")
		self.ai_model.add_metric(key, value)

	def PopulateModelStructure(self, trained_model):
		self.ai_model.populate_model_structure(trained_model)	
