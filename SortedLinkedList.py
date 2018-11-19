class Node:
	def __init__(self, element):
		self.element = element
		self.next = None

	def __str__(self):
		return self.element.__str__()

	def __repr__(self):
		return self.element.__repr__()


class SortedLinkedList:
	def __init__(self):
		self.head = None
		self.count = 0

	def __len__(self):
		return self.count

	def __iter__(self):
		current = self.head
		while current is not None:
			yield current.element
			current = current.next

	def __add__(self, other):
		new = SortedLinkedList()
		for n in self:
			new.add(n)
		for n in other:
			new.add(n)
		return new

	def get(self, index):
		if index < 0 or index > self.count:
			raise IndexError()

		aux = self.head
		for i in range(index):
			aux = aux.next

		return aux.element

	def get_next(self, element):
		if self.head is None:
			return None

		aux = self.head
		while aux.element != element:
			aux = aux.next

		if aux is None or aux.next is None:
			return None

		return aux.next.element

	def index_of(self, element):
		if self.head is None:
			return -1

		index = 0
		aux = self.head
		while aux.element != element:
			aux = aux.next
			index += 1
			if aux is None:
				return -1

		return index

	def add(self, element):
		node = Node(element)

		if self.count == 0:
			self.head = node
			self.count += 1
			return

		aux = self.head
		prev = None
		while aux is not None and aux.element < element:
			prev = aux
			aux = aux.next

		if aux == self.head:
			node.next = self.head
			self.head = node
			self.count += 1
			return

		node.next = aux
		prev.next = node
		self.count += 1

	def remove(self, element):
		if self.head is None:
			return False

		aux = self.head
		prev = None
		while aux.element != element:
			prev = aux
			aux = aux.next
			if aux is None:
				return False

		if aux == self.head:
			self.head = self.head.next
		else:
			prev.next = aux.next

		self.count -= 1
		return True

	def remove_by_index(self, index):
		if index < 0 or index > self.count:
			raise IndexError()

		aux = self.head
		prev = None
		for i in range(index - 1):
			prev = aux
			aux = aux.next

		if aux == self.head:
			self.head = self.head.next
		else:
			prev.next = aux.next

		self.count -= 1

	def __str__(self):
		s = ""
		aux = self.head
		while aux is not None:
			s += aux.element.__repr__()
			if aux.next is not None:
				s += ", "
			aux = aux.next

		return s
