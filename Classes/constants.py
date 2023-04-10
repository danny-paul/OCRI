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

# CANNOT_BOND_TO_SAME_TYPE = {
# 	"He": True,
# 	"C": False,
# 	"H": False,
# 	"B": False,
# 	"O": False
# }

ATOM_FULL_ELEC_COUNT = {
    'B':8, 'C':8, 'c':8, 'N': 8, 'O':8, 'F':8,
    'Si':8, 'P':8, 'S':8, 'Cl':8, 
    'Br':8, 'H':2
}

ATOM_UNBONDED_VAL_ELEC_COUNT = {
    'B':3, 'C':4, 'c':4, 'N': 5, 'O':6, 'F':7,
    'Si':4, 'P':5, 'S':6, 'Cl':7,
    'Br':7, 'H':1
}

ATOM_NAME_TO_SYMBOL_DICT = {
	"Hydrogen":"H", "Carbon": "C",
    "Boron":"B", "Nitrogen":"N", 
    "Oxygen":"O", "Fluorine":"F",
    "Silicon":"Si", 
    "Phosphorus":"P", "Sulfur":"S", 
    "Chlorine":"Cl", "Bromine":"Br"
}

ATOM_SYMBOL_TO_NAME_DICT = {
    "H":"Hydrogen", "C":"Carbon",
    "B":"Boron", "N":"Nitrogen",
    "O":"Oxygen", "F":"Fluorine",
    "Si":"Silicon",
    "P":"Phosphorus", "S":"Sulfur",
    "Cl":"Chlorine", "Br":"Bromine"
}

POLYATOMIC_SYMBOL_TO_NAME_DICT = {
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
    'OCl': 'Hypochlorite',
    'CN': 'Cyanide',
    'OCN': 'Cyanate',
    'SCN': 'Thiocyanate',
    'CO3': 'Carbonate',
    'C2O4': 'Oxalate'
}

POLYATOMIC_UNBONDED_VAL_ELEC_COUNT = {
    'SO4': 2,
    'HSO4': 1,
    'SO3': 2,
    'NO3': 1,
    'NO2': 1,
    'PO4': 3,
    'HPO4': 2,
    'H2PO4': 1,
    'PO3': 3,
    'ClO4': 1,
    'ClO3': 1,
    'ClO2': 1,
    'OCl': 1,
    'CN': 1,
    'OCN': 1,
    'SCN': 1,
    'CO3': 2,
    'C2O4': 2
}

POLYATOMIC_FULL_ELEC_COUNT = {
    'SO4': 4,
    'HSO4': 2,
    'SO3': 4,
    'NO3': 2,
    'NO2': 2,
    'PO4': 6,
    'HPO4': 4,
    'H2PO4': 2,
    'PO3': 6,
    'ClO4': 2,
    'ClO3': 2,
    'ClO2': 2,
    'OCl': 2,
    'CN': 2,
    'OCN': 2,
    'SCN': 2,
    'CO3': 4,
    'C2O4': 4
}