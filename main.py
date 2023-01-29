from Classes.graph import Graph
from Classes.bonds import SingleBond
from Classes.bonds import DoubleBond
from Classes.bonds import TripleBond
from Classes.atom import Atom

def main():
	print("\n")
	testAtomOne = Atom("C", 8, 0)
	testAtomTwo = Atom("He", 2, 2)
	testAtomThree = Atom("H", 1, 1)
	testAtomFour = Atom("H", 1, 1)
	
	print(SingleBond.can_atoms_form_bond(testAtomThree, testAtomTwo))
	print(SingleBond.can_atoms_form_bond(testAtomTwo, testAtomThree))
	print(SingleBond.can_atoms_form_bond(testAtomThree, testAtomThree))
	print(SingleBond.can_atoms_form_bond(testAtomOne, testAtomTwo))
	print(SingleBond.can_atoms_form_bond(testAtomThree, testAtomFour))
	print("\n\n")
	print(SingleBond.impossible_bonding(testAtomThree, testAtomTwo))
	print(SingleBond.impossible_bonding(testAtomTwo, testAtomThree))
	print(SingleBond.impossible_bonding(testAtomThree, testAtomThree))
	print(SingleBond.impossible_bonding(testAtomOne, testAtomTwo))
	print(SingleBond.impossible_bonding(testAtomThree, testAtomFour))



	# bondOne = SingleBond(testAtomOne, testAtomTwo)
	# print("bond One")
	# print(bondOne)
	# testingOne = bondOne.getAtoms()
	# for atom in testingOne:
	# 	print(atom)
	# print("ElectronCost" + str(bondOne.get_electron_bond_cost()))

	# bondTwo = DoubleBond(testAtomThree, testAtomFour)
	# print("\n\nbond Two")
	# print(bondTwo)
	# testingTwo = bondTwo.getAtoms()
	# for atom in testingTwo:
	# 	print(atom)
	# print("ElectronCost" + str(bondTwo.get_electron_bond_cost()))
	

if __name__ == "__main__":
	main()
else:
	print(__name__)
