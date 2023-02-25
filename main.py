from Classes.graph import Graph
from Classes.bonds import Bond
from Classes.bonds import CovalentBond
from Classes.bonds import SingleBond
from Classes.bonds import DoubleBond
from Classes.bonds import TripleBond
from Classes.atom import Atom
import Classes.constants as CONSTANT

import pprint

def main():
	pretty_print = pprint.PrettyPrinter()

	# print original molecule (no removals)
	print("\n\n")
	print('-------------------------------------------------------------------\n')
	print('original')
	valid_graph, bond_one, oxygenOne, hydrogenSix, carbonTwo = produce_valid_molecule()
	print(valid_graph)
	pretty_print.pprint(valid_graph.get_mapped_address())
	print()
	pretty_print.pprint(valid_graph.get_mapped_address_counts())
	print('-------------------------------------------------------------------\n')
	print("\n\n")

	# # remove bonds to oxygenOne and print molecule again
	# print('-------------------------------------------------------------------\n')
	# valid_graph.remove_bonds_to_atom(oxygenOne)
	# print('removed BONDS TO oxygenOne')
	# print(valid_graph)
	# pretty_print.pprint(valid_graph.get_mapped_address())
	# print()
	# pretty_print.pprint(valid_graph.get_mapped_address_counts())
	# print('-------------------------------------------------------------------\n')
	# print("\n\n")

	# remove oxygenOne and hydrogen six and print molecule again
	print('-------------------------------------------------------------------\n')
	valid_graph.delete_atoms_via_atom_list([oxygenOne, hydrogenSix])
	print('deleted OxygenOne and HydrogenSix')
	print(valid_graph)
	pretty_print.pprint(valid_graph.get_mapped_address())
	print()
	pretty_print.pprint(valid_graph.get_mapped_address_counts())
	print('-------------------------------------------------------------------\n')
	print("\n\n")

	print('-------------------------------------------------------------------\n')
	print('Adding node atom, Atom Oxygen')
	newOxygen = Atom("O", 6, 0, 8)
	valid_graph.add_node_via_atom_obj(newOxygen)
	print(valid_graph)
	pretty_print.pprint(valid_graph.get_mapped_address())
	print()
	pretty_print.pprint(valid_graph.get_mapped_address_counts())
	print('-------------------------------------------------------------------\n')

	print('-------------------------------------------------------------------\n')
	print('Adding node atom, Atom Hydrogen')
	newHydrogen = Atom("H", 1, 0, 2)
	valid_graph.add_node_via_atom_obj(newHydrogen)
	print(valid_graph)
	pretty_print.pprint(valid_graph.get_mapped_address())
	print()
	pretty_print.pprint(valid_graph.get_mapped_address_counts())
	print('-------------------------------------------------------------------\n')

	print('-------------------------------------------------------------------\n')
	print('Adding bond between non connected node atoms, oxygen1 and hydrogen 6')
	valid_graph.add_bond_via_bond_obj(SingleBond(newOxygen, newHydrogen))
	print(valid_graph)
	pretty_print.pprint(valid_graph.get_mapped_address())
	print()
	pretty_print.pprint(valid_graph.get_mapped_address_counts())
	print('-------------------------------------------------------------------\n')


	print('-------------------------------------------------------------------\n')
	print('Adding bond between non connected nodes, oxygen1 and ')
	valid_graph.add_bond_via_bond_obj(SingleBond(newOxygen, carbonTwo))
	print(valid_graph)
	pretty_print.pprint(valid_graph.get_mapped_address())
	print()
	pretty_print.pprint(valid_graph.get_mapped_address_counts())
	print('-------------------------------------------------------------------\n')


# returns graph of a valid molecule ("see presentation 3 for the example molecule")
def produce_valid_molecule():
	# pertains to the molecule described in slides
	carbonOne = Atom("C", CONSTANT.CARBON_VAL_ELEC_COUNT, 0, CONSTANT.CARBON_FULL_ELEC_COUNT)
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

	try:
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

		# generate molecule by passing bond_list
		valid_molecule_graph = Graph(bond_list)
	except NameError as e:
		print(e)


	return valid_molecule_graph, bond_nine, oxygenOne, hydrogenSix, carbonThree


	# can form bonding
	# can_form_bond =\
	# 				CovalentBond.can_atoms_form_bond(carbonOne, hydrogenOne, CONSTANT.SINGLE_BOND_COST) \
	# 				and \
	# 				CovalentBond.can_atoms_form_bond(carbonOne, hydrogenTwo, CONSTANT.SINGLE_BOND_COST) \
	# 				and \
	# 				CovalentBond.can_atoms_form_bond(carbonOne, hydrogenTwo, CONSTANT.SINGLE_BOND_COST) \
	# 				and \
	# 				CovalentBond.can_atoms_form_bond(carbonOne, hydrogenThree, CONSTANT.SINGLE_BOND_COST) \
	# 				and \
	# 				CovalentBond.can_atoms_form_bond(carbonOne, carbonThree, CONSTANT.SINGLE_BOND_COST) \
	# 				and \
	# 				CovalentBond.can_atoms_form_bond(carbonTwo, hydrogenFour, CONSTANT.SINGLE_BOND_COST) \
	# 				and \
	# 				CovalentBond.can_atoms_form_bond(carbonTwo, hydrogenFive, CONSTANT.SINGLE_BOND_COST) \
	# 				and \
	# 				CovalentBond.can_atoms_form_bond(carbonTwo, carbonThree, CONSTANT.DOUBLE_BOND_COST) \
	# 				and \
	# 				CovalentBond.can_atoms_form_bond(carbonThree, oxygenOne, CONSTANT.SINGLE_BOND_COST) \
	# 				and \
	# 				CovalentBond.can_atoms_form_bond(oxygenOne, hydrogenSix, CONSTANT.SINGLE_BOND_COST)

	# # if all bonds can form, create Bond objects
	# if can_form_bond:
	# 	bond_one = SingleBond(carbonOne, hydrogenOne)
	# 	bond_two = SingleBond(carbonOne, hydrogenTwo)
	# 	bond_three = SingleBond(carbonOne, hydrogenThree)
	# 	bond_four = SingleBond(carbonOne, carbonThree)

	# 	bond_five = SingleBond(carbonTwo, hydrogenFour)
	# 	bond_six = SingleBond(carbonTwo, hydrogenFive)
	# 	bond_seven = DoubleBond(carbonTwo, carbonThree)

	# 	bond_eight = SingleBond(carbonThree, oxygenOne)

	# 	bond_nine = SingleBond(oxygenOne, hydrogenSix)
	# 	bond_list: list[Bond] = \
	# 		[bond_one, \
	# 			bond_two, \
	# 				bond_three, \
	# 					bond_four, \
	# 						bond_five, \
	# 							bond_six, \
	# 								bond_seven, \
	# 									bond_eight, \
	# 										bond_nine ]

	# 	# generate molecule by passing bond_list
	# 	valid_molecule_graph = Graph(bond_list)

	# print('is this a valid structure? ' + str(can_form_bond))

	# return valid_molecule_graph, bond_nine, oxygenOne, hydrogenSix





if __name__ == "__main__":
	main()
else:
	print(__name__)
