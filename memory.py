import sys
import re
import os
import random
from SortedLinkedList import SortedLinkedList
from Errors import *
from queue import Queue


class Block:
	"""
	Representação de um bloco de memória.

	Atributos:
		id       Identificador do bloco
		start    Endereço do ínicio do bloco
		end      Endereço do final do bloco
	"""
	def __init__(self, id, start, end):
		self.id = int(id)
		self.start = int(start)
		self.end = int(end)

	def __eq__(self, other):
		if other is None:
			return False
		return self.start == other.start

	def __lt__(self, other):
		if other is None:
			return False
		return self.start < other.start

	def __str__(self):
		# return "B(" + str(self.id) + ", " + str(self.start) + ", " + str(self.end) + ")"
		return "{0:9s}    Bloco {1}".format(str(self.start) + "-" + str(self.end), self.id)

	def __repr__(self):
		return "B(" + str(self.id) + ", " + str(self.start) + ", " + str(self.end) + ")"


class FreeBlock:
	"""
	Representação de um bloco de memória livre.
	
	Atributos:
		start    Endereço do ínicio do bloco
		end      Endereço do final do bloco
	"""
	def __init__(self, start, end):
		self.start = int(start)
		self.end = int(end)

	def __eq__(self, other):
		if other is None:
			return False
		return self.start == other.start

	def __lt__(self, other):
		if other is None:
			return False
		return self.start < other.start

	def __str__(self):
		# return "F(" + str(self.start) + ", " + str(self.end) + ")"
		return "{0:9s}    Livre".format(str(self.start) + "-" + str(self.end))

	def __repr__(self):
		return "F(" + str(self.start) + ", " + str(self.end) + ")"


class PendingBlock:
	"""
		Bloco que está pendente para inclusão da memória.
		Atributos:
			index    Identificador do bloco
			size     Tamanho do bloco
	"""
	def __init__(self, index, size):
		self.index = index
		self.size = size

	def __str__(self):
		return str(self.index) + " " + str(self.size)

	def __repr__(self):
		return self.__str__()


class MemoryManager:
	"""
	Representação do gerenciador de memória.
	Atributos:
		mi                Endereço inicial
		mf                Endereço final
		blocks            Blocos ocupados
		free_blocks       Blocos livres
		free_memory       Quantidade de memória livre
		pending_blocks    Blocos pendentes
		index             Identificador dos blocos. A cada bloco inserido, é incrementado em 1
	"""
	def __init__(self, mi, mf):
		self.mi = int(mi)
		self.mf = int(mf)
		if mi >= mf:
			raise InvalidIntervalError()
		self.blocks = SortedLinkedList()
		self.free_blocks = SortedLinkedList()
		self.free_blocks.add(FreeBlock(self.mi, self.mf))
		self.free_memory = self.mf - self.mi
		self.index = 0
		self.pending_blocks = Queue()

	def count_free_memory(self):
		"""
		Conta a memória livre e atualiza o atributo free_memory.
		"""
		free = 0
		for block in self.free_blocks:
			free += (block.end - block.start)

		self.free_memory = free

	def add_block(self, size, index=None):
		"""
		Aloca espaço e adiciona um bloco à memória.
		"""
		if index is None:
			self.index += 1
		size = int(size)

		# Verifica se há memória disponível. Se houver, a variável start é atualizada com o endereço inicial do bloco livre
		block_removed = None
		start = -1
		for free_block in self.free_blocks:
			if free_block.end >= free_block.start + size:
				start = free_block.start
				block_removed = free_block

		# Caso não haja memória disponível, adiciona à fila de pendentes e
		# lança a exceção FragmentationError se houver fragmentação externa, ou NoFreeBlockError se não houver espaço disponível.
		if start == -1:
			self.pending_blocks.put(PendingBlock(index or self.index, size))
			if self.free_memory >= size:
				raise FragmentationError()
			raise NoFreeBlockError()

		new_block = Block(index or self.index, start, start + size)

		# Adiciona o bloco
		self.blocks.add(new_block)
		# Remove o bloco livre
		self.free_blocks.remove(block_removed)
		# Cria e insere nenhum, um ou dois blocos livres, dependendo do bloco inserido
		if block_removed.start < new_block.start:
			self.free_blocks.add(FreeBlock(block_removed.start, new_block.start))
		if new_block.end < block_removed.end:
			self.free_blocks.add(FreeBlock(new_block.end, block_removed.end))

		# Atualiza a quantidade de memória disponível
		self.count_free_memory()

	def remove_block(self, id):
		"""
		Remove um bloco da memória, liberando espaço.
		"""

		# Procura o bloco
		id = int(id)
		b = None
		for block in self.blocks:
			if block.id == id:
				b = block
				self.blocks.remove(block)
		if b is not None:
			# Cria um bloco livre correspondente ao bloco removido
			self.free_blocks.add(FreeBlock(b.start, b.end))
		else:
			# Bloco não encontrado
			raise BlockNotFoundError()

		# Reorganiza os blocos livres
		self.optimize_free_blocks()

	def optimize_free_blocks(self):
		aux = self.free_blocks.head
		while aux is not None:
			node = aux
			while node.next is not None and aux.element.end >= node.next.element.start:
				aux.element.end = node.next.element.end
				node = node.next
				self.free_blocks.remove(node.element)
			aux = aux.next

		self.count_free_memory()

	def check_pending_blocks(self):
		# Verifica se há blocos pendentes
		pending_blocks_count = self.pending_blocks.qsize()
		if pending_blocks_count > 0:
			# Tenta inserir todos os blocos pendentes na memória.
			# Os que não puderem ser inseridos voltam para a fila
			c = 0
			while c < pending_blocks_count:
				p = self.pending_blocks.get()
				print("Inserindo bloco pendente " + str(p))
				try:
					self.add_block(p.size, p.index)
					print("Bloco inserido")
				except (FragmentationError, NoFreeBlockError) as e:
					print(e.message)
				finally:
					c += 1

	def print_pending_blocks(self):
		return os.linesep.join([q.__str__() for q in list(self.pending_blocks.queue)])

	def __str__(self):
		return os.linesep.join([b.__str__() for b in self.blocks + self.free_blocks])

	def __repr__(self):
		return self.__str__()


def generate_block():
	return "S " + str(random.randrange(50, 1000, 50))

def generate_removal():
	return "L " + str(random.randint(0, 20))

def generate_random_instructions():
	"""
	Gera instruções para o gerenciador de memória aleatoriamente.
	
	O espaço de memória a ser criado vai de 0-500 a 600-10000.

	São geradas de 5 a 50 instruções. Cada instrução pode ser "S 50-1000" (com intervalo de 50) ou "L 0-20".

	"""
	mi = random.randrange(0, 500, 50)
	mf = random.randrange(600, 10000, 50)
	ins = []
	for i in range(random.randint(5, 50)):
		ins.append(generate_block() if random.randint(0,1) == 1 else generate_removal())

	return (mi, mf, ins)

def usage():
	print("Uso: " + sys.argv[0] + " arquivo")

if len(sys.argv) < 2:
	usage()
	quit(1)

filename = sys.argv[1]
try:
	file = open(filename, "r", encoding="utf-8")
except IOError as e:
	print(e)
	quit(1)

line_number = 0
regex = re.compile(r"^([0-9]+|[SL] [0-9]+)\s*?(?://.*|$)", re.I)
mi = -1
mf = -1
ins = []
random_mode = False

for line in file:
	m = regex.match(line)
	if m:
		line_number += 1
		l = m.group(1)
		if line_number == 1:
			if l == str(2):
				random_mode = True
				break
		elif line_number == 2:
			mi = l
		elif line_number == 3:
			mf = l
		else:
			ins.append(l)
			
if random_mode:
	mi, mf, ins = generate_random_instructions()
	print("Comandos gerados aleatoriamente:")
	print(mi)
	print(mf)
	[print(l) for l in ins]
	print()

if mi == -1 or mf == -1 or len(ins) < 1:
	raise NoInstructionsError()

memory = MemoryManager(mi, mf)
for line in ins:
	print("Comando: " + line)
	command = line.split(" ")
	try:
		if command[0] == "S":
			print("Inserindo bloco")
			memory.add_block(command[1])
			print("Bloco inserido")
		elif command[0] == "L":
			print("Liberando bloco")
			memory.remove_block(command[1])
			print("Bloco liberado")
			memory.check_pending_blocks()
	except FragmentationError as e:
		print(e.message)
		print("Estado da memória:")
		print(memory)
	except (NoFreeBlockError, BlockNotFoundError) as e:
		print(e.message)
	print()

	# print(memory.blocks)
	# print(memory.free_blocks)
	# print(list(memory.pending_blocks.queue))

print("Estado final da memória:")
print(memory)
print()
print("Blocos pendentes: ")
print(memory.print_pending_blocks())
print()
print(str(memory.free_memory) + " bytes livres")
print()
