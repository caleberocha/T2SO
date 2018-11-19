class NoFreeBlockError(Exception):
	def __init__(self):
		self.message = "Não há memória suficiente para alocar."

	def __str__(self):
		return repr(self.message)


class FragmentationError(Exception):
	def __init__(self):
		self.message = "Ocorreu uma fragmentação externa."

	def __str__(self):
		return repr(self.message)


class NoInstructionsError(Exception):
	def __init__(self):
		self.value = "Não há instruções."

	def __str__(self):
		return repr(self.value)


class InvalidIntervalError(Exception):
	def __init__(self):
		self.value = "Intervalo de memória inválido."

	def __str__(self):
		return repr(self.value)
