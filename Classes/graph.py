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
			self.add_bond(atom_one, atom_two, bond)

	def add_bond(self, atom_one: Atom, atom_two: Atom, bond: Bond):
		# add dictionary entry
		self.graph[atom_one].add((atom_two, bond))  
		self.graph[atom_two].add((atom_one, bond))
	
	def remove_bonds(self, atom_one: Atom):
		#remove all references to atom
		print('test')
	
	def __str__(self):
		tempStr = ''

		for key in self.graph.keys():
			tempStr = tempStr + str(key) + ' : \n{\n'
			# enumerate since sets are not iterable
			for index, atom_bond in enumerate(self.graph[key]):
				if index == len(self.graph[key]) - 1:
					tempStr = tempStr + "\t" + str(atom_bond[0]) + " " + str(atom_bond[1])
				else:
					tempStr = tempStr + "\t" + str(atom_bond[0]) + " " + str(atom_bond[1]) + ",\n"
			
			tempStr += "\n}\n\n"
		return tempStr
		
