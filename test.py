from colorama import Fore, Back, Style, init
import unittest
from src.model_commons.patra.validator_unit_test import TestValidatorClass
from src.model_commons.patra.ai_model_wrapper_unit_test import TestAIModelWrapperClass
from src.model_commons.patra.model_card_wrapper_unit_test import TestModelCardWrapperClass
from src.model_commons.ml_hub.ml_hub_caller_unit_test import TestMLHubCallerClass

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
	print()

	# testing the MLHubCaller class in then src/model_commons/ml_hub/ml_hub_caller.py file
	print(Fore.CYAN + Style.BRIGHT + "running test for ml hub caller class")
	mlHubCallerTestSuite = unittest.TestLoader().loadTestsFromTestCase(TestMLHubCallerClass)
	unittest.TextTestRunner(verbosity=2).run(mlHubCallerTestSuite)
