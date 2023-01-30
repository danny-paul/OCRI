from Classes.atom import Atom
import Classes.constants as CONSTANT


# will not be instantiated
class Bond(object):
	def __init__(self, atom_one: Atom, atom_two: Atom):
		self.atoms = [atom_one, atom_two]

	def get_atoms(self):
		return self.atoms
		
	def get_electron_bond_cost(self):
		raise NotImplementedError
	
	def can_atoms_form_bond(self, atom_one: Atom, atom_two: Atom) -> bool:
		raise NotImplementedError


class IonicBond(Bond):
	def __init(self, atom_one: Atom, atom_two: Atom):
		super().__init__(atom_one, atom_two)
	
	def get_electron_bond_cost(self):
		pass

	def can_atoms_form_bond(self, atom_one: Atom, atom_two: Atom) -> bool:
		pass


# will not be instantiated
class CovalentBond(Bond):
	def __init__(self, atom_one: Atom, atom_two: Atom):
		super().__init__(atom_one, atom_two)
	
	def get_electron_bond_cost(self):
		pass

	def can_atoms_form_bond(self, atom_one: Atom, atom_two: Atom) -> bool:
		pass


class SingleBond(CovalentBond):
	def __init__(self, atom_one: Atom, atom_two: Atom):
		super().__init__(atom_one, atom_two)
		# hydrogen will be the only exception with 1 valence electron
		self.electron_cost = CONSTANT.SINGLE_BOND_COST 
			
	def get_electron_bond_cost(self):
		return self.electron_cost
	
	# return boolean on ability of two parameter atoms ablity to bond based purely on remaining valence electron count
	@staticmethod
	def can_atoms_form_bond(atom_one: Atom, atom_two: Atom) -> bool:
		# hydrogen will be the only exception with 1 valence electron
		valid_bond: bool = True
		elec_count_one = 0
		elec_count_two = 0

		valid_bond = not SingleBond.impossible_bonding(atom_one, atom_two)

		if valid_bond:
			if atom_one.get_type() == "H":
				elec_count_one = atom_one.get_remaining_val_electrons() + 1
				elec_count_two = atom_two.get_remaining_val_electrons()
			elif atom_two.get_type() == "H":
				elec_count_one = atom_one.get_remaining_val_electrons()
				elec_count_two = atom_two.get_remaining_val_electrons() + 1
			
			if elec_count_one - CONSTANT.SINGLE_BOND_COST < 0 or elec_count_two - CONSTANT.SINGLE_BOND_COST < 0:
				valid_bond = False
			
		return valid_bond
	
	# Method to determine impossible bonding on issues OTHER than valence electron count (eg: same atom bonded, H-H bonding, etc)
	@staticmethod
	def impossible_bonding(atom_one: Atom, atom_two: Atom) -> bool:
		impossible_bond: bool = False
		cannot_bond_to_same_type = {
			"H": True,
			"He": True
		}

		if atom_one.get_type() == atom_two.get_type():
			if cannot_bond_to_same_type[atom_one.get_type()]:
				impossible_bond = True

		# Same object?
		if atom_one == atom_two:
			impossible_bond = True
		
		return impossible_bond
		


class DoubleBond(CovalentBond):
	def __init__(self, atom_one: Atom, atom_two: Atom):
		super().__init__(atom_one, atom_two)
		self.electron_cost = CONSTANT.DOUBLE_BOND_COST
	
	def can_atoms_form_bond(self) -> bool:
		pass


class TripleBond(CovalentBond):
	def __init__(self, atom_one: Atom, atom_two: Atom):
		super().__init__(atom_one, atom_two)
		self.electron_cost = CONSTANT.TRIPLE_BOND_COST
	
	def can_atoms_form_bond(self, atom_one: Atom, atom_two: Atom) -> bool:
		pass