from Classes.graph import Graph
from Classes.bonds import Bond
from Classes.bonds import SingleBond
from Classes.bonds import DoubleBond
from Classes.bonds import TripleBond
from Classes.atom import Atom
import Classes.constants as CONSTANT

import pprint

def main():
	print("\n\n")
	pretty_print = pprint.PrettyPrinter()
	valid_graph, bond_one, oxygenOne = produce_valid_molecule()
	print(valid_graph)
	#valid_graph.remove_bond_via_bond_obj(bond_one)
	valid_graph.remove_bonds_to_atom(oxygenOne)
	print('-------------------------------------------------------------------\n')
	print(valid_graph)

# returns graph of a valid molecule ("see presentation 3 for the example molecule")
def produce_valid_molecule():
	# pertains to the molecule described in slides
	carbonOne = Atom("C", 4, 0, 8)
	carbonTwo = Atom("C", CONSTANT.CARBON_VAL_ELEC_COUNT, 0, CONSTANT.CARBON_FULL_ELEC_COUNT)
	carbonThree = Atom("C", CONSTANT.CARBON_VAL_ELEC_COUNT, 0, CONSTANT.CARBON_FULL_ELEC_COUNT)
	
	hydrogenOne = Atom("H", CONSTANT.HYDROGEN_VAL_ELEC_COUNT, 0, CONSTANT.HYDROGEN_FULL_ELEC_COUNT)
	hydrogenTwo = Atom("H", CONSTANT.HYDROGEN_VAL_ELEC_COUNT, 0, CONSTANT.HYDROGEN_FULL_ELEC_COUNT)
	hydrogenThree = Atom("H", CONSTANT.HYDROGEN_VAL_ELEC_COUNT, 0, CONSTANT.HYDROGEN_FULL_ELEC_COUNT)
	hydrogenFour = Atom("H", CONSTANT.HYDROGEN_VAL_ELEC_COUNT, 0, CONSTANT.HYDROGEN_FULL_ELEC_COUNT)
	hydrogenFive = Atom("H", CONSTANT.HYDROGEN_VAL_ELEC_COUNT, 0, CONSTANT.HYDROGEN_FULL_ELEC_COUNT)
	hydrogenFive = Atom("H", CONSTANT.HYDROGEN_VAL_ELEC_COUNT, 0, CONSTANT.HYDROGEN_FULL_ELEC_COUNT)
	hydrogenSix = Atom("H", CONSTANT.HYDROGEN_VAL_ELEC_COUNT, 0, CONSTANT.HYDROGEN_FULL_ELEC_COUNT)

	oxygenOne = Atom("O", CONSTANT.OXYGEN_VAL_ELEC_COUNT, 0, CONSTANT.OXYGEN_FULL_ELEC_COUNT)

	# bonds	
	bond_one = SingleBond(carbonOne, hydrogenOne)
	bond_two = SingleBond(carbonOne, hydrogenTwo)
	bond_three = SingleBond(carbonOne, hydrogenThree)
	bond_four = SingleBond(carbonOne, carbonThree)
	bond_five = SingleBond(carbonTwo, hydrogenFour)
	bond_six = SingleBond(carbonTwo, hydrogenFive)
	bond_seven = DoubleBond(carbonTwo, carbonThree)
	bond_eight = SingleBond(carbonThree, oxygenOne)
	bond_nine = SingleBond(oxygenOne, hydrogenSix)


	bond_list: list[Bond] = \
		[bond_one, \
			 bond_two, \
				 bond_three, \
					 bond_four, \
						 bond_five, \
							 bond_six, \
								 bond_seven, \
									 bond_eight, \
										 bond_nine ]

	valid_molecule_graph = Graph(bond_list)

	return valid_molecule_graph, bond_nine, oxygenOne


if __name__ == "__main__":
	main()
else:
	print(__name__)
