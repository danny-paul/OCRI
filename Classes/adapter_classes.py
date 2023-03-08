
from collections import defaultdict

class mapped_node:
	def __init__(self, x: int, y: int, width: int, height: int, type_is: str = 'unknown'):
		self.x = x
		self.y = y
		self.width = width
		self.height = height

		# set coordinate properties
		self.top_left_x = self.x
		self.top_left_y = self.y

		self.top_right_x = self.x + self.width
		self.top_right_y = self.y

		self.bottom_left_x = self.x
		self.bottom_left_y = self.y + self.height

		self.bottom_right_x = self.x + self.width
		self.bottom_right_y = self.y + self.height

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
		temp_str = 'x: ' + str(self.x) + ', y: ' + str(self.y) + ', w: ' + str(self.width) + ', h: ' + str(self.height) + ', type: ' + self.type_is
		return temp_str
		

class mapped_edge:
	def __init__(self, x1: float, y1: float, x2: float, y2: float, perimeter_height: int, perimeter_width: int, type_is: str= 'unknown'):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.x_mid = abs(self.x1 - self.x2) + max(self.x1, self.x2)
		self.y_mid = abs(self.y1 - self.y2) + max(self.y1, self.y2)
		self.slope = (self.y2 -self.y1)/(self.x1 - self.x2)
		self.type_is = type_is

		self.perimeter_height = perimeter_height
		self.perimeter_width = perimeter_width
		# Perimeter box around the cartesian start point for the edge
		self.perimeter_start_point = {
			"top_left_x":(self.x1 - (self.perimeter_width/2)),		"top_left_y":(self.y1 - (self.perimeter_height/2)),
			"top_right_x":(self.x1 + (self.perimeter_width/2)),	"top_right_y":(self.y1 - (self.perimeter_height/2)),
			"bottom_left_x":(self.x1 - (self.perimeter_width/2)),	"bottom_left_y":(self.y1  + (self.perimeter_height/2)),
			"bottom_right_x":(self.x1 + (self.perimeter_width/2)),	"bottom_right_y":(self.y1 + (self.perimeter_height/2))
		   }
		# Perimeter box around the cartesian end point for the edge
		self.perimeter_end_point = {
			"top_left_x":(self.x2 - (self.perimeter_width/2)),		"top_left_y":(self.y2 - (self.perimeter_height/2)),
			"top_right_x":(self.x2 + (self.perimeter_width/2)),	"top_right_y":(self.y2 - (self.perimeter_height/2)),
			"bottom_left_x":(self.x2 - (self.perimeter_width/2)),	"bottom_left_y":(self.y2  + (self.perimeter_height/2)),
			"bottom_right_x":(self.x2 + (self.perimeter_width/2)),	"bottom_right_y":(self.y2 + (self.perimeter_height/2))
		   }
		# Perimeter box around the cartesian mid point for the edge
		self.perimeter_mid_point = {
			"top_left_x":(self.x_mid - (self.perimeter_width/2)),		"top_left_y":(self.y_mid - (self.perimeter_height/2)),
			"top_right_x":(self.x_mid + (self.perimeter_width/2)),	"top_right_y":(self.y_mid - (self.perimeter_height/2)),
			"bottom_left_x":(self.x_mid - (self.perimeter_width/2)),	"bottom_left_y":(self.y_mid  + (self.perimeter_height/2)),
			"bottom_right_x":(self.x_mid + (self.perimeter_width/2)),	"bottom_right_y":(self.y_mid + (self.perimeter_height/2))
		   }
		# Contains edges that are related in double or triple bonding
		self.related_edges = set()

	# Determines if passed cartesian point exist within the edge's start or end perimeter boxes
	def contained_within_perimeter_endpoints(self, x: float, y: float):
			matched: bool = False
			
			contained_within_x_perimeter_one: bool = x > self.perimeter_start_point["top_left_x"] and x < self.perimeter_start_point["top_right_x"]
			contained_within_y_perimeter_one: bool = y > self.perimeter_start_point['top_left_y'] and y < self.perimeter_start_point['bottom_left_y']
			contained_within_x_perimeter_two: bool = x > self.perimeter_end_point['top_left_x'] and x < self.perimeter_end_point['top_right_x']
			contained_within_y_perimeter_two: bool = y > self.perimeter_end_point['top_left_y'] and y < self.perimeter_end_point['bottom_left_y']

			if \
			contained_within_x_perimeter_one and contained_within_y_perimeter_one or \
			contained_within_x_perimeter_two and contained_within_y_perimeter_two:
				matched = True

			return matched
	
	# Determines if passed cartesian point exist within the edge's midpoint perimeter box
	def contained_within_perimeter_midpoint(self, x: float, y: float):
			matched: bool = False
			
			contained_within_x_perimeter_one: bool = x > self.perimeter_mid_point["top_left_x"] and x < self.perimeter_mid_point["top_right_x"]
			contained_within_y_perimeter_one: bool = y > self.perimeter_mid_point['top_left_y'] and y < self.perimeter_mid_point['bottom_left_y']
	
			if contained_within_x_perimeter_one and contained_within_y_perimeter_one:
				matched = True

			return matched
	
	# Determines type edge, should only be used after processing functions are applied (eg: minmize_bond_list_by_midpoint)
	def determine_type(self):
		if len(self.related_edges) == 0:
			self.type_is = 'Single Bond'
		elif len(self.related_edges) == 1:
			self.type_is = 'Double Bond'
		elif len(self.related_edges) == 2:
			self.type_is = 'Triple Bond'
		else:
			self.type_is = 'Error'

	# Updates the edge's "related_edges" property (via midpoint analysis)
	# to contain only those edges most likely to contribute to double or triple bonding
	def minimize_bond_list_by_midpoint(self):
		matched_midpoint_edges = set()

		for edge in self.related_edges:
			if self.contained_within_perimeter_midpoint(edge.x_mid, edge.y_mid):
				matched_midpoint_edges.add(edge)
		
		self.related_edges = matched_midpoint_edges


	def __str__(self):
		temp_str = '(' + str(self.x1) + ', ' + str(self.y1) + '), ' + '(' + str(self.x2) + ', ' + str(self.y2) + ') m=' + str(self.slope) + ' type:' + self.type_is
		return temp_str
			

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
			
