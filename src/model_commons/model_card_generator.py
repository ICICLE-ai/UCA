from dataclasses import dataclass
from typing import Optional

from huggingface_hub import ModelCard

from src.model_commons.hugging_face.hugging import Hugging
from src.model_commons.patra.model_card_wrapper import ModelCardWrapper
from src.model_commons.patra.validator import Validator


@dataclass
class ModelCardGenerator():
	pmc_wrapper: ModelCardWrapper
	hf_card: Optional[ModelCard] = None
	hf_repo_id: Optional[str] = None
	hf_create_repo: Optional[bool] = None

	def __init__(self, patra_model_dict: dict | None = None,
		patra_model_file: str | None = None, patra_ai_model_dict: dict | None = None,
		patra_ai_model_file: str | None = None, hf_card_dict: dict | None = None,
		hf_model_card_file: str | None = None, hf_repo_id: str | None = None,
		hf_create_repo: bool = False):

		# ensuring that a patra model card dictionary or file path is provided
		if not patra_model_dict and not patra_model_file:
			raise ValueError("🛑 expected either a 'patra_model_dict' or " + 
				"'patra_model_file'")
		if not patra_ai_model_dict and not patra_ai_model_file:
			raise ValueError("🛑 expected either a 'patra_ai_model_dict' or " +
				"'patra_ai_model_file'")

		# creating patra model card wrapper
		if patra_model_dict:
			self.pmc_wrapper = ModelCardWrapper(inputs=patra_model_dict)
		else:
			self.pmc_wrapper = ModelCardWrapper(file_path=patra_model_file)
	
		# creating patra ai model card wrapper	
		if patra_ai_model_dict:
			self.pmc_wrapper.update_ai_model(inputs = patra_ai_model_dict)
		else:
			self.pmc_wrapper.update_ai_model(file_path = patra_ai_model_file)

		# creating hugging face dictionary
		if hf_card_dict: 
			self.hf_card = Hugging.generate_model_card(self.make_hug_dict(hf_card_dict))
		
		# TODO write all of these

	def make_hug_dict(self, extra_inputs:dict) -> dict:
		# validating inputs
		Validator.Validate(extra_inputs, "dict")
	
		# building resulting dictionary
		result = {}
		result = self.hug_dict_from_patra(hug=result)
		result = self.generate_hugging_face_dict(result, extra_inputs)
		return result

	def hug_dict_from_patra(self, hug:dict) -> dict:
		# validating inputs
		Validator.Validate(hug, "dict")	

		# setting fields for ModelCardData
		hug["base_model"] = self.build_id(self.pmc_wrapper.get_foundational_model())
		hug["datasets"] = self.build_id(self.pmc_wrapper.get_input_type(), dataset=True)
		hug["library_name"] = self.pmc_wrapper.get_ai_model_framework()
		hug["license"] = self.pmc_wrapper.get_ai_model_license()
		hug["metrics"] = self.build_huggingface_metrics()
		hug["model_name"] = self.patra_wrapper.get_name()
		hug["pipeline_tag"] = self.patra_wrapper.get_category()
		hug["tags"] = self.patra_wrapper.get_keywords()
		
		# setting fields for ModelCard
		hug["developers"] = self.build_authors()
		hug["shared_by"] = self.build_atuhors()
		hug["model_type"] = self.pmc_wrapper.get_ai_model_model_type()
		hug["repo"] = self.pmc_wrapper.get_ai_model_location()
		hug["more_information"] = self.pmc_wrapper.get_documentation()
		hug["model_card_authors"] = self.build_authors()
		td = f"{self.pmc_wrapper.get_input_type()}\n{self.pmc_wrapper.get_input_data()}"
		hug["training_data"] = td
		hug["testing_metrics"] = self.build_huggingface_metrics()
		hug["training_regime"] = self.build_training_regime()
		hug["results"] = self.build_results_dict()
		return hug

	def generate_hugging_face_dict(self, hug:dict, inputs:dict) -> dict:
		hug = self.add("funded_by", hug, inputs)
		hug = self.add("language", hug, inputs)
		hug = self.add("paper", hug, inputs)
		hug = self.add("demo", hug, inputs)
		hug = self.add("direct_use", hug, inputs)
		hug = self.add("downstream_use", hug, inputs)
		hug = self.add("out_of_scope_use", hug, inputs)
		hug = self.add("bias_risk_limitations", hug, inputs)
		hug = self.add("bias_recommendations", hug, inputs)
		hug = self.add("get_started_code", hug, inputs)
		hug = self.add("preprocessing", hug, inputs)
		hug = self.add("speed_sizes_times", hug, inputs)
		hug = self.add("testing_data", hug, inputs)
		hug = self.add("testing_factors", hug, inputs)
		hug = self.add("results_summary", hug, inputs)
		hug = self.add("model_examination", hug, inputs)
		hug = self.add("hardware_type", hug, inputs)
		hug = self.add("hours_used", hug, inputs)
		hug = self.add("cloud_provider", hug, inputs)
		hug = self.add("co2_emitted", hug, inputs)
		hug = self.add("model_specs", hug, inputs)
		hug = self.add("compute_infrastructure", hug, inputs)
		hug = self.add("hardware_requirements", hug, inputs)
		hug = self.add("software", hug, inputs)
		hug = self.add("citation_bibtext", hug, inputs)
		hug = self.add("citation_apa", hug, inputs)
		hug = self.add("glossary", hug, inputs)
		hug = self.add("model_card_contact", hug, inputs)
		return hug

	def add(self, key:str, result:dict, original:str) -> dict:
		if key in original.keys():
			result[key] = original[key]
		return result

	def build_id(self, link:str, dataset:bool=False) -> str:
		if not self.is_huggingface_link(link, dataset):
			return None
		working = "https://huggingface.co/datasets/" if dataset else "https://huggingface.co/"
		index = len(working)
		return link[index:]
	
	def is_huggingface_link(self, link:str, dataset:bool=False) -> bool:
		working = "https://huggingface.co/datasets/" if dataset else "https://huggingface.co/"
		return True if link.find(working) == 0 else False

	def build_huggingface_metrics(self) -> list[str]:
		expected_other_values = ["Test loss", "Epochs", "Batch Size", "Optimizer",
			"Learning Rate", "Input Shape"]
		metrics = []
		for metric in self.patra_wrapper.get_ai_model_metrics():
			if metric not in expected_other_values:
				metrics.append(metric)
		if len(metrics) == 0:
			return None
		return metrics

	def build_results_dict(self) -> str:
		result = {}
		ai_model_metrics = self.build_huggingface_metrics()
		metrics = self.pmc_wrapper.get_ai_model_metrics()
		for metric in metrics:
			result[metric] = ai_model_metrics[metric]
		return str(result)

	def build_training_regime(self) -> str:
		result = {}
		metrics = self.pmc_wrapper.get_ai_model_metrics()
		non_metrics = ["Test loss","Epochs","Batch Size","Optimizer","Learning Rate",
			"Input Shape"]
		for metric in metrics:
			if metric in non_metrics:
				result[metric] = metrics[metric]
		return str(result)

	def build_authors(self) -> str:
		if self.pmc_wrapper.get_author() != self.patra_wrapper.get_ai_model_owner():
			return f"{self.wrapper.get_author()}, {self.patra_wrapper.get_ai_model_owner}"
		return self.pmc_wrapper.get_author()
