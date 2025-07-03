from huggingface_hub import hf_hub_download
from huggingface_hub import snapshot_download
from huggingface_hub import login
from huggingface_hub import HfApi
from huggingface_hub import create_repo
from huggingface_hub import delete_repo
from huggingface_hub import ModelCard
from src.model_commons.patra.validator import Validator

class Hugging():
	
	@staticmethod
	def Login(token:str="", file_path:str=""):
		# validating inputs
		Validator.Validate(token, "str")
		Validator.Validate(file_path, "str")
		
		# throw value error if didn't get any inputs
		if not token and not file_path:
			raise ValueError("🛑 expected a 'token' input or a 'file_path' input")

		# logging in
		if token:
			login(token=token)
		else:
			Validator.ValidateFileExists(file_path)
			with open(file_path, "r") as file:
				read_token = file.read().strip()
				login(token=read_token)

	@staticmethod
	def DownloadFile(repo_id:str, filename:str, revision:str="", local_dir:str="") -> str:
		# validating input data types
		Validator.Validate(repo_id, "str")
		Validator.Validate(filename, "str")
		Validator.Validate(revision, "str")
		Validator.Validate(local_dir, "str")

		# downloading to a specific local file path from particular revision	
		if revision and local_dir:
			return hf_hub_download(repo_id=repo_id, filename=filename, revision=revision,
				local_dir=local_dir)
		# downloading to a specific local file path
		if not revision and local_dir:
			return hf_hub_download(repo_id=repo_id, filename=filename, local_dir=local_dir)	
		# downloading a specific revision
		if revision and not local_dir:
			return hf_hub_download(repo_id=repo_id, filename=filename, revision=revision)
		# downloading file
		return hf_hub_download(repo_id=repo_id, filename=filename)

	@staticmethod
	def DownloadRepo(repo_id:str, revision:str="", allow_patterns:list[str]=[],
		ignore_patterns:list[str]=[], local_dir:str="") -> str:
		
		# validating input data types
		Validator.Validate(repo_id, "str")
		Validator.Validate(revision, "str")
		Validator.Validate(allow_patterns, "list[str]")
		Validator.Validate(ignore_patterns, "list[str]")
		Validator.Validate(local_dir, "str")
	
		# uploading repo
		if not revision and not allow_patterns and not ignore_patterns and not local_dir:
			return snapshot_download(repo_id = repo_id)
		if revision and not allow_patterns and not ignore_patterns and not local_dir:
			return snapshot_download(repo_id = repo_id, revision = revision)
		if not revision and allow_patterns and not ignore_patterns and not local_dir:
			return snapshot_download(repo_id, allow_patterns = allow_patterns)
		if not revision and not allow_patterns and ignore_patterns and not local_dir:
			return snapshot_download(repo_id, ignore_patterns = ignore_patterns)
		if not revision and not allow_patterns and not ignore_patterns and local_dir:
			return snapshot_download(repo_id, local_dir=local_dir)
		if revision and allow_patterns and not ignore_patterns and not local_dir:
			return snapshot_download(repo_id, revision = revision,
				allow_patterns = allow_patterns)
		if revision and not allow_patterns and ignore_patterns and not local_dir:
			return snapshot_download(repo_id, revision = revision,
				ignore_patterns = ignore_patterns)
		if revision and not allow_patterns and not ignore_patterns and local_dir:
			return snapshot_download(repo_id, revision=revision, local_dir=local_dir)
		if not revision and allow_patterns and ignore_patterns and not local_dir:
			return snapshot_download(repo_id, allow_patterns = allow_patterns,
				ignore_patterns = ignore_patterns)
		if not revision and allow_patterns and not ignore_patterns and local_dir:
			return snapshot_download(repo_id, allow_patterns = allow_patterns,
				local_dir=local_dir)
		if not revision and not allow_patterns and ignore_patterns and local_dir:
			return snapshot_download(repo_id, ignore_patterns = ignore_patterns,
				local_dir=local_dir)
		if allow_patterns and ignore_patterns and revision and not local_dir:
			return snapshot_download(repo_id, allow_patterns = allow_patterns,
				ignore_patterns = ignore_patterns, revision = revision)
		if allow_patterns and ignore_patterns and not revision and local_dir:
			return snapshot_download(repo_id, allow_patterns = allow_patterns,
				ignore_patterns = ignore_patterns, local_dir = local_dir)
		if allow_patterns and not ignore_patterns and revision and local_dir:
			return snapshot_download(repo_id, allow_patterns = allow_patterns,
				revision = revision, local_dir = local_dir)
		if not allow_patterns and ignore_patterns and revision and local_dir:
			return snapshot_download(repo_id, ignore_patterns = ignore_patterns,
				revision = revision, local_dir = local_dir)
		if allow_patterns and ignore_patterns and revision and local_dir:
			return snapshot_download(repo_id, ignore_patterns = ignore_patterns,
				revision = revision, local_dir = local_dir)

	@staticmethod
	def GetRepoInfo(repo_id:str):
		Validator.Validate(repo_id, "str")
		api = HfApi()
		return api.repo_info(repo_id)

	@staticmethod
	def UploadFile(local_file_path:str, repo_file_path:str, repo_id:str, repo_type:str="",
		token:str="", token_file_path:str=""):
		# validating input data
		Validator.Validate(local_file_path, "str")
		Validator.Validate(repo_file_path, "str")
		Validator.Validate(repo_id, "str")
		Validator.Validate(repo_type, "str")
		Validator.Validate(token, "str")
		Validator.Validate(token_file_path, "str")
		Validator.ValidateFileExists(local_file_path)		

		# login if given token or token_file_path
		if token or token_file_path:
			Hugging.Login(token=token, file_path=token_file_path)
		
		# making api call
		api = HfApi()
		if repo_type:
			return api.upload_file(path_or_fileobj = local_file_path,
				path_in_repo = repo_file_path,
				repo_id = repo_id,
				repo_type = repo_type)
		return api.upload_file(path_or_fileobj = local_file_path,
			path_in_repo = repo_file_path,
			repo_id = repo_id)

	@staticmethod
	def UploadFolder(local_folder_path:str, repo_path:str, repo_id:str, repo_type:str="model",
		ignore_patterns:list[str]=[], allow_patterns:list[str]=[], delete_patterns:list[str]=[],
		token:str="", token_file_path:str=""):
		
		# validating input data
		Validator.Validate(local_folder_path, "str")
		Validator.Validate(repo_path, "str")
		Validator.Validate(repo_id, "str")
		Validator.Validate(repo_type, "str")
		Validator.Validate(ignore_patterns, "list[str]")
		Validator.Validate(allow_patterns, "list[str]")
		Validator.Validate(delete_patterns, "list[str]")
		Validator.Validate(token, "str")
		Validator.Validate(token_file_path, "str")
		Validator.ValidateDirectoryExists(local_folder_path)	
	
		# login if token or token_file_path
		if token or token_file_path:
			Hugging.Login(token=token, file_path=token_file_path)		

		# making api call
		api = HfApi()
		if ignore_patterns and not allow_patterns and not delete_patterns:
			return api.upload_folder(folder_path = local_folder_path,
				repo_id = repo_id,
				path_in_repo = repo_path,
				repo_type = repo_type,
				ignore_patterns = ignore_patterns)
		if not ignore_patterns and allow_patterns and not delete_patterns:
			return api.upload_folder(folder_path = local_folder_path,
				repo_id = repo_id,
				path_in_repo = repo_path,
				repo_type = repo_type,
				allow_patterns = allow_patterns)
		if not ignore_patterns and not allow_patterns and delete_patterns:
			return api.upload_folder(folder_path = local_folder_path,
				repo_id = repo_id,
				path_in_repo = repo_path,
				repo_type = repo_type,
				delete_patterns = delete_patterns)
		if ignore_patterns and allow_patterns and not delete_patterns:
			return api.upload_folder(foler_path = local_folder_path,
				repo_id = repo_id,
				path_in_repo = repo_path, 
				repo_type = repo_type,
				ignore_patterns = ignore_patterns,
				allow_patterns = allow_patterns)
		if ignore_patterns and not allow_patterns and delete_patterns:
			return api.upload_folder(folder_path = local_folder_path,
				repo_id = repo_id,
				path_in_repo = repo_path,
				repo_type = repo_type,
				ignore_patterns = ignore_patterns,
				delete_patterns = delete_patterns)
		if not ignore_patterns and allow_patterns and delete_patterns:
			return api.upload_folder(folder_path = local_folder_path,
				repo_id = repo_id,
				path_in_repo = repo_path,
				repo_type = repo_type,
				allow_patterns = allow_patterns,
				delete_patterns = delete_patterns)
		if ignore_patterns and allow_patterns and delete_patterns:
			return api.upload_folder(folder_path = local_folder_path,
				repo_id = repo_id,
				path_in_repo = repo_path,
				repo_type = repo_type,
				ignore_patterns = ignore_patterns,
				allow_patterns = allow_patterns,
				delete_patterns = delete_patterns)
		return api.upload_folder(folder_path = local_folder_path,
			repo_id = repo_id,
			path_in_repo = repo_path,
			repo_type = repo_type)

	@staticmethod
	def CreateRepo(repo_id:str, repo_type:str="", private:bool=False) -> str:
		# validating inputs
		Validator.Validate(repo_id, "str")
		Validator.Validate(repo_type, "str")
		Validator.Validate(private, "bool")		
		
		if repo_type:
			return create_repo(repo_id, repo_type=repo_type, private=private)
		return create_repo(repo_id, private=private)

	@staticmethod
	def DeleteRepo(repo_id:str, repo_type:str=""):
		# validating inputs
		Validator.Validate(repo_id, "str")
		Validator.Validate(repo_type, "str")
		
		# deleting repo
		if repo_type:
			delete_repo(repo_id, repo_type=repo_type)
			return
		delete_repo(repo_id)

	@staticmethod
	def GetModelCard(repo_id:str, token_file_path:str="", token:str="") -> ModelCard:
		# validating inputs
		Validator.Validate(repo_id, "str")
		Validator.Validate(token_file_path, "str")
		Validator.Validate(token, "str")
		
		# login if given token or token_file_path
		if token or token_file_path:
			Hugging.Login(token=token, file_path=token_file_path)

		# getting model card
		return ModelCard.load(repo_id)

	@staticmethod
	def PushModelCard(repo_id:str, model_card:ModelCard, token_file_path:str="", token:str=""):
		Validator.Validate(repo_id, "str")
		Validator.Validate(model_card, "HFModelCard")
		Validator.Validate(token_file_path, "str")
		Validator.Validate(token, "str")

		# login if given token or token_file_path
		if token or token_file_path:
			Hugging.Login(token=token, file_path=token_file_path)

		# writing model card
		model_card.push_to_hub(repo_id)
