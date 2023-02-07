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
			self.add_bond(bond)

	def add_bond(self, bond: Bond):
		atom_one, atom_two = bond.get_atoms()
		# add dictionary entry
		self.graph[atom_one].add((atom_two, bond))  
		self.graph[atom_two].add((atom_one, bond))

	def remove_bonds(self, reference_atom: Atom):
		# remove all bonds to a given atom, restore valence electrons to atoms- atoms are preserved, bonds are deleted
		for atom_bond_tuple in self.graph[reference_atom]:
			connected_atom = atom_bond_tuple[0]
			bond: Bond = atom_bond_tuple[1]
			bond.delete_bond()
			



	def remove_bond(self, bond: Bond):
		# remove bond, keep the atoms
		print('test')
	
	def __str__(self):
		tempStr = ''

		for atom_as_key in self.graph.keys():
			tempStr = tempStr + str(atom_as_key) + ' : \n{\n'

			# enumerate since sets are not iterable
			for index, tuple_of_atom_bond in enumerate(self.graph[atom_as_key]):
				if index == len(self.graph[atom_as_key]) - 1:
					tempStr = tempStr + "\t" + str(tuple_of_atom_bond[0]) + " " + str(tuple_of_atom_bond[1])
				else:
					tempStr = tempStr + "\t" + str(tuple_of_atom_bond[0]) + " " + str(tuple_of_atom_bond[1]) + ",\n"
			
			tempStr += "\n}\n\n"

		return tempStr
		
