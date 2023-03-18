# You cannot declare constants in python, so this is the next best thing

# Bond costs for each atom in the bond
SINGLE_BOND_COST = 1
#SINGLE_BOND_COST_HYDROGEN = 1 # hydrogen costs 1 electron only
DOUBLE_BOND_COST = 2
TRIPLE_BOND_COST = 3
BOND_NAMES_ARR = ['IndexZeroPlaceholder', 'Single Bond', 'Double Bond', 'Triple Bond']

# Max electron count for atoms
CARBON_FULL_ELEC_COUNT = 8
CARBON_VAL_ELEC_COUNT = 4

SILICON_FULL_ELEC_COUNT = 8
SILICON_VAL_ELEC_COUNT = 4

OXYGEN_FULL_ELEC_COUNT = 8
OXYGEN_VAL_ELEC_COUNT = 6

SULFUR_VAL_ELEC_COUNT = 6

NITROGEN_FULL_ELEC_COUNT = 8
NITROGEN_VAL_ELEC_COUNT = 5

POTASSIUM_VAL_ELEC_COUNT = 5

HELIUM_VAL_ELEC_COUNT = 2
MAGNESIUM_VAL_ELEC_COUNT = 2

HYDROGEN_VAL_ELEC_COUNT = 1 
HYDROGEN_FULL_ELEC_COUNT = 2

CANNOT_BOND_TO_SAME_TYPE = {
	"He": True,
	"C": False,
	"H": False,
	"B": False,
	"O": False
}

ATOM_FULL_ELEC_COUNT = {
    'B':8, 'C':8, 'N': 8, 'O':8, 'F':8,
    'Si':8, 'P':8, 'S':8, 'Cl':8,
    'Br':8, 'I':8, 'H':2
}

ATOM_UNBONDED_VAL_ELEC_COUNT = {
    'B':3, 'C':4, 'N': 5, 'O':6, 'F':7,
    'Si':4, 'P':5, 'S':6, 'Cl':7,
    'Br':7, 'I':7, 'H':1
}

ATOM_NAME_TO_SYMBOL_DICT = {
	"Hydrogen":"H", "Helium":"He", "Lithium":"Li","Beryllium":"Be", "Boron":"B",
    "Carbon":"C", "Nitrogen":"N", "Oxygen":"O", "Fluorine":"F", "Neon":"Ne",
    "Sodium":"Na", "Magnesium":"Mg", "Aluminum":"Al", "Silicon":"Si", "Phosphorus":"P",
    "Sulfur":"S", "Chlorine":"Cl", "Argon":"Ar", "Potassium":"K", "Calcium":"Ca",
    "Scandium":"Sc", "Titanium":"Ti", "Vanadium":"V", "Chromium":"Cr", "Manganese":"Mn",
    "Iron":"Fe", "Cobalt":"Co", "Nickel":"Ni", "Copper":"Cu", "Zinc":"Zn",
    "Gallium":"Ga", "Germanium":"Ge", "Arsenic":"As", "Selenium":"Se", "Bromine":"Br",
    "Krypton":"Kr", "Rubidium":"Rb", "Strontium":"Sr", "Yttrium":"Y", "Zirconium":"Zr",
    "Niobium":"Nb", "Molybdenum":"Mo", "Technetium":"Tc", "Ruthenium":"Ru", "Rhodium":"Rh",
    "Palladium":"Pd", "Silver":"Ag", "Cadmium":"Cd", "Indium":"In", "Tin":"Sn",
    "Antimony":"Sb", "Tellurium":"Te", "Iodine":"I", "Xenon":"Xe", "Cesium":"Cs",
    "Barium":"Ba", "Lanthanum":"La", "Cerium":"Ce", "Praseodymium":"Pr", "Neodymium":"Nd",
    "Promethium":"Pm", "Samarium":"Sm", "Europium":"Eu", "Gadolinium":"Gd", "Terbium":"Tb",
    "Dysprosium":"Dy", "Holmium":"Ho", "Erbium":"Er", "Thulium":"Tm", "Ytterbium":"Yb",
    "Lutetium":"Lu", "Hafnium":"Hf", "Tantalum":"Ta", "Wolfram":"W", "Rhenium":"Re",
    "Osmium":"Os", "Iridium":"Ir", "Platinum":"Pt", "Gold":"Au", "Mercury":"Hg",
    "Thallium":"Tl", "Lead":"Pb", "Bismuth":"Bi", "Polonium":"Po", "Astatine":"At",
    "Radon":"Rn", "Francium":"Fr", "Radium":"Ra", "Actinium":"Ac", "Thorium":"Th",
    "Protactinium":"Pa", "Uranium":"U", "Neptunium":"Np", "Plutonium":"Pu", "Americium":"Am",
    "Curium":"Cm", "Berkelium":"Bk", "Californium":"Cf", "Einsteinium":"Es", "Fermium":"Fm",
    "Mendelevium":"Md", "Nobelium":"No", "Lawrencium":"Lr", "Rutherfordium":"Rf", "Dubnium":"Db",
    "Seaborgium":"Sg", "Bohrium":"Bh", "Hassium":"Hs", "Meitnerium":"Mt", "Darmstadtium ":"Ds",
    "Roentgenium ":"Rg", "Copernicium ":"Cn", "Nihonium":"Nh", "Flerovium":"Fl", "Moscovium":"Mc",
    "Livermorium":"Lv", "Tennessine":"Ts", "Oganesson":"Og"
}

ATOM_SYMBOL_TO_NAME_DICT = {
	"H":"Hydrogen", "He":"Helium", "Li":"Lithium", "Be":"Beryllium", "B":"Boron",
	"C":"Carbon", "N":"Nitrogen", "O":"Oxygen", "F":"Fluorine", "Ne":"Neon",
	"Na":"Sodium", "Mg":"Magnesium", "Al":"Aluminum", "Si":"Silicon", "P":"Phosphorus",
	"S":"Sulfur", "Cl":"Chlorine", "Ar":"Argon", "K":"Potassium", "Ca":"Calcium",
	"Sc":"Scandium", "Ti":"Titanium", "V":"Vanadium", "Cr":"Chromium", "Mn":"Manganese",
	"Fe":"Iron", "Co":"Cobalt", "Ni":"Nickel", "Cu":"Copper", "Zn":"Zinc",
	"Ga":"Gallium", "Ge":"Germanium", "As":"Arsenic","Se":"Selenium", "Br":"Bromine",
	"Kr":"Krypton", "Rb":"Rubidium", "Sr":"Strontium", "Y":"Yttrium", "Zr":"Zirconium",
	"Nb":"Niobium", "Mo":"Molybdenum", "Tc":"Technetium", "Ru":"Ruthenium", "Rh":"Rhodium",
	"Pd":"Palladium", "Ag":"Silver", "Cd":"Cadmium", "In":"Indium", "Sn":"Tin",
	"Sb":"Antimony", "Te":"Tellurium", "I":"Iodine", "Xe":"Xenon", "Cs":"Cesium",
	"Ba":"Barium", "La":"Lanthanum", "Ce":"Cerium", "Pr":"Praseodymium", "Nd":"Neodymium",
	"Pm":"Promethium", "Sm":"Samarium", "Eu":"Europium", "Gd":"Gadolinium", "Tb":"Terbium",
	"Dy":"Dysprosium", "Ho":"Holmium", "Er":"Erbium", "Tm":"Thulium", "Yb":"Ytterbium",
	"Lu":"Lutetium", "Hf":"Hafnium", "Ta":"Tantalum", "W":"Wolfram", "Re":"Rhenium",
	"Os":"Osmium", "Ir":"Iridium", "Pt":"Platinum", "Au":"Gold", "Hg":"Mercury",
	"Tl":"Thallium", "Pb":"Lead", "Bi":"Bismuth", "Po":"Polonium", "At":"Astatine",
	"Rn":"Radon", "Fr":"Francium", "Ra":"Radium", "Ac":"Actinium", "Th":"Thorium",
	"Pa":"Protactinium", "U":"Uranium", "Np":"Neptunium", "Pu":"Plutonium", "Am":"Americium",
	"Cm":"Curium", "Bk":"Berkelium", "Cf":"Californium", "Es":"Einsteinium", "Fm":"Fermium",
	"Md":"Mendelevium", "No":"Nobelium", "Lr":"Lawrencium", "Rf":"Rutherfordium", "Db":"Dubnium",
	"Sg":"Seaborgium", "Bh":"Bohrium", "Hs":"Hassium", "Mt":"Meitnerium", "Ds":"Darmstadtium ",
	"Rg":"Roentgenium ", "Cn":"Copernicium ", "Nh":"Nihonium", "Fl":"Flerovium", "Mc":"Moscovium",
	"Lv":"Livermorium", "Ts":"Tennessine", "Og":"Oganesson"
}