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
    'B':8, 'C':8, 'c':8, 'N': 8, 'O':8, 'F':8,
    'Si':8, 'P':8, 'S':8, 'Cl':8, 'Na': 8, 'Be': 8,
    'Br':8, 'I':8, 'H':2, 'Li': 8, 'Mg':8, 'Al':8,
    'K':8, 'Ca':8, 'As':8, 'Se':8, 'Sr':8, 'Sn':8,
    'Sb':8, 'Ba':8, 'Pb':8, 'Bi':8, 'Ra':8
}

ATOM_UNBONDED_VAL_ELEC_COUNT = {
    'B':3, 'C':4, 'c':4, 'N': 5, 'O':6, 'F':7,
    'Si':4, 'P':5, 'S':6, 'Cl':7, 'Na': 1, 'Mg':2,
    'Br':7, 'I':7, 'H':1, 'Li':1, 'Be':2, 'Al':3,
    'K':1, 'Ca':2, 'As':5, 'Se':6, 'Sr':2, 'Sn':4,
    'Sb':5, 'Ba':2, 'Pb':4, 'Bi':5, 'Ra':2
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
	"H":"Hydrogen", "Li":"Lithium", "Be":"Beryllium", "B":"Boron",
	"C":"Carbon", "c" :"Carbon", "N":"Nitrogen", "O":"Oxygen", "F":"Fluorine",
	"Na":"Sodium", "Mg":"Magnesium", "Al":"Aluminum", "Si":"Silicon", 
    "P":"Phosphorus", "S":"Sulfur", "Cl":"Chlorine", "K":"Potassium", 
    "Ca":"Calcium", "As":"Arsenic", "Se":"Selenium", "Br":"Bromine",
	"Sr":"Strontium", "Sn":"Tin", "Sb":"Antimony", "Ba":"Barium", 
	"Pb":"Lead", "Bi":"Bismuth", "Ra":"Radium"
}

POLYATOMIC_SYMBOL_TO_NAME_DICT = {
    "NH4": "Ammonium",
    'SO4': 'Sulfate',
    'HSO4': 'Hydrogen Sulfate',
    'SO3': 'Sulfite',
    'NO3': 'Nitrate',
    'NO2': 'Nitrite',
    'PO4': 'Phosphate',
    'HPO4': "Hydrogen Phosphate",
    'H2PO4': "Dihydrogen Phosphate",
    'PO3': 'Phosphite',
    'ClO4': 'Perchlorate',
    'ClO3': 'Chlorate',
    'ClO2': 'Chlorite',
    'ClO': 'Hypochlorite',
    'MnO4': 'Permanganate',
    'CN': 'Cyanide',
    'CNO': 'Cyanate',
    'SCN': 'Thiocyanate',
    'CO3': 'Carbonate',
    'C2O4': 'Oxalate',
    'H3O': 'Hydronium',
    'NH3': 'Ammonium',
    'NH2': 'Ammonia'
}

POLYATOMIC_UNBONDED_VAL_ELEC_COUNT = {
    "NH4": 1,
    'SO4': 1,
    'HSO4': 1,
    'SO3': 1,
    'NO3': 1,
    'NO2': 1,
    'PO4': 1,
    'HPO4': 1,
    'H2PO4': 1,
    'PO3': 1,
    'ClO4': 1,
    'ClO3': 1,
    'ClO2': 1,
    'ClO': 1,
    'MnO4': 1,
    'CN': 1,
    'CNO': 1,
    'SCN': 1,
    'CO3': 1,
    'C2O4': 1,
    'H3O': 1,
    'NH3': 1
}

POLYATOMIC_FULL_ELEC_COUNT = {
    "NH4": 1,
    'SO4': 1,
    'HSO4': 1,
    'SO3': 1,
    'NO3': 1,
    'NO2': 1,
    'PO4': 1,
    'HPO4': 1,
    'H2PO4': 1,
    'PO3': 1,
    'ClO4': 1,
    'ClO3': 1,
    'ClO2': 1,
    'ClO': 1,
    'MnO4': 1,
    'CN': 1,
    'CNO': 1,
    'SCN': 1,
    'CO3': 1,
    'C2O4': 1,
    'H3O': 1,
    'NH3': 1
}