import os
import re

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
		self.value = "Não há instruções"
		 
	def __str__(self):
		return repr(self.value)

class Block:
	id = 0
	start = 0
	end = 0

	def __init__(self, id, start, end):
		self.id = int(id)
		self.start = int(start)
		self.end = int(end)

	def __eq__(self, other):
		if other == None:
			return False
		return self.start == other.start
	
	def __lt__(self, other):
		if other == None:
			return False
		return self.start < other.start

	def __str__(self):
		#return "B(" + str(self.id) + ", " + str(self.start) + ", " + str(self.end) + ")"
		return "{0:9s}    Bloco {1}".format(str(self.start) + "-" + str(self.end), self.id)

	def __repr__(self):
		return "B(" + str(self.id) + ", " + str(self.start) + ", " + str(self.end) + ")"

class FreeBlock:
	start = 0
	end = 0

	def __init__(self, start, end):
		self.start = int(start)
		self.end = int(end)

	def __eq__(self, other):
		if other == None:
			return False
		return self.start == other.start
	
	def __lt__(self, other):
		if other == None:
			return False
		return self.start < other.start
	
	def __str__(self):
		#return "F(" + str(self.start) + ", " + str(self.end) + ")"
		return "{0:9s}    Livre".format(str(self.start) + "-" + str(self.end))

	def __repr__(self):
		return "F(" + str(self.start) + ", " + str(self.end) + ")"

class MemoryManager:

	mi = 0
	mf = 0
	free_blocks = []
	blocks = []
	index = 0
	free_memory = 0

	def __init__(self, mi, mf):
		self.mi = int(mi)
		self.mf = int(mf)
		if mi >= mf:
			raise "Intervalo de memória inválido."

		self.free_blocks.append(FreeBlock(mi, mf))
		self.free_memory = self.mf - self.mi

	def count_free_memory(self):
		free = 0
		for block in self.free_blocks:
			free += block.end - block.start

		return free

	def add_block(self, size):
		self.index += 1
		size = int(size)
		
		block_removed = None
		start = -1
		for free_block in self.free_blocks:
			if free_block.end >= free_block.start + size:
				start = free_block.start
				block_removed = free_block

		if start == -1:
			if self.free_memory >= size:
				raise FragmentationError()
			raise NoFreeBlockError()

		new_block = Block(self.index, start, start + size)

		self.blocks.append(new_block)
		self.free_blocks.remove(block_removed)
		if block_removed.start < new_block.start:
			self.free_blocks.append(FreeBlock(block_removed.start, new_block.start))
		if new_block.end < block_removed.end:
			self.free_blocks.append(FreeBlock(new_block.end, block_removed.end))
		
		self.sort()

	def remove_block(self, id):
		id = int(id)
		b = None
		for block in self.blocks:
			if block.id == id:
				b = block
				self.blocks.remove(block)
		if b != None:
			self.free_blocks.append(FreeBlock(b.start, b.end))
		self.sort()
		self.optimize_free_blocks()
		
	def sort(self):
		self.blocks.sort()
		self.free_blocks.sort()
		
	def optimize_free_blocks(self):
		for i in range(len(self.free_blocks) - 1):
			if self.free_blocks[i].end == self.free_blocks[i+1].start:
				self.free_blocks[i].end = self.free_blocks[i+1].end
				self.free_blocks.pop(i+1)
		
with open("example.txt", "r", encoding="utf-8") as file:
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
			all_blocks = memory.blocks + memory.free_blocks
			all_blocks.sort()
			[print(b) for b in all_blocks]

		except NoFreeBlockError as e:
			print(e.message)
		print()

		#print("Processos:    " + str(memory.blocks))
		#print("Mem. livre:   " + str(memory.free_blocks))
		#print()
