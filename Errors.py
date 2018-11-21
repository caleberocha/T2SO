class Error(Exception):
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return repr(self.message)

class NoFreeBlockError(Error):
	def __init__(self):
		self.message = "Não há memória livre suficiente para alocar."


class FragmentationError(Error):
	def __init__(self):
		self.message = "Ocorreu uma fragmentação externa."


class NoInstructionsError(Error):
	def __init__(self):
		self.message = "Não há instruções."


class InvalidIntervalError(Error):
	def __init__(self):
		self.message = "Intervalo de memória inválido."


class BlockNotFoundError(Error):
	def __init__(self):
		self.message = "Bloco não encontrado."
