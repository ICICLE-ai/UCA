import unittest

from colorama import Fore, Style, init

from src.database.cyber_infra.cyber_infra_unit_test import TestCyberInfraClient
from src.database.rules_engine.rules_engine_unit_test import TestRuleEngineClient
from src.model_commons.hugging_face.hugging_unit_test import TestHuggingClass
from src.model_commons.ml_hub.ml_hub_caller_unit_test import TestMLHubCallerClass
from src.model_commons.patra.ai_model_wrapper_unit_test import TestAIModelWrapperClass
from src.model_commons.patra.model_card_wrapper_unit_test import TestModelCardWrapperClass
from src.model_commons.patra.validator_unit_test import TestValidatorClass

if __name__ == "__main__":
	# auto resetting colorama color
	init(autoreset=True)

	# testing the Validator class in the src/model_commons/patra/validator.py file	
	print(Fore.MAGENTA + Style.BRIGHT + "running test for patra Validator class")
	validator_test_suite = unittest.TestLoader().loadTestsFromTestCase(TestValidatorClass)
	unittest.TextTestRunner(verbosity=2).run(validator_test_suite)
	print()
	
	# testing the AIModelWrapper class in the src/model_commons/patra/ai_model_wrapper.py file
	print(Fore.CYAN + Style.BRIGHT + "running test for patra ai model wrapper class")
	ai_model_test_suite = unittest.TestLoader().loadTestsFromTestCase(TestAIModelWrapperClass)
	unittest.TextTestRunner(verbosity=2).run(ai_model_test_suite)
	print()

	# testing the ModelCardWrapper class in the src/model_commons/patra/model_card_wrapper.py file
	print(Fore.MAGENTA + Style.BRIGHT + "running test for model card wrapper class")
	model_card_test_suite = unittest.TestLoader().loadTestsFromTestCase(TestModelCardWrapperClass)
	unittest.TextTestRunner(verbosity=2).run(model_card_test_suite)
	print()

	# testing the MLHubCaller class in then src/model_commons/ml_hub/ml_hub_caller.py file
	print(Fore.CYAN + Style.BRIGHT + "running test for ml hub caller class")
	ml_hub_caller_test_suite = unittest.TestLoader().loadTestsFromTestCase(TestMLHubCallerClass)
	unittest.TextTestRunner(verbosity=2).run(ml_hub_caller_test_suite)
	print()

	# testing the Hugging calss in the src/model_commons/hugging_face/hugging.py file
	print(Fore.CYAN + Style.BRIGHT + "running test for hugging class")
	hugging_test_suite = unittest.TestLoader().loadTestsFromTestCase(TestHuggingClass)
	unittest.TextTestRunner(verbosity=2).run(hugging_test_suite)
	print()
	
	# testing the RuleEngineClient class in then src/database/rules_engine/rules_engine_client.py file
	print(Fore.CYAN + Style.BRIGHT + "running test for rules engine class")
	rules_engine_test_suite = unittest.TestLoader().loadTestsFromTestCase(TestRuleEngineClient)
	unittest.TextTestRunner(verbosity=2).run(rules_engine_test_suite)
	print()

	# testing the cyberInfraClient class in then src/database/cyber_infra/cyber_infra_client.py file
	print(Fore.CYAN + Style.BRIGHT + "running test for cyber infra class")
	cyber_infra_test_suite = unittest.TestLoader().loadTestsFromTestCase(TestCyberInfraClient)
	unittest.TextTestRunner(verbosity=2).run(cyber_infra_test_suite)
	print()
