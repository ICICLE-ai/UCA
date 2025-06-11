from abc import ABC, abstractmethod

class IMTComponent(ABC):
	@abstractmethod
	def Start():
		pass

	@abstractmethod
	def Terminate():
		pass

	@abstractmethod
	def Restart():
		pass
