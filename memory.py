import os
import re

class NoFreeBlockError(Exception):
	def __init__(self, value):
         self.value = value

     def __str__(self):
        return repr(self.value)

class BlockTooLargeError(Exception):
	def __init__(self, value):
         self.value = value
		 
     def __str__(self):
        return repr(self.value)

class FragmentationError(Exception):
	def __init__(self, value):
         self.value = value
		 
     def __str__(self):
        return repr(self.value)

class Block:
	id = 0
	start = 0
	end = 0

	def __init__(self, id, start, end):
		self.id = id
		self.start = start
		self.end = end

class FreeBlock:
	start = 0
	end = 0

	def __init__(self, start, end):
		self.start = start
		self.end = end

class MemoryManager:

	mi = 0
	mf = 0
	free_memory = []
	blocks = []
	index = 0

	def __init__(self, mi, mf):
		self.mi = mi
		self.mf = mf
		if mi >= mf:
			raise "Intervalo de memória inválido."

		free_memory.append(FreeBlock(mi, mf))

	def count_free_memory(self):
		free = 0
		for block in free_memory:
			free += block.end - block.start

		return free

	def add_block(self, start, end):
		index += 1
		new_block = Block(index, start, end)

		i = -1
		for a in range(len(free_memory)):
			if new_block.start >= free_memory[a].start:
				i = a
				break

		if i == -1:
			raise NoFreeBlockError()

		if new_block.end - new.block.start > count_free_memory():
			if free_memory[i].end < new_block.end:
				raise BlockTooLargeError()
			else:
				raise FragmentationError()

		blocks.append(new_block)
		block_removed = free_memory.pop(i)	
		free_memory.append(FreeBlock(block_removed.start, new_block.start))
		free_memory.append(FreeBlock(new_block.end, block_removed.end))
		
with open("example.txt", "r") as file:
	regex = re.compile(r"(.*?)\s*?//.*")
	for line in file:
		l = line.replace()