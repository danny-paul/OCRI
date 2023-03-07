
from collections import defaultdict

class mapped_node:
	def __init__(self, x: int, y: int, width: int, height: int, type_is: str = 'unknown'):
		self.x = x
		self.y = y
		self.width = width
		self.height = height

		# set coordinate properties
		self.top_left_x = self._x
		self.top_left_y = self._y

		self.top_right_x = self._x + self._width
		self.top_right_y = self._y

		self.bottom_left_x = self._x
		self.bottom_left_y = self._y + self._height

		self.bottom_right_x = self._x + self._width
		self.bottom_right_y = self._y + self._height

		self.type_is = type_is
		self.associated_edges = list[mapped_edge]
	
	def expand_boundaries_letterbox(self):
		print()
	
	def contained_in_boundaries(self, x: float, y: float):
			matched: bool = False
			contained_within_x: bool = x > self.top_left_x and x < self.top_right_x
			contained_within_y: bool = y > self.top_left_y and y < self.bottom_left_y

			if contained_within_x and contained_within_y:
				matched = True

			return matched
	
	def __str__(self):
		temp_str = 'x: ' + str(self._x) + ', y: ' + str(self._y) + ', w: ' + str(self._width) + ', h: ' + str(self._height) + ', type: ' + self._type_is
		return temp_str
	
	# getters
	@property
	def x(self):
		return self._x
	@property
	def y(self):
		return self._y
		# getters
	@property
	def width(self):
		return self._width
	@property
	def height(self):
		return self._height
	@property
	def type_is(self):
		return self._type_is
	@property
	def associated_edges(self):
		return self._associated_edges
	# setters
	@x.setter
	def x(self, x):
		self._x = x
	@y.setter
	def y(self, y):
		self._y = y
	@width.setter
	def width(self, width):
		self._width = width
	@height.setter
	def height(self, height):
		self._height = height
	@type_is.setter
	def type_is(self, type_is):
		self._type_is = type_is
	@associated_edges.setter
	def associated_edges(self, associated_edges):
		self._associated_edges = associated_edges
		

class mapped_edge:
	def __init__(self, x1: float, y1: float, x2: float, y2: float, type_is: str= 'unknown'):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.type_is = type_is

	def determine_type(self):
		return "Single Bond"
	
	def __str__(self):
		temp_str = '(' + str(self.x1) + ', ' + str(self._y1) + '), ' + '(' + str(self._x2) + ', ' + str(self._y2) + ')'
		return temp_str
	
	# getters
	@property
	def x1(self):
		return self._x1
	@property
	def y1(self):
		return self._y1
	@property
	def x2(self):
		return self._x2
	@property
	def y2(self):
		return self._y2
	@property
	def type_is(self):
		return self._type_is
	
	# setters
	@x1.setter
	def x1(self, x1):
		self._x1 = x1
	@y1.setter
	def y1(self, y1):
		self._y1 = y1
	@x2.setter
	def x2(self, x2):
		self._x2 = x2
	@y2.setter
	def y2(self, y2):
		self._y2 = y2
	@type_is.setter
	def type_is(self, type_is):
		self._type_is = type_is
			

class edge_map:
	def __init__(self, edge_list = list[mapped_edge], edgeless_nodes = list[mapped_node]):
		self.graph = defaultdict(set) # key = edge, value = set of atoms (2)
		self.edge_list = edge_list
		self.edgeless_nodes = edgeless_nodes
			
	def add_edge(self, edge: mapped_edge):
		print()
		
	def associate_node_with_edge(self, edge: mapped_edge):
		print()

	def __str__(self):
		return ''
			
