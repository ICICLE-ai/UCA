import unittest
import os
from pathlib import Path
import shutil
from src.model_commons.hugging_face.hugging import Hugging

class TestHuggingClass(unittest.TestCase):
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

	def test_upload_file_pass(self):
		try:
			Hugging.UploadFile(local_file_path="src/model_commons/hugging_face/test_file.txt",
				repo_file_path="README.md", repo_id=PublicRepoId())
		except Exception as e:
			self.fail(f"❌ received unexpected exception: {e}")

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

	def test_upload_folder_pass(self):
		raise NotImplementedError()

def PublicRepoId() -> str:
	return "NickCliffel/PublicUCATestRepo"
