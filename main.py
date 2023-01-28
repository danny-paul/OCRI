from Classes.graph import Graph
from Classes.bonds import Bond
from Classes.bonds import SingleBond
from Classes.atom import Atom

def main():
	testAtomOne = Atom("C", 8)
	testAtomTwo = Atom("C", 8)
	testing = SingleBond(testAtomOne, testAtomTwo)
	print(testing)
	print(testing.getAtoms)

if __name__ == "__main__":
	main()
else:
	print(__name__)
