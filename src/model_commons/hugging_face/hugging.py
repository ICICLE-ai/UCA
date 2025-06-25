from huggingface_hub import hf_hub_download
from huggingface_hub import snapshot_download
from huggingface_hub import HfApi
from src.model_commons.patra.validator import Validator

class Hugging():
	
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
	def UploadFile(local_file_path:str, repo_file_path:str, repo_id:str, repo_type:str=""):
		# validating input data
		Validator.Validate(local_file_path, "str")
		Validator.Validate(repo_file_path, "str")
		Validator.Validate(repo_id, "str")
		Validator.Validate(repo_type, "str")
		
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
		ignore_patterns:list[str]=[], allow_patterns:list[str]=[], delete_patterns:list[str]=[]):
		
		# validating input data
		Validator.Validate(local_folder_path, "str")
		Validator.Validate(repo_path, "str")
		Validator.Validate(repo_id, "str")
		Validator.Validate(repo_type, "str")
		Validator.Validate(ignore_patterns, "list[str]")
		Validator.Validate(allow_patterns, "list[str]")
		Validator.Validate(delete_patterns, "list[str]")
		
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
