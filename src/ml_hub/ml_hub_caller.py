import requests
from src.patra.validator import Validator


class MLHubCaller():
	@staticmethod
	def GetBaseURL() -> str:
		return "https://dev.develop.tapis.io/v3/mlhub/models-api/platforms/"

	@staticmethod
	def BuildGetModelURL(platform:str) -> str:
		# validating inputs
		Validator.Validate(platform, "str")
		result = GetBaseURL() + platform + "/models/"
		return result

	@staticmethod
	def PullModelFromHuggingFace():
		url = BuildGetModelURL(platform="huggingface")
		raise NotImplementedError("PullModelFromHuggingFace has yet to be implemented")

	@staticmethod
	def WriteModelToHuggingFace():
		raise NotImplementedError("WriteModelToHuggingFace has yet to be implemented")
	
	@staticmethod
	def SearchHuggingFace():
		raise NotImplementedError("SearchHuggingFace has yet to be implemented")

	@staticmethod
	def PullModelFromGithub():
		url = BuildGetModelURL(platform="github")
		raise NotImplementedError("PullModelFromGithub has yet to be implemented")

	@staticmethod
	def WriteModelToGithub():
		raise NotImplementedError("WriteModelToGithub has yet to be implemented")

	@staticmethod
	def SearchPatra():
		raise NotImplementedError("SearchPatra has yet to be implemented")

	@staticmethod
	def WriteModelCardToPatra():
		raise NotImplementedError("WriteModelCardToPatra has yet to be implemented")

	@staticmethod
	def PullModelCardFromPatra():
		raise NotImplementedError("PullModelCardFromPatra has yet to be implemented")

	

