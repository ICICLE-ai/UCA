from colorama import Fore, Back, Style, init
import unittest
from src.patra.unit_test import TestValidatorClass
from src.patra.unit_test import TestAIModelWrapperClass
from src.patra.unit_test import TestModelCardWrapperClass

if __name__ == "__main__":
	# auto resetting colorama color
	init(autoreset=True)

	# testing the Validator class in the src/patra/validator.py file	
	print(Fore.MAGENTA + Style.BRIGHT + "running test for patra Validator class")
	validatorTestSuite = unittest.TestLoader().loadTestsFromTestCase(TestValidatorClass)
	unittest.TextTestRunner(verbosity=2).run(validatorTestSuite)
	print()
	
	# testing the AIModelWrapper class in the src/patra/ai_model_wrapper.py file
	print(Fore.CYAN + Style.BRIGHT + "running test for patra ai model wrapper class")
	aiModelTestSuite = unittest.TestLoader().loadTestsFromTestCase(TestAIModelWrapperClass)
	unittest.TextTestRunner(verbosity=2).run(aiModelTestSuite)
	print()

	# testing the ModelCardWrapper class in the src/patra/model_card_wrapper.py file
	print(Fore.MAGENTA + Style.BRIGHT + "running test for model card wrapper class")
	modelCardTestSuite = unittest.TestLoader().loadTestsFromTestCase(TestModelCardWrapperClass)
	unittest.TextTestRunner(verbosity=2).run(modelCardTestSuite)
