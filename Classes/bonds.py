from Classes.atom import Atom
import Classes.constants as CONSTANT

class Bond:
	def __init__(self, atomOne: Atom, atomTwo: Atom):
		self.atoms = [atomOne, atomTwo]

	def getAtoms(self):
		return self.atoms

class CovalentBond(Bond):
	def __init__(self, atomOne: Atom, atomTwo: Atom):
		super.__init__(atomOne, atomTwo)

class SingleBond(CovalentBond):
	def __init__(self, atomOne: Atom, atomTwo: Atom):
		super.__init__(atomOne, atomTwo)
		self.electronCost = CONSTANT.SINGLE_BOND_COST
	
	def get_electron_cost(self):
		return self.electronCost
	

class DoubleBond(CovalentBond):
	def __init__(self, atomOne: Atom, atomTwo: Atom):
		super.__init__(atomOne, atomTwo)
		self.electronCost = CONSTANT.DOUBLE_BOND_COST

class TripleBond(CovalentBond):
	def __init__(self, atomOne: Atom, atomTwo: Atom):
		super.__init__(atomOne, atomTwo)
		self.electronCost = CONSTANT.TRIPLE_BOND_COST