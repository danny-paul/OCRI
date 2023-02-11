class Atom:
	def __init__(self, atom_type: str, base_val_electrons: int, shared_val_electrons: int, full_electron_config: int):
		# will need to restrict type to a list of predefined values else raise error
		self.atom_type = atom_type
		self.full_electron_config = full_electron_config # number of electrons req'd to have outer shell stable
		self.base_val_electrons = base_val_electrons # valence electrons available when no bonding present
		self.shared_val_electrons = shared_val_electrons # electrons shared (base - shared >= 0)

	def get_type(self):
		return self.atom_type
	
	def get_base_val_electrons(self):
		return self.base_val_electrons

	def get_shared_val_electrons(self):
		return self.shared_val_electrons

	def get_max_valence_electrons(self):
		return self.full_electron_config
	
	# update the remaining valence electron count if valid
	def set_shared_val_electrons(self, new_value: int):
		success: bool

		if  new_value >= 0 and new_value <= self.full_electron_config:
			self.shared_val_electrons = new_value
			success = True
		else:
			success = False

		return success

	def __str__(self):
		tempStr = str(hex(id(self))) + " " + self.__class__.__name__ + " "

		if len(self.atom_type) == 1:
			tempStr += self.atom_type + "  "
		else:
			tempStr += self.atom_type + " "

		tempStr += str(self.base_val_electrons) + "/" + str(self.shared_val_electrons) + "/" + str(self.full_electron_config)

		return tempStr
		
