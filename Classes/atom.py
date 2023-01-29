class Atom:
	def __init__(self, type: str, max_val_electrons: int, remaining_val_electrons: int):
		# will need to restrict type to a list of predefined values else raise error
		self.type = type
		self.max_val_electrons = max_val_electrons # maximum number of valence elctrons an atom can hold
		self.remaining_val_electrons = remaining_val_electrons # remaining electrons after bonding

	def get_type(self):
		return self.type
	
	def get_max_valence_electrons(self):
		return self.max_val_electrons
	
	def get_remaining_val_electrons(self):
		return self.remaining_val_electrons
	
	def __str__(self):
		return "Type: " + str(self.type) + " Valence Electrons: " + str(self.max_val_electrons) + " Remaining Valence Electrons: " + str(self.remaining_val_electrons)
		
