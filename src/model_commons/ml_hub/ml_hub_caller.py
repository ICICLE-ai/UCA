from src.model_commons.patra.validator import Validator


class MLHubCaller():
	@staticmethod
	def get_base_url() -> str:
		return "https://dev.develop.tapis.io/v3/mlhub/models-api/platforms/"

	@staticmethod
	def build_get_model_url(platform:str) -> str:
		# validating inputs
		Validator.validate(platform, "str")
		result = MLHubCaller().GetBaseURL() + platform + "/models/"
		return result

	@staticmethod
	def pull_model_from_hugging_face():
		_url = MLHubCaller().build_get_model_url(platform="huggingface")
		raise NotImplementedError("PullModelFromHuggingFace has yet to be implemented")

	@staticmethod
	def write_model_to_hugging_face():
		raise NotImplementedError("WriteModelToHuggingFace has yet to be implemented")
	
	@staticmethod
	def search_hugging_face():
		raise NotImplementedError("SearchHuggingFace has yet to be implemented")

	@staticmethod
	def pull_model_from_github():
		_url = MLHubCaller().BuildGetModelURL(platform="github")
		raise NotImplementedError("PullModelFromGithub has yet to be implemented")

	@staticmethod
	def write_model_to_github():
		raise NotImplementedError("WriteModelToGithub has yet to be implemented")

	@staticmethod
	def search_patra():
		raise NotImplementedError("SearchPatra has yet to be implemented")

	@staticmethod
	def write_model_card_to_patra():
		raise NotImplementedError("WriteModelCardToPatra has yet to be implemented")

	@staticmethod
	def pull_model_card_from_patra():
		raise NotImplementedError("PullModelCardFromPatra has yet to be implemented")

	

