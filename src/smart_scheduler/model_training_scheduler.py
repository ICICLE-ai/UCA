from src.smart_scheduler.smart_scheduler import SmartScheduler


class ModelTrainingScheduler(SmartScheduler):
	def __init__(self, inputs:dict):
		self.inputs = inputs

	def validate_inputs(self):
		raise NotImplementedError("ValidateInputs function has yet to be implemented")

	def estimate(self):
		raise NotImplementedError("Estimate function has yet to be implemented")

	def select_best_system(self):
		raise NotImplementedError("SelectBestSystem has yet to be implemented")

	def monitor_service(self):
		raise NotImplementedError("MonitorService has yet to be implemented")

	def stop_service(self):
		raise NotImplementedError("StopService has yet to be implemented")

	def start(self):
		raise NotImplementedError("Start has yet to be implemented")

	def terminate(self):
		raise NotImplementedError("Terminate has yet to be implemented")

	def restart(self):
		raise NotImplementedError("Restart has yet to be implemented")
