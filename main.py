from Classes.graph import Graph
from Classes.bonds import Bond
from Classes.bonds import SingleBond
from Classes.bonds import DoubleBond
from Classes.bonds import TripleBond
from Classes.atom import Atom

import pprint

def main():
	print("\n")
	testAtom = Atom("C", 2, 2)
	testAtomTwo = Atom("C", 4, 2)
	singleBondOne = SingleBond(Atom("C", 8, 8), Atom("He", 2, 2))
	singleBondTwo = SingleBond(Atom("He", 2, 2), Atom("N", 5, 5))
	singleBondThree = SingleBond(Atom("N", 5, 5), Atom("H", 1, 1))
	singleBondFour = SingleBond(testAtom, Atom("H", 2, 2))
	singleBondFive = SingleBond(testAtom, Atom("Be", 4, 4))
	singleBondSix = SingleBond(testAtom, Atom("He", 6, 6))
	doubleBondSeven = DoubleBond(testAtomTwo, Atom("Be", 2, 2))
	doubleBondEight = DoubleBond(testAtomTwo, Atom("C", 4, 0))

	bonds: list[Bond] = [singleBondOne, singleBondTwo, singleBondThree, singleBondFour, singleBondFive, singleBondSix, doubleBondSeven, doubleBondEight]
	graphTest = Graph(bonds)

	pretty_print = pprint.PrettyPrinter()
	pretty_print.pprint(graphTest.graph)	
	print("\n\n")
	print(graphTest)
	print(singleBondOne)
	print(doubleBondSeven)
	print(doubleBondEight)

	# print(graphTest)


	# testAtomOne = Atom("C", 8, 0)
	# testAtomTwo = Atom("He", 2, 2)
	# testAtomThree = Atom("H", 1, 1)
	# testAtomFour = Atom("H", 1, 1)
	
	# print(SingleBond.can_atoms_form_bond(testAtomThree, testAtomTwo))
	# print(SingleBond.can_atoms_form_bond(testAtomTwo, testAtomThree))
	# print(SingleBond.can_atoms_form_bond(testAtomThree, testAtomThree))
	# print(SingleBond.can_atoms_form_bond(testAtomOne, testAtomTwo))
	# print(SingleBond.can_atoms_form_bond(testAtomThree, testAtomFour))
	# print("\n\n")
	# print(SingleBond.impossible_bonding(testAtomThree, testAtomTwo))
	# print(SingleBond.impossible_bonding(testAtomTwo, testAtomThree))
	# print(SingleBond.impossible_bonding(testAtomThree, testAtomThree))
	# print(SingleBond.impossible_bonding(testAtomOne, testAtomTwo))
	# print(SingleBond.impossible_bonding(testAtomThree, testAtomFour))



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
