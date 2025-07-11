import os
import shutil
import unittest
from pathlib import Path

from huggingface_hub import ModelCard

from src.model_commons.hugging_face.hugging import Hugging


class TestHuggingClass(unittest.TestCase):
	def test_login_bad_token_type(self):
		with self.assertRaises(TypeError):
			Hugging.login(token=12344)

	def test_login_bad_file_path_type(self):
		with self.assertRaises(TypeError):
			Hugging.login(file_path=[123,456])

	def test_login_file_path_doesnt_exist(self):
		with self.assertRaises(ValueError):
			Hugging.login(file_path="src/model_commons/hugging_face/hug_token.txt")

	def test_login_bad_no_inputs(self):
		with self.assertRaises(ValueError):
			Hugging.login()

	def test_login_pass_file_path(self):
		try:
			Hugging.login(file_path="src/model_commons/hugging_face/hugging_face_token.txt")
		except Exception as e:
			self.fail(f"❌ unexpected exception: {e}")

	def test_login_pass_token(self):
		try:
			with open("src/model_commons/hugging_face/hugging_face_token.txt", "r") as file:
				token = file.read().strip()
			Hugging.login(token=token)
		except Exception as e:
			self.fail(f"❌ unexpected exception: {e}")

	def test_download_file_bad_repo_id_type(self):
		with self.assertRaises(TypeError):
			Hugging.download_file(repo_id=123, filename="test")

	def test_download_file_bad_filename_type(self):
		with self.assertRaises(TypeError):
			Hugging.download_file(repo_id="test", filename={"a":1,"b":2})

	def test_download_file_bad_revision_type(self):
		with self.assertRaises(TypeError):
			Hugging.download_file(repo_id="test", filename="test", revision=[])

	def test_download_file_bad_local_dir_type(self):
		with self.assertRaises(TypeError):
			Hugging.download_file(repo_id="test", filename="test", revision="test",
				local_dir=1234.5)

	def test_download_file_pass(self):
		try:
			_file_location = Hugging.download_file(repo_id=public_repo_id(),
				filename="README.md")
		except Exception as e:
			self.fail(f"unexpected exception: {e}")

	def test_download_file_pass_with_local_dir(self):
		try:
			# downloading file from hugging face
			_file_location = Hugging.download_file(repo_id=public_repo_id(),
				filename="README.md", local_dir="src/model_commons/hugging_face/temp_test_dir/")
			# fail test if file does not exist in the expected directory
			if "README.md" not in os.listdir("src/model_commons/hugging_face/temp_test_dir/"):
				self.fail("❌ file not found in src/model_commons/hugging_face/temp_test_dir/")
			# delete file
			if os.path.exists("src/model_commons/hugging_face/temp_test_dir/README.md"):
				os.remove("src/model_commons/hugging_face/temp_test_dir/README.md")
		except Exception as e:
			self.fail(f"❌ unexpected exception: {e}")

	def test_download_repo_bad_repo_id_type(self):
		with self.assertRaises(TypeError):
			Hugging.download_repo(repo_id=[1,2,3], revision="test")

	def test_download_repo_bad_revision_type(self):
		with self.assertRaises(TypeError):
			Hugging.download_repo(repo_id="test", revision=1234.5)

	def test_download_repo_bad_allow_patterns_type(self):
		with self.assertRaises(TypeError):
			Hugging.download_repo(repo_id="test", revision="test",
				allow_patterns={"a":1,"b":2})

	def test_download_repo_bad_ignore_patterns_type(self):
		with self.assertRaises(TypeError):
			Hugging.download_repo(repo_id="test", ignore_patterns=1234.5)

	def test_download_repo_bad_local_dir_type(self):
		with self.assertRaises(TypeError):
			Hugging.download_repo(repo_id="test", local_dir=[12,34,"test"])

	def test_download_repo_pass(self):
		try:
			Hugging.download_repo(repo_id=public_repo_id())
		except Exception as e:
			self.fail(f"❌ unexpected exception: {e}")

	def test_download_repo_to_local_dir_pass(self):
		try:
			# downloading repo from hugging face
			_location = Hugging.download_repo(repo_id=public_repo_id(),
				local_dir="src/model_commons/hugging_face/temp_test_dir/")
			# fail test id file does not exist in the expected directory
			if "README.md" not in os.listdir("src/model_commons/hugging_face/temp_test_dir/"):
				self.fail("❌ an expected file was not found in src/model_commons/hugging_face/temp_test_dir/")
			dir_path = Path("src/model_commons/hugging_face/temp_test_dir")
			if dir_path.is_dir():
				shutil.rmtree(dir_path)
				dir_path.mkdir()
			else:
				self.fail("❌ src/model_commons/hugging_face/temp_test_dir is not a directory")
		except Exception as e:
			self.fail(f"❌ unexpected exception: {e}")

	def test_upload_file_bad_local_file_path_type(self):
		with self.assertRaises(TypeError):
			Hugging.upload_file(local_file_path=[1,2,3,4], repo_file_path="test",
				repo_id="test")

	def test_upload_file_bad_repo_file_path_type(self):
		with self.assertRaises(TypeError):
			Hugging.upload_file(local_file_path="test", repo_file_path={"a":1,"b":2},
				repo_id="test")

	def test_upload_file_bad_repo_id_type(self):
		with self.assertRaises(TypeError):
			Hugging.upload_file(local_file_path="test", repo_file_path="test",
				repo_is=1234)

	def test_upload_file_bad_repo_type_type(self):
		with self.assertRaises(TypeError):
			Hugging.upload_file(local_file_path="test", repo_file_path="test",
				repo_id="test", repo_type=[12,34])

	def test_upload_file_bad_token_type(self):
		with self.assertRaises(TypeError):
			Hugging.upload_file(local_file_path="src/model_commons/hugging_face/README.md",
				repo_file_path="README.md", repo_id=public_repo_id(), token=1234.56)

	def test_upload_file_bad_token_file_path_type(self):
		with self.assertRaises(TypeError):
			Hugging.upload_file(local_file_path="src/model_commons/hugging_face/README.md",
				repo_file_path="README.md", repo_id=public_repo_id(),
				token_file_path=[12,34,56,78])

	def test_upload_file_bad_local_file_path(self):
		with self.assertRaises(ValueError):
			Hugging.upload_file(local_file_path="src/model_commons/hugging_face/READM.md",
				repo_file_path="README.md", repo_id=public_repo_id(),
				token_file_path="src/model_commons/hugging_face/hugging/hugging_face_token.txt")

	def test_upload_file_pass(self):
		try:
			file_path = Path("src/model_commons/hugging_face/README.md")
			if not file_path.is_file():
				self.fail("❌ neccessary file at src/model_commons/hugging_face/README.md is not present")
			Hugging.upload_file(local_file_path="src/model_commons/hugging_face/README.md",
				repo_file_path="README.md", repo_id=public_repo_id())
		except Exception as e:
			self.fail(f"❌ received unexpected exception: {e}")

	def test_upload_file_with_token_file_path_pass(self):
		try:
			Hugging.upload_file(local_file_path="src/model_commons/hugging_face/README.md",
				repo_file_path="README.md", repo_id=public_repo_id(),
				token_file_path=token_file_path())	
		except Exception as e:
			self.fail(f"❌ receivied unexpected exception: {e}")

	def test_upload_file_with_token_pass(self):
		try:
			with open(token_file_path(), "r") as file:
				token = file.read().strip()
			Hugging.upload_file(local_file_path="src/model_commons/hugging_face/README.md",
				repo_file_path="README.md", repo_id=public_repo_id(),
				token=token)
		except Exception as e:
			self.fail(f"❌ receivied unexpected exception: {e}")

	def test_upload_folder_bad_local_folder_path_type(self):
		with self.assertRaises(TypeError):
			Hugging.upload_folder(local_folder_path=1234, repo_path="test", repo_id="test")

	def test_upload_folder_bad_repo_path_type(self):
		with self.assertRaises(TypeError):
			Hugging.upload_folder(local_folder_path="test", repo_path=[12,34], repo_id="test")

	def test_upload_folder_bad_repo_id_type(self):
		with self.assertRaises(TypeError):
			Hugging.upload_folder(local_folder_path="test", repo_path="test", repo_id=12.34)

	def test_upload_folder_bad_repo_type_type(self):
		with self.assertRaises(TypeError):
			Hugging.upload_folder(local_folder_path="test", repo_path="test", repo_id="test",
				repo_type={"a":1})

	def test_upload_folder_bad_ignore_patterns_type(self):
		with self.assertRaises(TypeError):
			Hugging.upload_folder(local_folder_path="test", repo_path="test", repo_id="test",
				ignore_patterns=123.45)

	def test_upload_folder_bad_allow_patterns_type(self):
		with self.assertRaises(TypeError):
			Hugging.upload_folder(local_folder_path="test", repo_path="test", repo_id="test",
				allow_patterns={"a":1,"b":2})

	def test_upload_folder_bad_delete_patterns_type(self):
		with self.assertRaises(TypeError):
			Hugging.upload_folder(local_folder_path="test", repo_path="test", repo_id="test",
				delete_patterns=1e-6)

	def test_upload_folder_bad_local_folder_path(self):
		with self.assertRaises(ValueError):
			Hugging.upload_folder(
				local_folder_path="src/model_commons/hugging_face/temp_test",
				repo_path="", repo_id=public_repo_id())

	def test_upload_folder_pass(self):
		try:
			Hugging.upload_folder(local_folder_path=local_folder_path(),
				repo_path="", repo_id=public_repo_id())
		except Exception as e:
			self.fail(f"❌ receivied unexpected exception: {e}")

	def test_upload_folder_with_token_file_path_pass(self):
		try:
			Hugging.upload_folder(local_folder_path=local_folder_path(),
				repo_path="", repo_id=public_repo_id(),
				token_file_path=token_file_path())
		except Exception as e:
			self.fail(f"❌ receivied unexpected exception: {e}")

	def test_upload_folder_with_token_pass(self):
		try:
			with open(token_file_path(), "r") as file:
				token = file.read().strip()
			Hugging.upload_folder(local_folder_path=local_folder_path(),
				repo_path="", repo_id=public_repo_id(),
				token=token)
		except Exception as e:
			self.fail(f"❌ receivied unexpected exception: {e}")

	def test_get_repo_info_bad_repo_id_type(self):
		with self.assertRaises(TypeError):
			Hugging.get_repo_info(repo_id=[1,2,3,4])

	def test_get_repo_info_pass(self):
		try:
			Hugging.get_repo_info(repo_id=public_repo_id())
		except Exception as e:
			self.fail(f"❌ receivied unexpected exception: {e}")

	def test_create_repo_bad_repo_id_type(self):
		with self.assertRaises(TypeError):
			Hugging.create_repo(repo_id=123445.5)

	def test_create_repo_bad_repo_type_type(self):
		with self.assertRaises(TypeError):
			Hugging.create_repo(repo_id=public_repo_id(), repo_type=[1,2,34])

	def test_create_repo_pass(self):
		try:
			Hugging.create_repo(repo_id=temp_repo_id())
		except Exception as e:
			self.fail(f"❌ receivied unexpected exception: {e}")

	def test_delete_repo_pass(self):
		try:
			Hugging.delete_repo(repo_id=temp_repo_id())
		except Exception as e:
			self.fail(f"❌ receivied unexpected exception: {e}")

	def test_create_pivate_repo_pass(self):
		try:
			Hugging.create_repo(repo_id=temp_private_repo_id(), private=True)
		except Exception as e:
			self.fail(f"❌ receivied unexpected exception: {e}")

	def test_delete_private_repo_pass(self):
		try:
			Hugging.delete_repo(repo_id=temp_private_repo_id())
		except Exception as e:
			self.fail(f"❌ receivied unexpected exception: {e}")

	def test_create_dataset_repo(self):
		try:
			Hugging.create_repo(repo_id=temp_dataset_repo_id(), repo_type="dataset")
		except Exception as e:
			self.fail(f"❌ receivied unexpected exception: {e}")

	def test_delete_dataset_repo(self):
		try:
			Hugging.delete_repo(repo_id=temp_dataset_repo_id(), repo_type="dataset")
		except Exception as e:
			self.fail(f"❌ receivied unexpected exception: {e}")

	def test_create_repo_bad_private_type(self):
		with self.assertRaises(TypeError):
			Hugging.create_repo(repo_id=public_repo_id(), private={"a":1,"b":2})

	def test_delete_repo_bad_repo_id_type(self):
		with self.assertRaises(TypeError):
			Hugging.delete_repo(repo_id=[1,24,4])

	def test_delete_repo_bad_repo_type_type(self):
		with self.assertRaises(TypeError):
			Hugging.delete_repo(repo_id=public_repo_id(), repo_type=123.7543)

	def test_get_model_card_bad_repo_id_type(self):
		with self.assertRaises(TypeError):
			Hugging.get_model_card(repo_id=[12,34,67])
	
	def test_get_model_card_bad_token_type(self):
		with self.assertRaises(TypeError):
			Hugging.get_model_card(repo_id=public_repo_id(),
				token={"a":1,"b":2})

	def test_get_model_card_bad_token_file_path_type(self):
		with self.assertRaises(TypeError):
			Hugging.get_model_card(repo_id=public_repo_id(),
				token_file_path=12344.245)

	def test_get_model_card_pass(self):
		try:	
			mc = Hugging.get_model_card(repo_id=public_repo_id())
			if not isinstance(mc, ModelCard):
				self.fail(f"❌ expected ModelCard type got {type(mc)}")
		except Exception as e:
			self.fail(f"❌ receivied unexpected exception: {e}")

	def test_push_model_card_bad_repo_id_type(self):
		model_card = Hugging.get_model_card(repo_id=public_repo_id())
		with self.assertRaises(TypeError):
			Hugging.push_model_card(repo_id=1234.5, model_card=model_card)

	def test_push_model_card_bad_model_card_type(self):
		with self.assertRaises(TypeError):
			Hugging.push_model_card(repo_id=public_repo_id(), model_card=["a","b","c"])

	def test_push_model_card_bad_token_file_path_type(self):
		model_card = Hugging.get_model_card(repo_id=public_repo_id())
		with self.assertRaises(TypeError):
			Hugging.push_model_card(repo_id=public_repo_id(), model_card=model_card,
				token_file_path={"a":"b","c":"d"})

	def test_push_model_card_bad_token_type(self):
		model_card = Hugging.get_model_card(repo_id=public_repo_id())
		with self.assertRaises(TypeError):
			Hugging.push_model_card(repo_id=public_repo_id(), model_card=model_card,
				token=12345.78)

	def test_push_model_card_pass(self):
		model_card = Hugging.get_model_card(repo_id=public_repo_id())
		Hugging.push_model_card(repo_id=public_repo_id(), model_card=model_card,
			token_file_path=token_file_path())

def public_repo_id() -> str:
	return "NickCliffel/PublicUCATestRepo"

def temp_repo_id() -> str:
	return "NickCliffel/TempRepo"

def temp_private_repo_id() -> str:
	return "NickCliffel/TempPrivateRepo"

def temp_dataset_repo_id() -> str:
	return "NickCliffel/TempDatasetRepo"

def token_file_path() -> str:
	return "src/model_commons/hugging_face/hugging_face_token.txt"

def local_folder_path() -> str:
	return "src/model_commons/hugging_face/temp_test_dir/"
