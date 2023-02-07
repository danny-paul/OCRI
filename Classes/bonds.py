from Classes.atom import Atom
import Classes.constants as CONSTANT


# will not be instantiated
class Bond(object):
	# electron_cost = None

	def __init__(self, atom_one: Atom, atom_two: Atom, electron_cost: int):
		self.atoms = [atom_one, atom_two]
		self.electron_cost = electron_cost
		if self.electron_cost == None:
			raise NotImplementedError('Bond Subclasses must define electron_cost')

	def get_atoms(self):
		return self.atoms
		
	def get_electron_bond_cost(self):
		raise NotImplementedError
	
	def can_atoms_form_bond(self, atom_one: Atom, atom_two: Atom) -> bool:
		raise NotImplementedError
	
	# Method to restore valence count to connected atoms and delete instance (self)
	def delete_bond(self):
		update_success: bool = False

		for atom in self.atoms:
			curr_valence_count = atom.get_remaining_val_electrons()
			print(curr_valence_count, self.electron_cost)
			update_success = atom.set_remaining_val_electrons(curr_valence_count + self.electron_cost)
			if not update_success:
				raise NameError("Could not delete the respective bonds")
		
	

	def __str__(self):
		raise NotImplementedError


class IonicBond(Bond):
	def __init(self, atom_one: Atom, atom_two: Atom):
		super().__init__(atom_one, atom_two)
		self.electron_cost = None
	
	def get_electron_bond_cost(self):
		pass

	def can_atoms_form_bond(self, atom_one: Atom, atom_two: Atom) -> bool:
		pass

	def __str__(self):
		pass


# will not be instantiated
class CovalentBond(Bond):
	def __init__(self, atom_one: Atom, atom_two: Atom, electron_cost: int):
		super().__init__(atom_one, atom_two, electron_cost)

	def get_electron_bond_cost(self):
		pass

	def can_atoms_form_bond(self, atom_one: Atom, atom_two: Atom) -> bool:
		pass
	
	def __str__(self):
		pass
	
	def __str__(self):
		pass


class SingleBond(CovalentBond):
	def __init__(self, atom_one: Atom, atom_two: Atom):
		# hydrogen will be the only exception with 1 valence electron
		# self.electron_cost = CONSTANT.SINGLE_BOND_COST 
		super().__init__(atom_one, atom_two, CONSTANT.SINGLE_BOND_COST)
			
	def get_electron_bond_cost(self):
		return self.electron_cost
	
	# return boolean on ability of two parameter atoms ablity to bond
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
	
	# Method to restore valence count to connected atoms and delete instance (self)
	# def delete_bond(self):
	# 	for atom in self.atoms:
	# 		curr_valence_count = atom.get_remaining_val_electrons()
	# 		update_success: bool = atom.set_remaining_val_electrons(curr_valence_count + self.electron_cost)
	# 		if not update_success:
	# 			raise NameError('bonds.py delete_bond(); could not perform atom.set_remaining_val_electrons')


	def __str__(self):
		return str(hex(id(self))) + " " + "Single Bond" + "=(" + str(self.atoms[0]) + ", " + str(self.atoms[1]) + ")"

class DoubleBond(CovalentBond):
	def __init__(self, atom_one: Atom, atom_two: Atom):
		super().__init__(atom_one, atom_two, CONSTANT.DOUBLE_BOND_COST)
		# self.electron_cost = CONSTANT.DOUBLE_BOND_COST
	
	def can_atoms_form_bond(self) -> bool:
		pass
	
	def __str__(self):
		return str(hex(id(self))) + " " + "Double Bond" + "=(" + str(self.atoms[0]) + ", " + str(self.atoms[1]) + ")"

class TripleBond(CovalentBond):
	def __init__(self, atom_one: Atom, atom_two: Atom):
		super().__init__(atom_one, atom_two)
		self.electron_cost = CONSTANT.TRIPLE_BOND_COST
	
	def can_atoms_form_bond(self, atom_one: Atom, atom_two: Atom) -> bool:
		pass
		
	def __str__(self):
		return str(hex(id(self))) + " " + "Triple Bond" + "=(" + str(self.atoms[0]) + ", " + str(self.atoms[1]) + ")"