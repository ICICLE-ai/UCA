from abc import ABC, abstractmethod


class IMTComponent(ABC):
	@abstractmethod
	def start():
		pass

	@abstractmethod
	def stop():
		pass

	@abstractmethod
	def terminate():
		pass

	@abstractmethod
	def restart():
		pass
