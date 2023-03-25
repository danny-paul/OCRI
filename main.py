from Classes.graph import Graph
from Classes.bonds import Bond
from Classes.bonds import CovalentBond
from Classes.bonds import SingleBond
from Classes.bonds import DoubleBond
from Classes.bonds import TripleBond
from Classes.atom import Atom
import Classes.constants as CONSTANT
from Classes.adapter_classes import mapped_edge, mapped_node, edge_map, translate_molecule

import pprint

# import Image_Recognition.RecognizerDanny as RecognizerDanny
import Image_Recognition.Recognizer as Recognizer

import Classes.gui as GUI
import tkinter as tk

# def main():
# 	pretty_print = pprint.PrettyPrinter()
# 	# letterBoxes, lines = RecognizerDanny.recognize()
# 	mapped_node_arr, mapped_edge_arr, edge_list = Recognizer.recognize()
# 	recognized_structure: Graph = translate_molecule(mapped_edge_arr, mapped_node_arr)

# 	print(recognized_structure)


# Creates a Tk object, assigns it to the root variable, sets the title of the window, creates
# a Main object with root as the window parameter, and starts the main loop of the application.
def main():
	root = tk.Tk()
	root.title("OCRI Interface")
	app = GUI.Gui_Edit_Molecule(root)
	#root.attributes('-fullscreen',True) # Makes the root frame start in fullscreen
	root.resizable(False, False)         # Does not allow user to resize the frame
	root.mainloop()

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



if __name__ == "__main__":
	main()
else:
	print(__name__)
