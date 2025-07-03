import unittest
import os
from pathlib import Path
import shutil
from src.model_commons.hugging_face.hugging import Hugging
from huggingface_hub import ModelCard

class TestHuggingClass(unittest.TestCase):
	def test_login_bad_token_type(self):
		with self.assertRaises(TypeError):
			Hugging.Login(token=12344)

	def test_login_bad_file_path_type(self):
		with self.assertRaises(TypeError):
			Hugging.Login(file_path=[123,456])

	def test_login_file_path_doesnt_exist(self):
		with self.assertRaises(ValueError):
			Hugging.Login(file_path="src/model_commons/hugging_face/hug_token.txt")

	def test_login_bad_no_inputs(self):
		with self.assertRaises(ValueError):
			Hugging.Login()

	def test_login_pass_file_path(self):
		try:
			Hugging.Login(file_path="src/model_commons/hugging_face/hugging_face_token.txt")
		except Exception as e:
			self.fail(f"❌ unexpected exception: {e}")

	def test_login_pass_token(self):
		try:
			with open("src/model_commons/hugging_face/hugging_face_token.txt", "r") as file:
				token = file.read().strip()
			Hugging.Login(token=token)
		except Exception as e:
			self.fail(f"❌ unexpected exception: {e}")

	def test_download_file_bad_repo_id_type(self):
		with self.assertRaises(TypeError):
			Hugging.DownloadFile(repo_id=123, filename="test")

	def test_download_file_bad_filename_type(self):
		with self.assertRaises(TypeError):
			Hugging.DownloadFile(repo_id="test", filename={"a":1,"b":2})

	def test_download_file_bad_revision_type(self):
		with self.assertRaises(TypeError):
			Hugging.DownloadFile(repo_id="test", filename="test", revision=[])

	def test_download_file_bad_local_dir_type(self):
		with self.assertRaises(TypeError):
			Hugging.DownloadFile(repo_id="test", filename="test", revision="test",
				local_dir=1234.5)

	def test_download_file_pass(self):
		try:
			file_location = Hugging.DownloadFile(repo_id=PublicRepoId(),
				filename="README.md")
		except Exception as e:
			self.fail(f"unexpected exception: {e}")

	def test_download_file_pass_with_local_dir(self):
		try:
			# downloading file from hugging face
			file_location = Hugging.DownloadFile(repo_id=PublicRepoId(),
				filename="README.md", local_dir="src/model_commons/hugging_face/temp_test_dir/")
			# fail test if file does not exist in the expected directory
			if "README.md" not in os.listdir("src/model_commons/hugging_face/temp_test_dir/"):
				self.fail(f"❌ file not found in src/model_commons/hugging_face/temp_test_dir/")
			# delete file
			if os.path.exists("src/model_commons/hugging_face/temp_test_dir/README.md"):
				os.remove("src/model_commons/hugging_face/temp_test_dir/README.md")
		except Exception as e:
			self.fail(f"❌ unexpected exception: {e}")

	def test_download_repo_bad_repo_id_type(self):
		with self.assertRaises(TypeError):
			Hugging.DownloadRepo(repo_id=[1,2,3], revision="test")

	def test_download_repo_bad_revision_type(self):
		with self.assertRaises(TypeError):
			Hugging.DownloadRepo(repo_id="test", revision=1234.5)

	def test_download_repo_bad_allow_patterns_type(self):
		with self.assertRaises(TypeError):
			Hugging.DownloadRepo(repo_id="test", revision="test", allow_patterns={"a":1,"b":2})

	def test_download_repo_bad_ignore_patterns_type(self):
		with self.assertRaises(TypeError):
			Hugging.DownloadRepo(repo_id="test", ignore_patterns=1234.5)

	def test_download_repo_bad_local_dir_type(self):
		with self.assertRaises(TypeError):
			Hugging.DownloadRepo(repo_id="test", local_dir=[12,34,"test"])

	def test_download_repo_pass(self):
		try:
			Hugging.DownloadRepo(repo_id=PublicRepoId())
		except Exception as e:
			self.fail(f"❌ unexpected exception: {e}")

	def test_download_repo_to_local_dir_pass(self):
		try:
			# downloading repo from hugging face
			location = Hugging.DownloadRepo(repo_id=PublicRepoId(),
				local_dir="src/model_commons/hugging_face/temp_test_dir/")
			# fail test id file does not exist in the expected directory
			if "README.md" not in os.listdir("src/model_commons/hugging_face/temp_test_dir/"):
				self.fail(f"❌ an expected file was not found in src/model_commons/hugging_face/temp_test_dir/")
			dir_path = Path("src/model_commons/hugging_face/temp_test_dir")
			if dir_path.is_dir():
				shutil.rmtree(dir_path)
				dir_path.mkdir()
			else:
				self.fail(f"❌ src/model_commons/hugging_face/temp_test_dir is not a directory")
		except:
			self.fail(f"❌ unexpected exception: {e}")

	def test_upload_file_bad_local_file_path_type(self):
		with self.assertRaises(TypeError):
			Hugging.UploadFile(local_file_path=[1,2,3,4], repo_file_path="test",
				repo_id="test")

	def test_upload_file_bad_repo_file_path_type(self):
		with self.assertRaises(TypeError):
			Hugging.UploadFile(local_file_path="test", repo_file_path={"a":1,"b":2},
				repo_id="test")

	def test_upload_file_bad_repo_id_type(self):
		with self.assertRaises(TypeError):
			Hugging.UploadFile(local_file_path="test", repo_file_path="test",
				repo_is=1234)

	def test_upload_file_bad_repo_type_type(self):
		with self.assertRaises(TypeError):
			Hugging.UploadFile(local_file_path="test", repo_file_path="test",
				repo_id="test", repo_type=[12,34])

	def test_upload_file_bad_token_type(self):
		with self.assertRaises(TypeError):
			Hugging.UploadFile(local_file_path="src/model_commons/hugging_face/README.md",
				repo_file_path="README.md", repo_id=PublicRepoId(), token=1234.56)

	def test_upload_file_bad_token_file_path_type(self):
		with self.assertRaises(TypeError):
			Hugging.UploadFile(local_file_path="src/model_commons/hugging_face/README.md",
				repo_file_path="README.md", repo_id=PublicRepoId(),
				token_file_path=[12,34,56,78])

	def test_upload_file_bad_local_file_path(self):
		with self.assertRaises(ValueError):
			Hugging.UploadFile(local_file_path="src/model_commons/hugging_face/READM.md",
				repo_file_path="README.md", repo_id=PublicRepoId(),
				token_file_path="src/model_commons/hugging_face/hugging/hugging_face_token.txt")

	def test_upload_file_pass(self):
		try:
			file_path = Path("src/model_commons/hugging_face/README.md")
			if not file_path.is_file():
				self.fail(f"❌ neccessary file at src/model_commons/hugging_face/README.md is not present")
			Hugging.UploadFile(local_file_path="src/model_commons/hugging_face/README.md",
				repo_file_path="README.md", repo_id=PublicRepoId())
		except Exception as e:
			self.fail(f"❌ received unexpected exception: {e}")

	def test_upload_file_with_token_file_path_pass(self):
		try:
			Hugging.UploadFile(local_file_path="src/model_commons/hugging_face/README.md",
				repo_file_path="README.md", repo_id=PublicRepoId(),
				token_file_path=TokenFilePath())	
		except Exception as e:
			self.fail(f"❌ receivied unexpected exception: {e}")

	def test_upload_file_with_token_pass(self):
		try:
			with open(TokenFilePath(), "r") as file: token = file.read().strip()
			Hugging.UploadFile(local_file_path="src/model_commons/hugging_face/README.md",
				repo_file_path="README.md", repo_id=PublicRepoId(),
				token=token)
		except Exception as e:
			self.fail(f"❌ receivied unexpected exception: {e}")

	def test_upload_folder_bad_local_folder_path_type(self):
		with self.assertRaises(TypeError):
			Hugging.UploadFolder(local_folder_path=1234, repo_path="test", repo_id="test")

	def test_upload_folder_bad_repo_path_type(self):
		with self.assertRaises(TypeError):
			Hugging.UploadFolder(local_folder_path="test", repo_path=[12,34], repo_id="test")

	def test_upload_folder_bad_repo_id_type(self):
		with self.assertRaises(TypeError):
			Hugging.UploadFolder(local_folder_path="test", repo_path="test", repo_id=12.34)

	def test_upload_folder_bad_repo_type_type(self):
		with self.assertRaises(TypeError):
			Hugging.UploadFolder(local_folder_path="test", repo_path="test", repo_id="test",
				repo_type={"a":1})

	def test_upload_folder_bad_ignore_patterns_type(self):
		with self.assertRaises(TypeError):
			Hugging.UploadFolder(local_folder_path="test", repo_path="test", repo_id="test",
				ignore_patterns=123.45)

	def test_upload_folder_bad_allow_patterns_type(self):
		with self.assertRaises(TypeError):
			Hugging.UploadFolder(local_folder_path="test", repo_path="test", repo_id="test",
				allow_patterns={"a":1,"b":2})

	def test_upload_folder_bad_delete_patterns_type(self):
		with self.assertRaises(TypeError):
			Hugging.UploadFolder(local_folder_path="test", repo_path="test", repo_id="test",
				delete_patterns=1e-6)

	def test_upload_folder_bad_local_folder_path(self):
		with self.assertRaises(ValueError):
			Hugging.UploadFolder(
				local_folder_path="src/model_commons/hugging_face/temp_test",
				repo_path="", repo_id=PublicRepoId())

	def test_upload_folder_pass(self):
		try:
			Hugging.UploadFolder(local_folder_path=LocalFolderPath(),
				repo_path="", repo_id=PublicRepoId())
		except Exception as e:
			self.fail(f"❌ receivied unexpected exception: {e}")

	def test_upload_folder_with_token_file_path_pass(self):
		try:
			Hugging.UploadFolder(local_folder_path=LocalFolderPath(),
				repo_path="", repo_id=PublicRepoId(),
				token_file_path=TokenFilePath())
		except Exception as e:
			self.fail(f"❌ receivied unexpected exception: {e}")

	def test_upload_folder_with_token_pass(self):
		try:
			with open(TokenFilePath(), "r") as file: token = file.read().strip()
			Hugging.UploadFolder(local_folder_path=LocalFolderPath(),
				repo_path="", repo_id=PublicRepoId(),
				token=token)
		except Exception as e:
			self.fail(f"❌ receivied unexpected exception: {e}")

	def test_get_repo_info_bad_repo_id_type(self):
		with self.assertRaises(TypeError):
			Hugging.GetRepoInfo(repo_id=[1,2,3,4])

	def test_get_repo_info_pass(self):
		try:
			Hugging.GetRepoInfo(repo_id=PublicRepoId())
		except Exception as e:
			self.fail(f"❌ receivied unexpected exception: {e}")

	def test_create_repo_bad_repo_id_type(self):
		with self.assertRaises(TypeError):
			Hugging.CreateRepo(repo_id=123445.5)

	def test_create_repo_bad_repo_type_type(self):
		with self.assertRaises(TypeError):
			Hugging.CreateRepo(repo_id=PublicRepoId(), repo_type=[1,2,34])

	def test_create_repo_pass(self):
		try:
			Hugging.CreateRepo(repo_id=TempRepoId())
		except Exception as e:
			self.fail(f"❌ receivied unexpected exception: {e}")

	def test_delete_repo_pass(self):
		try:
			Hugging.DeleteRepo(repo_id=TempRepoId())
		except Exception as e:
			self.fail(f"❌ receivied unexpected exception: {e}")

	def test_create_pivate_repo_pass(self):
		try:
			Hugging.CreateRepo(repo_id=TempPrivateRepoId(), private=True)
		except Exception as e:
			self.fail(f"❌ receivied unexpected exception: {e}")

	def test_delete_private_repo_pass(self):
		try:
			Hugging.DeleteRepo(repo_id=TempPrivateRepoId())
		except Exception as e:
			self.fail(f"❌ receivied unexpected exception: {e}")

	def test_create_dataset_repo(self):
		try:
			Hugging.CreateRepo(repo_id=TempDatasetRepoId(), repo_type="dataset")
		except Exception as e:
			self.fail(f"❌ receivied unexpected exception: {e}")

	def test_delete_dataset_repo(self):
		try:
			Hugging.DeleteRepo(repo_id=TempDatasetRepoId(), repo_type="dataset")
		except Exception as e:
			self.fail(f"❌ receivied unexpected exception: {e}")

	def test_create_repo_bad_private_type(self):
		with self.assertRaises(TypeError):
			Hugging.CreateRepo(repo_id=PublicRepoId(), private={"a":1,"b":2})

	def test_delete_repo_bad_repo_id_type(self):
		with self.assertRaises(TypeError):
			Hugging.DeleteRepo(repo_id=[1,24,4])

	def test_delete_repo_bad_repo_type_type(self):
		with self.assertRaises(TypeError):
			Hugging.DeleteRepo(repo_id=PublicRepoId(), repo_type=123.7543)

	def test_get_model_card_bad_repo_id_type(self):
		with self.assertRaises(TypeError):
			Hugging.GetModelCard(repo_id=[12,34,67])
	
	def test_get_model_card_bad_token_type(self):
		with self.assertRaises(TypeError):
			Hugging.GetModelCard(repo_id=PublicRepoId(),
				token={"a":1,"b":2})

	def test_get_model_card_bad_token_file_path_type(self):
		with self.assertRaises(TypeError):
			Hugging.GetModelCard(repo_id=PublicRepoId(),
				token_file_path=12344.245)

	def test_get_model_card_pass(self):
		try:	
			mc = Hugging.GetModelCard(repo_id=PublicRepoId())
			if not isinstance(mc, ModelCard):
				self.fail(f"❌ expected ModelCard type got {type(mc)}")
		except Exception as e:
			self.fail(f"❌ receivied unexpected exception: {e}")

	def test_push_model_card_bad_repo_id_type(self):
		model_card = Hugging.GetModelCard(repo_id=PublicRepoId())
		with self.assertRaises(TypeError):
			Hugging.PushModelCard(repo_id=1234.5, model_card=model_card)

	def test_push_model_card_bad_model_card_type(self):
		with self.assertRaises(TypeError):
			Hugging.PushModelCard(repo_id=PublicRepoId(), model_card=["a","b","c"])

	def test_push_model_card_bad_token_file_path_type(self):
		model_card = Hugging.GetModelCard(repo_id=PublicRepoId())
		with self.assertRaises(TypeError):
			Hugging.PushModelCard(repo_id=PublicRepoId(), model_card=model_card,
				token_file_path={"a":"b","c":"d"})

	def test_push_model_card_bad_token_type(self):
		model_card = Hugging.GetModelCard(repo_id=PublicRepoId())
		with self.assertRaises(TypeError):
			Hugging.PushModelCard(repo_id=PublicRepoId(), model_card=model_card,
				token=12345.78)

	def test_push_model_card_pass(self):
		model_card = Hugging.GetModelCard(repo_id=PublicRepoId())
		Hugging.PushModelCard(repo_id=PublicRepoId(), model_card=model_card,
			token_file_path=TokenFilePath())

def PublicRepoId() -> str:
	return "NickCliffel/PublicUCATestRepo"

def TempRepoId() -> str:
	return "NickCliffel/TempRepo"

def TempPrivateRepoId() -> str:
	return "NickCliffel/TempPrivateRepo"

def TempDatasetRepoId() -> str:
	return "NickCliffel/TempDatasetRepo"

def TokenFilePath() -> str:
	return "src/model_commons/hugging_face/hugging_face_token.txt"

def LocalFolderPath() -> str:
	return "src/model_commons/hugging_face/temp_test_dir/"
