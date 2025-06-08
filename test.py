import unittest
from src.patra.unit_test import TestValidatorClass
from src.patra.unit_test import TestAIModelWrapperClass

if __name__ == "__main__":
	# testing the Validator class in the src/patra/validator.py file
	validatorTestSuite = unittest.TestLoader().loadTestsFromTestCase(TestValidatorClass)
	unittest.TextTestRunner(verbosity=2).run(validatorTestSuite)
	
	# testing the AIModelWrapper class in the src/patra/ai_model_wrapper.py file
	aiModelTestSuite = unittest.TestLoader().loadTestFromTestCase(TestAIModelWrapperClass)
	unittest.TextTestRunner(verbosity=2).run(aiModelTestSuite)
