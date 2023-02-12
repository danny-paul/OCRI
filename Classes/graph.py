# Derived from https://stackoverflow.com/questions/19472530/representing-graphs-data-structure-in-python
from collections import defaultdict
from Classes.atom import Atom
from Classes.bonds import Bond	
from Classes.bonds import CovalentBond

class Graph:
	def __init__(self, bonds: list[Bond]):
		self.graph = defaultdict(set)
		self.add_bonds_via_bond_list(bonds)

	def add_bonds_via_bond_list(self, bonds: list[Bond]):
		for bond in bonds:
			self.add_bond_via_bond_obj(bond)

	def add_bond_via_bond_obj(self, bond: Bond):
		atom_one, atom_two = bond.get_atoms()

		# bond class did checking for validity, so just add to graph
		self.graph[atom_one].add((atom_two, bond))  
		self.graph[atom_two].add((atom_one, bond))
	
	def remove_bonds_via_bond_list(self, bonds: list[Bond]):
		for bond in bonds:
			self.remove_bond_via_bond_obj(bond)

	# update electrons in associated Atom objects, remove bond from the Graph (molecule)
	def remove_bond_via_bond_obj(self, bond: Bond):
		# update electrons associated with previously bonded atoms
		bond.unshare_electrons() 

		# remove bond from graph
		for atom in bond.get_atoms():
			atom_bond_tuples_to_remove = []

			for atom_bond_tuple in self.graph[atom]:
				if (atom_bond_tuple[1] == bond):
					atom_bond_tuples_to_remove.append(atom_bond_tuple)

			# deletes from graph- cannot delete while iterating through set
			for atom_bond_tuple in atom_bond_tuples_to_remove:
				self.graph[atom].remove(atom_bond_tuple)
	
	def add_nodes_via_atom_list(self, atoms: list[Atom]):
		for atom in atoms:
			self.add_node_via_atom_obj(atom)
	
	def add_node_via_atom_obj(self, atom: Atom):
		print()

	def remove_bonds_to_atom(self, reference_atom: Atom):
		# remove all bonds to a given atom, restore valence electrons to atoms- atoms are preserved, bonds are deleted
		bonds_to_atom = []
		# build bonds to the atom
		for atom_bond_tuple in self.graph[reference_atom]:
			bond = atom_bond_tuple[1]
			bonds_to_atom.append(bond)
				
		print(bonds_to_atom)
		self.remove_bonds_via_bond_list(bonds_to_atom)

	def delete_atoms(self, atoms: list[Atom]):
		print()

	def delete_atom(self, atom: Atom):
		print()

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
		
