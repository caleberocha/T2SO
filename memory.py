import sys
import re
from SortedLinkedList import SortedLinkedList
from Errors import *
from queue import Queue


class Block:
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
	def __init__(self, index, size):
		self.index = index
		self.size = size

	def __str__(self):
		return str(self.index) + " " + str(self.size)

	def __repr__(self):
		return self.__str__()


class MemoryManager:
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
		free = 0
		for block in self.free_blocks:
			free += (block.end - block.start)

		self.free_memory = free

	def add_block(self, size, index=None):
		if index is None:
			self.index += 1
		size = int(size)

		block_removed = None
		start = -1
		for free_block in self.free_blocks:
			if free_block.end >= free_block.start + size:
				start = free_block.start
				block_removed = free_block

		if start == -1:
			self.pending_blocks.put(PendingBlock(self.index, size))
			if self.free_memory >= size:
				raise FragmentationError()
			raise NoFreeBlockError()

		i = self.index
		if index is not None:
			i = index
		new_block = Block(i, start, start + size)

		self.blocks.add(new_block)
		self.free_blocks.remove(block_removed)
		if block_removed.start < new_block.start:
			self.free_blocks.add(FreeBlock(block_removed.start, new_block.start))
		if new_block.end < block_removed.end:
			self.free_blocks.add(FreeBlock(new_block.end, block_removed.end))

		self.count_free_memory()

	def remove_block(self, id):
		id = int(id)
		b = None
		for block in self.blocks:
			if block.id == id:
				b = block
				self.blocks.remove(block)
		if b is not None:
			self.free_blocks.add(FreeBlock(b.start, b.end))

		self.optimize_free_blocks()

		if not self.pending_blocks.empty():
			p = self.pending_blocks.get()
			print("Inserindo bloco pendente " + str(p))
			self.add_block(p.size, p.index)

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

for line in file:
	m = regex.match(line)
	if m:
		line_number += 1
		l = m.group(1)
		if line_number == 1:
			pass
		elif line_number == 2:
			mi = l
		elif line_number == 3:
			mf = l
		else:
			ins.append(l)

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
		elif command[0] == "L":
			print("Liberando bloco")
			memory.remove_block(command[1])
	except FragmentationError as e:
		print(e.message)
		print("Estado da memória:")
		[print(b) for b in memory.blocks + memory.free_blocks]

	except NoFreeBlockError as e:
		print(e.message)
	print()

# print("Blocos:    " + str(memory.blocks))
# print("Livre:     " + str(memory.free_blocks))
# print("Pendentes: " + str(list(memory.pending_blocks.queue)))
# print(str(memory.free_memory) + " bytes livres")
# print()
