from src.model_commons.patra.validator import Validator
from src.imt_component import IMTComponent

class SmartScheduler(IMTComponent):
	@abstartmethod
	def ValidateInputs():
		pass

	@abstractmethod
	def Estimate():
		pass

	@abstractmethod
	def SelectBestSystem():
		pass

	@abstractmethod
	def MonitorService():
		pass

	@abstractmethod
	def StopService():
		pass
