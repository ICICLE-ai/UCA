from abc import ABC, abstractmethod


class IMTComponent(ABC):
	# starts component operation
	@abstractmethod
	def start():
		pass

	# gracefully stops the component operation
	@abstractmethod
	def stop():
		pass

	# forcefully stops the component operation
	@abstractmethod
	def terminate():
		pass

	# chains stop function and start function
	# while allowing for custom functionality
	@abstractmethod
	def restart():
		pass
