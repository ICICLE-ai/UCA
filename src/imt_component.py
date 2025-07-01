from abc import ABC, abstractmethod

class IMTComponent(ABC):
	@abstractmethod
	def Start():
		pass

	@abstractmethod
	def Stop():
		pass

	@abstractmethod
	def Terminate():
		pass

	@abstractmethod
	def Restart():
		pass
