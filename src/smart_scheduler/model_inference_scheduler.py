from src.model_commons.patra.validator import Validator
from src.imt_component import IMTComponent
from src.smart_scheduler.smart_scheduler import SmartScheduler

class ModeInferneceScheduler(SmartScheduler):
	def __init__(self, inputs:dict):
		self.inputs = inputs

	def ValidateInputs(self):
		raise NotImplementedError("ValidateInputs function has yet to be implemented")

	def Estimate(self):
		raise NotImplementedError("Estimate function has yet to be implemented")

	def SelectBestSystem(self):
		raise NotImplementedError("SelectBestSystem has yet to be implemented")

	def MonitorService(self):
		raise NotImplementedError("MonitorService has yet to be implemented")

	def StopService(self):
		raise NotImplementedError("StopService has yet to be implemented")

	def Start(self):
		raise NotImplementedError("Start has yet to be implemented")

	def Terminate(self):
		raise NotImplementedError("Terminate has yet to be implemented")

	def Restart(self):
		raise NotImplementedError("Restart has yet to be implemented")
