class Atom:
	def __init__(self, atom_type: str, max_val_electrons: int, remaining_val_electrons: int):
		# will need to restrict type to a list of predefined values else raise error
		self.atom_type = atom_type
		self.max_val_electrons = max_val_electrons # maximum number of valence elctrons an atom can hold
		self.remaining_val_electrons = remaining_val_electrons # remaining electrons after bonding

	def get_type(self):
		return self.atom_type
	
	def get_max_valence_electrons(self):
		return self.max_val_electrons
	
	def get_remaining_val_electrons(self):
		return self.remaining_val_electrons
	
	def __str__(self):
		tempStr = str(hex(id(self))) + " " + self.__class__.__name__ + " "

		if len(self.atom_type) == 1:
			tempStr += self.atom_type + "  "
		else:
			tempStr += self.atom_type + " "

		tempStr += str(self.remaining_val_electrons) + "/" + str(self.max_val_electrons)

		return tempStr
		
