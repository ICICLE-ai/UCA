from patra_toolkit.patra_model_card import ModelCard
from patra_toolkit.patra_model_card import AIModel
from patra_toolkit.patra_model_card import BiasAnalysis
from patra_toolkit.patra_model_card import ExplainabilityAnalysis
from patra_toolkit.patra_model_card import Metric
from src.patra.validator import Validator
from src.patra.ai_model_wrapper import AIModelWrapper
import json

class ModelCardWrapper():
	
	def __init__(self, inputs:dict={}, model_card:ModelCard=None, file_path:str=""):
		# raise error if no parameters are given
		if not inputs and not model_card and not file_path:
			raise ValueError("no parameters were given")
		
		# creating class model_card parameter
		if model_card:
			Validator.Validate(model_card, "ModelCard")
			self.model_card = model_card
		elif inputs:
			Validator.Validate(inputs, "dict")
			self.model_card = ModelCard(**inputs)
		elif file_path:
			Validator.Validate(file_path, "str")
			with open(file_path, "r") as file:
				self.model_card = ModelCard(**json.load(file_path))

	def GetModelCard(self) -> ModelCard:
		return self.model_card

	def UpdateAIModel(self, inputs:dict={}, ai_model:AIModel=None, file_path:str=""):
		# raise error if no parameters are given
		if not inputs and not ai_model and not file_path:
			raise ValueError("no parameters were given")
		
		# updating AIModel
		self.model_card.ai_model = AIModelWrapper(inputs=inputs, ai_model=ai_model,
			file_path=file_path).GetAIModel()
	
		# updating AIModel
		if aiModel:
			Validator.Validate(ai_model, "AIModel")
			self.model_card.ai_model = ai_model
		elif inputs:
			Validator.Validate(inputs, "dict")
			self.model_card.ai_model = AIModel(**AIModel)
		elif file_path:
			Validator.Validate(file_path, "str")
			with open(file_path, "r") as file:
				self.model_card.ai_model = AIModel(**json.load(file_path))

	def UpdateBiasAnalysis(self, inputs:dict={}, bias_analysis:BiasAnalysis=None, file_path:str=""):
		# raise error if no parameters are given
		if not inputs and not bias_analysis and not file_path:
			raise ValueError("no parameters were given")
		
		# updating BiasAnalysis
		if bias_analysis:
			Validator.Validate(bias_analysis, "BiasAnalysis")
			self.model_card.bias_analysis = bias_analysis
		elif inputs:
			Validator.Validate(inputs, "dict")
			self.model_card.bias_analysis = BiasAnalysis(**inputs)
		elif file_path:
			Validator.Validate(inputs, "str")
			with open(file_path, "r") as file:
				self.model_card.bias_analysis = BiasAnalysis(**json.load(file))

	def UpdateXaiAnalysis(self, inputs:dict={}, xia_analysis:ExplainabilityAnalysis=None,
		file_path:str=""):

		# raise error if no parameters are given
		if not inputs and not xia_analysis and not file_path:
			raise ValueError("no parameters were given")

		# updating ExplainabilityAnalysis
		if xia_analysis:
			Validator.Validate(xia_analysis, "ExplainabilityAnalysis")
			self.model_card.xia_analysis = xia_analysis
		elif inputs:
			Validator.Validate(inputs, "dict")
			self.model_card.xia_analysis = ExplainabilityAnalysis(**inputs)
		elif file_path:
			Validator.Validate(inputs, "str")
			with open(file_path, "r") as file:
				self.model_card.xia_analysis = ExplainabilityAnalysis(**json.load(file))

	def UpdateName(self, name:str):
		Validator.Validate(name, "str")
		self.model_card.name = name

	def UpdateVersion(self, version:str):
		Validator.Validate(version, "str")
		self.model_card.version = version

	def UpdateShortDescription(self, short_description:str):
		Validator.Validate(short_description, "str")
		self.model_card.short_description = short_description

	def UpdateFullDescription(self, full_description:str):
		Validator.Validate(full_description, "str")
		self.model_card.full_description = full_description

	def UpdateKeywords(self, keywords:str):
		Validator.Validate(keywords, "str")
		self.model_card.keywords = keywords

	def UpdateAuthor(self, author:str):
		Validator.Validate(author, "str")
		self.model_card.author = author

	def UpdateInputType(self, input_type:str):
		Validator.Validate(input_type, "str")
		self.model_card.input_type = input_type

	def UpdateCategory(self, category:str):
		Validator.Validate(category, "str")
		self.model_card.category = category

	def UpdateInputData(self, input_data:str):
		Validator.Validate(input_data, "str")
		self.model_card.input_data = input_data

	def UpdateOutputData(self, output_data:str):
		Validator.Validate(output_data, "str")
		self.model_card.output_data = output_data

	def UpdateFoundationalModel(self, foundational_model:str):
		Validator.Validate(foundational_model, "str")
		self.model_card.foundational_model = foundational_model

	def UpdateModelRequirements(self, model_requirements:list[str]):
		Validator.Validate(model_requirements, "list[str]")
		self.model_card.model_requirements = model_requirements

	def PopulateRequirements(self):
		self.model_card.populate_requirements()

	def PopulateBias(self, dataset, true_labels:list, predicted_labels:list,
		sensitive_feature_name:str, sensitive_feature_data:list, model):
		
		# validating inputs
		Validator.Validate(true_labels, "list")
		Validator.Validate(predicted_labels, "list")
		Validator.Validate(sensitive_feature_name, "str")
		Validator.Validate(sensitive_feature_data, "list")

		# populating bias
		self.model_card.populate_bias(dataset=dataset,
			true_labels=true_labels,
			predicted_labels=predicted_labels,
			sensitive_feature_name=sensitive_feature_name,
			sensitive_feature_data=sensitive_feature_data,
			model=model)

	def PopulateXai(self, train_dataset, column_names:list, model, n_features:int=None):
		# validating inputs
		Validator.Validate(column_names, "list")
		if n_features:
			Validator.Validate(n_features, "int")
		
		# populating xia
		if n_features:
			self.model_card.populate_xai(train_dataset=train_dataset,
				column_names=column_names,
				model=model,
				n_features=n_features)
		else:
			self.model_card.populate_xai(train_dataset=train_dataset,
				column_names=column_names,
				model=model)

	def WriteToFile(self, file_location:str):
		# validating inputs
		Validator.Validate(file_location, "str")
		# validating model card before saving
		self.model_card.validate()
		# writing to file
		self.model_card.save(file_location)

	def WriteModelToPatraServer(self, patra_server_url:str, token:str=None) -> dict:
		# validating model card before submitting to server
		self.model_card.validate()
		# submitting model card to server
		if token:
			# used for non public servers
			return self.model_card.submit(patra_server_url=patra_server_url,
				token=token)
		else:
			# used for public servers
			return self.model_card.submit(patra_server_url=patra_server_url)
