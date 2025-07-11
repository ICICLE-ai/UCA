from abc import abstractmethod

from src.imt_component import IMTComponent


class SmartScheduler(IMTComponent):
	@abstractmethod
	def validate_inputs():
		pass

	@abstractmethod
	def estimate():
		pass

	@abstractmethod
	def select_best_system():
		pass

	@abstractmethod
	def monitor_service():
		pass

	@abstractmethod
	def stop_service():
		pass
