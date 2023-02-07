from Classes.graph import Graph
from Classes.bonds import Bond
from Classes.bonds import SingleBond
from Classes.bonds import DoubleBond
from Classes.bonds import TripleBond
from Classes.atom import Atom

import pprint

def main():
	print("\n")
	# testAtom = Atom("C", 2, 2)
	# testAtomTwo = Atom("C", 2, 4)
	# singleBondOne = SingleBond(Atom("C", 8, 8), Atom("He", 2, 2))
	# singleBondTwo = SingleBond(Atom("He", 2, 2), Atom("N", 5, 5))
	# singleBondThree = SingleBond(Atom("N", 5, 5), Atom("H", 1, 1))
	# singleBondFour = SingleBond(testAtom, Atom("H", 2, 2))
	# singleBondFive = SingleBond(testAtom, Atom("Be", 4, 4))
	# singleBondSix = SingleBond(testAtom, Atom("He", 6, 6))
	# doubleBondSeven = DoubleBond(testAtomTwo, Atom("Be", 2, 2))
	# doubleBondEight = DoubleBond(testAtomTwo, Atom("C", 0, 4))

	# bonds: list[Bond] = [singleBondOne, singleBondTwo, singleBondThree, singleBondFour, singleBondFive, singleBondSix, doubleBondSeven, doubleBondEight]
	# graphTest = Graph(bonds)

	# pretty_print = pprint.PrettyPrinter()
	# pretty_print.pprint(graphTest.graph)	
	# print("\n\n")
	# print(graphTest)
	# print(singleBondOne)
	# print(doubleBondSeven)
	# print(doubleBondEight)

	print("\n\n")
	pretty_print = pprint.PrettyPrinter()

	valid_graph = produce_valid_molecule()
	print(valid_graph)
	# temp = graphTest.remove_bonds(testAtom) # key is testAtomTwo, value is set of tuple pairing of atom_bond
	# print(temp)
	# print(type(temp))
	# pretty_print.pprint(temp)	

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

def produce_valid_molecule():
	# pertains to the molecule described in slides
	carbonOne = Atom("C", 4, 4)
	carbonTwo = Atom("C", 4, 4)
	carbonThree = Atom("C", 4, 4)
	
	hydrogenOne = Atom("H", 1, 1)
	hydrogenTwo = Atom("H", 1, 1)
	hydrogenThree = Atom("H", 1, 1)
	hydrogenFour = Atom("H", 1, 1)
	hydrogenFive = Atom("H", 1, 1)
	hydrogenFive = Atom("H", 1, 1)
	hydrogenSix = Atom("H", 1, 1)

	oxygenOne = Atom("O", 6, 6)

	# bonds
	bond_list: list[Bond] = [\
		SingleBond(carbonOne, hydrogenOne), \
		SingleBond(carbonOne, hydrogenTwo), \
		SingleBond(carbonOne, hydrogenThree), \
		SingleBond(carbonOne, carbonThree), \
		SingleBond(carbonTwo, hydrogenFour), \
		SingleBond(carbonTwo, hydrogenFive), \
		DoubleBond(carbonTwo, carbonThree), \
		SingleBond(carbonThree, oxygenOne), \
		SingleBond(oxygenOne, hydrogenSix)]

	valid_molecule_graph = Graph(bond_list)

	return valid_molecule_graph


if __name__ == "__main__":
	main()
else:
	print(__name__)
