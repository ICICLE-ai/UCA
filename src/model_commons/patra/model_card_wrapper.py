import json

from patra_toolkit.patra_model_card import AIModel, BiasAnalysis, ExplainabilityAnalysis, ModelCard

from src.model_commons.patra.ai_model_wrapper import AIModelWrapper
from src.model_commons.patra.validator import Validator


class ModelCardWrapper():
	
	def __init__(self, inputs:dict | None = None, model_card: ModelCard | None =None,
		file_path:str=""):
		
		# raise error if no parameters are given
		if not inputs and not model_card and not file_path:
			raise ValueError("no parameters were given")
		
		# creating class model_card parameter
		if model_card:
			Validator.validate(model_card, "ModelCard")
			self.model_card = model_card
		elif inputs:
			Validator.validate(inputs, "dict")
			self.model_card = ModelCard(**inputs)
		elif file_path:
			Validator.validate(file_path, "str")
			with open(file_path, "r") as file:
				self.model_card = ModelCard(**json.load(file))

	def get_model_card(self) -> ModelCard:
		return self.model_card

	def update_ai_model(self, inputs:dict | None = None, ai_model:AIModel | None = None,
		file_path:str="", ai_model_wrapper:AIModelWrapper | None = None):
		
		# raise error if no parameters are given
		if not inputs and not ai_model and not file_path and not ai_model_wrapper:
			raise ValueError("no parameters were given")
		
		if ai_model_wrapper:
			if not isinstance(ai_model_wrapper, AIModelWrapper):
				raise TypeError("expected AIModelWrapper type")
			self.model_card.ai_model = ai_model_wrapper.get_ai_model()
			return
		
		# updating ai_model
		self.model_card.ai_model = AIModelWrapper(inputs=inputs, ai_model=ai_model,
			file_path=file_path).get_ai_model()
	
	def update_bias_analysis(self, inputs:dict | None = None, bias_analysis:BiasAnalysis=None,
		file_path:str=""):
		
		# raise error if no parameters are given
		if not inputs and not bias_analysis and not file_path:
			raise ValueError("no parameters were given")
		
		# updating BiasAnalysis
		if bias_analysis:
			Validator.validate(bias_analysis, "BiasAnalysis")
			self.model_card.bias_analysis = bias_analysis
		elif inputs:
			Validator.validate(inputs, "dict")
			self.model_card.bias_analysis = BiasAnalysis(**inputs)
		elif file_path:
			Validator.validate(inputs, "str")
			with open(file_path, "r") as file:
				self.model_card.bias_analysis = BiasAnalysis(**json.load(file))

	def update_xai_analysis(self, inputs:dict | None = None, xia_analysis:ExplainabilityAnalysis=None,
		file_path:str=""):

		# raise error if no parameters are given
		if not inputs and not xia_analysis and not file_path:
			raise ValueError("no parameters were given")

		# updating ExplainabilityAnalysis
		if xia_analysis:
			Validator.validate(xia_analysis, "ExplainabilityAnalysis")
			self.model_card.xia_analysis = xia_analysis
		elif inputs:
			Validator.validate(inputs, "dict")
			self.model_card.xia_analysis = ExplainabilityAnalysis(**inputs)
		elif file_path:
			Validator.validate(inputs, "str")
			with open(file_path, "r") as file:
				self.model_card.xia_analysis = ExplainabilityAnalysis(**json.load(file))

	def update_name(self, name:str):
		Validator.validate(name, "str")
		self.model_card.name = name

	def update_version(self, version:str):
		Validator.validate(version, "str")
		self.model_card.version = version

	def update_short_description(self, short_description:str):
		Validator.validate(short_description, "str")
		self.model_card.short_description = short_description

	def update_full_description(self, full_description:str):
		Validator.validate(full_description, "str")
		self.model_card.full_description = full_description

	def update_keywords(self, keywords:str):
		Validator.validate(keywords, "str")
		self.model_card.keywords = keywords

	def update_author(self, author:str):
		Validator.validate(author, "str")
		self.model_card.author = author

	def update_input_type(self, input_type:str):
		Validator.validate(input_type, "str")
		self.model_card.input_type = input_type

	def update_category(self, category:str):
		Validator.validate(category, "str")
		self.model_card.category = category

	def update_input_data(self, input_data:str):
		Validator.validate(input_data, "str")
		self.model_card.input_data = input_data

	def update_output_data(self, output_data:str):
		Validator.validate(output_data, "str")
		self.model_card.output_data = output_data

	def update_foundational_model(self, foundational_model:str):
		Validator.validate(foundational_model, "str")
		self.model_card.foundational_model = foundational_model

	def update_model_requirements(self, model_requirements:list[str]):
		Validator.validate(model_requirements, "list[str]")
		self.model_card.model_requirements = model_requirements

	def update_model_structure(self, trained_model):
		if self.model_card.ai_model:
			self.model_card.ai_model.populate_model_structure(trained_model)
		else:
			raise ValueError("never set an ai model")

	def populate_requirements(self):
		self.model_card.populate_requirements()

	def populate_bias(self, dataset, true_labels:list, predicted_labels:list,
		sensitive_feature_name:str, sensitive_feature_data:list, model):
		
		# validating inputs
		Validator.validate(true_labels, "list")
		Validator.validate(predicted_labels, "list")
		Validator.validate(sensitive_feature_name, "str")
		Validator.validate(sensitive_feature_data, "list")

		# populating bias
		self.model_card.populate_bias(dataset=dataset,
			true_labels=true_labels,
			predicted_labels=predicted_labels,
			sensitive_feature_name=sensitive_feature_name,
			sensitive_feature_data=sensitive_feature_data,
			model=model)

	def populate_xai(self, train_dataset, column_names:list, model, n_features:int=None):
		# validating inputs
		Validator.validate(column_names, "list")
		if n_features:
			Validator.validate(n_features, "int")
		
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

	def update_ai_model_metrics(self, metrics:dict | None = None, key:str | None = None,
		value:str | None = None):
		
		# validation
		if metrics is None and (key is None or value is None):
			raise ValueError("🛑 expected a metrics dict or key value pair")

		if self.model_card.ai_model is None:
			raise ValueError("🛑 the ai_model is not set on the model card")

		# setting values
		if metrics is not None:
			Validator.validate(metrics, "dict")
			self.model_card.ai_model.metrics = metrics
		else:
			Validator.validate(key, "str")
			Validator.validate(value, "str")
			self.model_card.ai_model.add_metric(key, value)

	def write_to_file(self, file_location:str):
		# validating inputs
		Validator.validate(file_location, "str")
		# validating model card before saving
		self.model_card.validate()
		# writing to file
		self.model_card.save(file_location)

	def write_model_to_patra_server(self, patra_server_url:str, token:str="") -> dict:
		# validating inputs
		
		Validator.validate(patra_server_url, "str")
		if token:
			Validator.validate(token, "str")

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

	def get_name(self) -> str:
		return self.model_card.name

	def get_version(self) -> str:
		return self.model_card.version

	def get_short_description(self) -> str:
		return self.model_card.short_description

	def get_full_description(self) -> str:
		return self.model_card.full_description

	def get_keywords(self) -> str:
		return self.model_card.keywords

	def get_author(self) -> str:
		return self.model_card.author

	def get_input_type(self) -> str:
		return self.model_card.input_type

	def get_category(self) -> str:
		return self.model_card.category

	def get_input_data(self) -> str:
		return self.model_card.input_data

	def get_output_data(self) -> str:
		return self.model_card.output_data

	def get_foundational_model(self) -> str:
		return self.model_card.foundational_model

	def get_documentation(self) -> str:
		return self.model_card.documentation

	def get_ai_model_name(self) -> str:
		return self.model_card.ai_model.name

	def get_ai_model_version(self) -> str:
		return self.model_card.ai_model.version

	def get_ai_model_description(self) -> str:
		return self.model_card.ai_model.description

	def get_ai_model_owner(self) -> str:
		return self.model_card.ai_model.owner

	def get_ai_model_location(self) -> str:
		return self.model_card.ai_model.location

	def get_ai_model_license(self) -> str:
		return self.model_card.ai_model.license

	def get_ai_model_framework(self) -> str:
		return self.model_card.ai_model.framework

	def get_ai_model_model_type(self) -> str:
		return self.model_card.ai_model.model_type

	def get_ai_model_test_accuracy(self) -> str:
		return self.model_card.ai_model.test_accuracy

	def get_ai_model_model_structure(self) -> str:
		return self.model_card.ai_model.model_structure

	def get_ai_model_metrics(self) -> str:
		return self.model_card.ai_model.metrics
