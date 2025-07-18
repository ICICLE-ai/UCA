from huggingface_hub import HfApi, ModelCard, create_repo, delete_repo, hf_hub_download, login, snapshot_download

from src.model_commons.patra.validator import Validator


class Hugging():
	
	@staticmethod
	def login(token:str="", file_path:str=""):
		# validating inputs
		Validator.validate(token, "str")
		Validator.validate(file_path, "str")
		
		# throw value error if didn't get any inputs
		if not token and not file_path:
			raise ValueError("🛑 expected a 'token' input or a 'file_path' input")

		# logging in
		if token:
			login(token=token)
		else:
			Validator.validate_file_exists(file_path)
			with open(file_path, "r") as file:
				read_token = file.read().strip()
				login(token=read_token)

	@staticmethod
	def download_file(repo_id:str, filename:str, revision:str="", local_dir:str="") -> str:
		# validating input data types
		Validator.validate(repo_id, "str")
		Validator.validate(filename, "str")
		Validator.validate(revision, "str")
		Validator.validate(local_dir, "str")

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
	def download_repo(repo_id:str, revision:str="", allow_patterns:list[str] | None = None,
		ignore_patterns:list[str] | None = None, local_dir:str="") -> str:
		
		# validating input data types
		Validator.validate(repo_id, "str")
		Validator.validate(revision, "str")
		if allow_patterns:
			Validator.validate(allow_patterns, "list[str]")
		if ignore_patterns:
			Validator.validate(ignore_patterns, "list[str]")
		Validator.validate(local_dir, "str")
	
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
	def get_repo_info(repo_id:str):
		Validator.validate(repo_id, "str")
		api = HfApi()
		return api.repo_info(repo_id)

	@staticmethod
	def upload_file(local_file_path:str, repo_file_path:str, repo_id:str, repo_type:str="",
		token:str="", token_file_path:str=""):
		# validating input data
		Validator.validate(local_file_path, "str")
		Validator.validate(repo_file_path, "str")
		Validator.validate(repo_id, "str")
		Validator.validate(repo_type, "str")
		Validator.validate(token, "str")
		Validator.validate(token_file_path, "str")
		Validator.validate_file_exists(local_file_path)		

		# login if given token or token_file_path
		if token or token_file_path:
			Hugging.login(token=token, file_path=token_file_path)
		
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
	def upload_folder(local_folder_path:str, repo_path:str, repo_id:str, repo_type:str="model",
		ignore_patterns:list[str] | None = None, allow_patterns:list[str] | None = None,
		delete_patterns:list[str] | None = None, token:str="", token_file_path:str=""):
		
		# validating input data
		Validator.validate(local_folder_path, "str")
		Validator.validate(repo_path, "str")
		Validator.validate(repo_id, "str")
		Validator.validate(repo_type, "str")
		if ignore_patterns:
			Validator.validate(ignore_patterns, "list[str]")
		if allow_patterns:
			Validator.validate(allow_patterns, "list[str]")
		if delete_patterns:
			Validator.validate(delete_patterns, "list[str]")
		Validator.validate(token, "str")
		Validator.validate(token_file_path, "str")
		Validator.validate_directory_exists(local_folder_path)	
	
		# login if token or token_file_path
		if token or token_file_path:
			Hugging.login(token=token, file_path=token_file_path)		

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
	def create_repo(repo_id:str, repo_type:str="", private:bool=False) -> str:
		# validating inputs
		Validator.validate(repo_id, "str")
		Validator.validate(repo_type, "str")
		Validator.validate(private, "bool")		
		
		if repo_type:
			return create_repo(repo_id, repo_type=repo_type, private=private)
		return create_repo(repo_id, private=private)

	@staticmethod
	def delete_repo(repo_id:str, repo_type:str=""):
		# validating inputs
		Validator.validate(repo_id, "str")
		Validator.validate(repo_type, "str")
		
		# deleting repo
		if repo_type:
			delete_repo(repo_id, repo_type=repo_type)
			return
		delete_repo(repo_id)

	@staticmethod
	def get_model_card(repo_id:str, token_file_path:str="", token:str="") -> ModelCard:
		# validating inputs
		Validator.validate(repo_id, "str")
		Validator.validate(token_file_path, "str")
		Validator.validate(token, "str")
		
		# login if given token or token_file_path
		if token or token_file_path:
			Hugging.login(token=token, file_path=token_file_path)

		# getting model card
		return ModelCard.load(repo_id)

	@staticmethod
	def push_model_card(repo_id:str, model_card:ModelCard, token_file_path:str="", token:str=""):
		Validator.validate(repo_id, "str")
		Validator.validate(model_card, "HFModelCard")
		Validator.validate(token_file_path, "str")
		Validator.validate(token, "str")

		# login if given token or token_file_path
		if token or token_file_path:
			Hugging.login(token=token, file_path=token_file_path)

		# writing model card
		model_card.push_to_hub(repo_id)
