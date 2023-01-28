# Derived from https://stackoverflow.com/questions/19472530/representing-graphs-data-structure-in-python
from collections import defaultdict
from Classes.atom import Atom

class Graph:
	def __init__(self, bonds):
		self._graph = defaultdict(set)
		self.add_bonds(bonds)

	def add_bonds(self, bonds):
		pass
		# Add bonds (list of tuple pairs) to the graph
		# for bond in bonds:
		# 	self.add(bond.atomOne, bond.atomTwo)
	
	def add(self, atomOne, atomTwo):
		#add connection between atomOne and atomTwo
		self._graph[atomOne].add(atomTwo)  
		self._graph[atomTwo].add(atomOne)
	
	def remove_bonds(self, atomOne):
		#remove all references to atom
		print('test')
	
	def testing_one(self):
		print('works')
		