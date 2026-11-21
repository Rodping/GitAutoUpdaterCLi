import os
import tempfile
import unittest

from python_scripts.variables import TempVariables


class TempVariablesTests(unittest.TestCase):
    def test_values_persist_and_can_be_deleted(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_name = os.path.join(temp_dir, "temp_variables.json")
            variables = TempVariables(file_name=file_name)

            variables.set_value("REPO_URL", "https://example.com/repo.git")

            loaded_variables = TempVariables(file_name=file_name)
            self.assertEqual(
                loaded_variables.get_value("REPO_URL"),
                "https://example.com/repo.git",
            )
            self.assertTrue(loaded_variables.delete_value("REPO_URL"))

            reloaded_variables = TempVariables(file_name=file_name)
            self.assertEqual(reloaded_variables.get_value("REPO_URL"), "")


if __name__ == "__main__":
    unittest.main()
