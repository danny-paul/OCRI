# Derived from https://stackoverflow.com/questions/19472530/representing-graphs-data-structure-in-python
from collections import defaultdict
from Classes.atom import Atom
from Classes.bonds import Bond	

class Graph:
	def __init__(self, bonds: list[Bond]):
		self.graph = defaultdict(set)
		self.add_bonds(bonds)

	def add_bonds(self, bonds: list[Bond]):
		for bond in bonds:
			atom_one, atom_two = bond.get_atoms()
			self.add_atoms(atom_one, atom_two)
	
	def add_atoms(self, atom_one: Atom, atom_two: Atom):
		# add dictionary entry
		self.graph[atom_one].add(atom_two)  
		self.graph[atom_two].add(atom_one)
	
	def remove_bonds(self, atom_one: Atom):
		#remove all references to atom
		print('test')
	
	def testing_one(self):
		print('works')
	
	def __str__(self):
		return '{}({})'.format(self.__class__.__name__, dict(self.graph))