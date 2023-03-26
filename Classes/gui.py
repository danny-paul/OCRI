
import tkinter as tk
import math
from tkinter import filedialog as fido # duplicate
from Classes.graph import Graph
from Classes.bonds import Bond
from Classes.bonds import CovalentBond
from Classes.bonds import SingleBond
from Classes.bonds import DoubleBond
from Classes.bonds import TripleBond
from Classes.atom import Atom
import Classes.constants as CONSTANT
from Classes.adapter_classes import mapped_edge, mapped_node, edge_map, translate_molecule


'''
class SingleBond:
	# constructor method. It takes in a canvas object, and two points (start and end)
	# and creates a line between them with the create_line method of the canvas object.
	def __init__(self, canvas: tk.Canvas, start, end):
		#we don't need the array for single bonds, but I'm putting it here for consistency
		sB = []
		sB.append(canvas.create_line(start, end, width=4, tags="bond"))
		global singleBonds
		singleBonds.append(sB)


class DoubleBond:
	# constructor method. It takes in a canvas object, and two points (start and end)
	# and creates two lines between them with the create_line method of the canvas object.
	def __init__(self, canvas: tk.Canvas, start, end):
		dB = []
		dB.append(canvas.create_line(start, end, width=12, fill="black", tags="bond"))
		dB.append(canvas.create_line(start, end, width=4, fill="white", tags="bond"))
		global doubleBonds
		doubleBonds.append(dB)

class TripleBond:
	# constructor method. It takes in a canvas object, and two points (start and end)
	# and creates three lines between them with the create_line method of the canvas object.
	def __init__(self, canvas: tk.Canvas, start, end):
		tB = []
		tB.append(canvas.create_line(start, end, width=20, fill="black", tags="bond"))
		tB.append(canvas.create_line(start, end, width=12, fill="white", tags="bond"))
		tB.append(canvas.create_line(start, end, width=4, fill="black", tags="bond"))
		global tripleBonds
		tripleBonds.append(tB)

class BondCreator:
	def __init__(self, canvas: tk.Canvas):
		self.canvas = canvas
		self.start = None
		self.startConnected = False
		self.end = None
		self.endConnected = False
		self.line_instance = None
		self.canvas.bind("<Button-1>", self.on_click)
		self.startLetter = -1
		self.endLetter = -1


	# Checks if line instance is None. If it is, it sets "start" to the current mouse position (event.x, event.y).
	# If it isn't, it sets "end" to the current mouse position and creates a new Bond object using
	# self.canvas, self.start, self.end. Finally it resets "start" and "end" back to None.
	def on_click(self, event):
		if self.line_instance is None:
			if self.start is None:
				# keep mouse position so we can change it
				point_x, point_y = event.x, event.y

				# check if we are inside a letter
				for letter in letters:
					letter_x, letter_y = self.canvas.coords(letter)
					within_x_boundary: bool = event.x < letter_x + 10 and event.x > letter_x - 10
					within_y_boundary: bool = event.y < letter_y + 10 and event.y > letter_y - 10

					if within_x_boundary and within_y_boundary:
						point_x, point_y = letter_x, letter_y

						# set bonded status
						self.startLetter = letter
						self.startConnected = True
						break

				# set start coordinates for bond
				self.start = (point_x, point_y)

			else:
				point_x, point_y = event.x, event.y   # keep mouse position so we can change it

				# check if we are inside a letter

				for letter in letters:
					x, y = self.canvas.coords(letter)

					if event.x < x + 20 and event.x > x - 20 and event.y < y + 20 and event.y > y - 20:
						point_x, point_y = x, y

						# set bonded status
						self.endLetter = letter
						self.endConnected = True
						break

				
				self.end = (point_x, point_y)

				# calculate snap line to connected letters
				start_x, start_y = self.start
				end_x, end_y = self.end
				startPoint = self.start     # these two are for the letterBonding array
				endPoint = self.end

				if start_x - end_x != 0:
					angle = math.atan((start_y - end_y)/(start_x - end_x))
				elif start_y >= end_y:
					angle = math.pi/2
				elif start_y < end_y:
					angle = -math.pi/2

				if start_x >= end_x:
					start_x = start_x - 20*math.cos(angle)
					end_x = end_x + 20*math.cos(angle)
					start_y = start_y - 20*math.sin(angle)
					end_y = end_y + 20*math.sin(angle)
				else:
					start_x = start_x + 20*math.cos(angle)
					end_x = end_x - 20*math.cos(angle)
					start_y = start_y + 20*math.sin(angle)
					end_y = end_y - 20*math.sin(angle)

				# if connected to a letter, snap line to letter
				if self.startConnected:
					self.start = (start_x, start_y)
				if self.endConnected:
					self.end = (end_x, end_y)

				AddLine = True

				# don't allow the bond to be created if a bond already exists
				if self.startConnected and self.endConnected:
					if self.startLetter != self.endLetter:
						for j in range(len(letterBondings[letters.index(self.startLetter)])):
							if \
								letterBondings[letters.index(self.startLetter)][j][1] == "STARTwithEND" and \
								letterBondings[letters.index(self.startLetter)][j][2] == self.endLetter:
								AddLine = False
								print("Bond exists")

					# Prevent self bonding
					if self.startLetter == self.endLetter:
						AddLine = False
						print("Same Letter")

				# draw line                                                                                                             
				if AddLine: 
					self.line_instance = SingleBond(self.canvas, self.start, self.end)

				#add lines to letterBondings so we know the objects are supposed to be connected
				#letterBondings:  lineIDs  |   anchor type flags   |   anchors (either a letter or a point, we know the difference from the flag)
				if self.startLetter != -1 and self.endLetter != -1 and AddLine:     #start and end attached to letters
					letterBondings[letters.index(self.startLetter)].append((singleBonds[len(singleBonds) - 1], "STARTwithEND", self.endLetter))
					letterBondings[letters.index(self.endLetter)].append((singleBonds[len(singleBonds) - 1], "ENDwithSTART", self.startLetter))    
				elif self.startLetter != -1 and self.endLetter == -1 and AddLine:   #only start attached to a letter
					letterBondings[letters.index(self.startLetter)].append((singleBonds[len(singleBonds) - 1], "STARTnoEND", endPoint))
				elif self.startLetter == -1 and self.endLetter != -1 and AddLine:   #only end attached to a letter
					letterBondings[letters.index(self.endLetter)].append((singleBonds[len(singleBonds) - 1], "ENDnoSTART", startPoint))

				self.startLetter = -1
				self.endLetter = -1
				self.startConnected = False
				self.endConnected = False
				
				self.start = None
				self.end = None



class SingleBondCreator:
	# constructor method. It takes in canvas object and initializes instance variables,
	# start, end, and line instance. It then binds the on_click method to the left mouse
	# button click event on the canvas
	def __init__(self, canvas: tk.Canvas):
		self.canvas = canvas
		self.start = None
		self.startConnected = False
		self.end = None
		self.endConnected = False
		self.line_instance = None
		self.canvas.bind("<Button-1>", self.on_click)
		self.startLetter = -1
		self.endLetter = -1


	
	# Checks if line instance is None. If it is, it sets "start" to the current mouse position (event.x, event.y).
	# If it isn't, it sets "end" to the current mouse position and creates a new Bond object using
	# self.canvas, self.start, self.end. Finally it resets "start" and "end" back to None.
	def on_click(self, event):
		if self.line_instance is None:
			if self.start is None:
				# keep mouse position so we can change it
				point_x, point_y = event.x, event.y

				# check if we are inside a letter
				for letter in letters:
					letter_x, letter_y = self.canvas.coords(letter)
					within_x_boundary: bool = event.x < letter_x + 10 and event.x > letter_x - 10
					within_y_boundary: bool = event.y < letter_y + 10 and event.y > letter_y - 10

					if within_x_boundary and within_y_boundary:
						point_x, point_y = letter_x, letter_y

						# set bonded status
						self.startLetter = letter
						self.startConnected = True
						break

				# set start coordinates for bond
				self.start = (point_x, point_y)

			else:
				point_x, point_y = event.x, event.y   # keep mouse position so we can change it

				# check if we are inside a letter

				for letter in letters:
					if letter in self.canvas.find_all():
						print(letter)
						x, y = self.canvas.coords(letter)

						if event.x < x + 20 and event.x > x - 20 and event.y < y + 20 and event.y > y - 20:
							point_x, point_y = x, y

							# set bonded status
							self.endLetter = letter
							self.endConnected = True
					

				self.end = (point_x, point_y)

				# calculate snap line to connected letters
				start_x, start_y = self.start
				end_x, end_y = self.end
				startPoint = self.start     # these two are for the letterBonding array
				endPoint = self.end

				if start_x - end_x != 0:
					angle = math.atan((start_y - end_y)/(start_x - end_x))
				elif start_y >= end_y:
					angle = math.pi/2
				elif start_y < end_y:
					angle = -math.pi/2

				if start_x >= end_x:
					start_x = start_x - 20*math.cos(angle)
					end_x = end_x + 20*math.cos(angle)
					start_y = start_y - 20*math.sin(angle)
					end_y = end_y + 20*math.sin(angle)
				else:
					start_x = start_x + 20*math.cos(angle)
					end_x = end_x - 20*math.cos(angle)
					start_y = start_y + 20*math.sin(angle)
					end_y = end_y - 20*math.sin(angle)

				# if connected to a letter, snap line to letter
				if self.startConnected:
					self.start = (start_x, start_y)
				if self.endConnected:
					self.end = (end_x, end_y)

				AddLine = True

				# don't allow the bond to be created if a bond already exists
				if self.startConnected and self.endConnected:
					if self.startLetter != self.endLetter:
						for j in range(len(letterBondings[letters.index(self.startLetter)])):
							if \
								letterBondings[letters.index(self.startLetter)][j][1] == "STARTwithEND" and \
								letterBondings[letters.index(self.startLetter)][j][2] == self.endLetter:
								AddLine = False
								print("Bond exists")

					# Prevent self bonding
					if self.startLetter == self.endLetter:
						AddLine = False
						print("Same Letter")

				# draw line                                                                                                             
				if AddLine: 
					self.line_instance = SingleBond(self.canvas, self.start, self.end)

				#add lines to letterBondings so we know the objects are supposed to be connected
				#letterBondings:  lineIDs  |   anchor type flags   |   anchors (either a letter or a point, we know the difference from the flag)
				if self.startLetter != -1 and self.endLetter != -1 and AddLine:     #start and end attached to letters
					letterBondings[letters.index(self.startLetter)].append((singleBonds[len(singleBonds) - 1], "STARTwithEND", self.endLetter))
					letterBondings[letters.index(self.endLetter)].append((singleBonds[len(singleBonds) - 1], "ENDwithSTART", self.startLetter))    
				elif self.startLetter != -1 and self.endLetter == -1 and AddLine:   #only start attached to a letter
					letterBondings[letters.index(self.startLetter)].append((singleBonds[len(singleBonds) - 1], "STARTnoEND", endPoint))
				elif self.startLetter == -1 and self.endLetter != -1 and AddLine:   #only end attached to a letter
					letterBondings[letters.index(self.endLetter)].append((singleBonds[len(singleBonds) - 1], "ENDnoSTART", startPoint))

				self.startLetter = -1
				self.endLetter = -1
				self.startConnected = False
				self.endConnected = False
				
				self.start = None
				self.end = None



class DoubleBondCreator:
	# constructor method. It takes in canvas object and initializes instance variables,
	# start, end, and line instance. It then binds the on_click method to the left mouse
	# button click event on the canvas
	def __init__(self, canvas):
		self.canvas = canvas
		self.start = None
		self.startConnected = False
		self.end = None
		self.endConnected = False
		self.line_instance = None
		self.canvas.bind("<Button-1>", self.on_click)
		self.startLetter = -1
		self.endLetter = -1

	# Checks if line instance is None. If it is, it sets "start" to the current mouse position (event.x, event.y).
	# If it isn't, it sets "end" to the current mouse position and creates a new Bond object using
	# self.canvas, self.start, self.end. Finally it resets "start" and "end" back to None.
	def on_click(self, event):
	   
		if self.line_instance is None:
			if self.start is None:
				eX, eY = event.x, event.y   #keep mouse position so we can change it
				#check if we are inside a letter
				for i in range(len(letters)):
					if letters[i] in self.canvas.find_all():
						x, y = self.canvas.coords(letters[i])
						#test if inside the letter
						if event.x < x + 10 and event.x > x - 10 and event.y < y + 10 and event.y > y - 10:
							eX, eY = x, y
							#set bonded status
							self.startLetter = letters[i]
							self.startConnected = True
				self.start = (eX, eY)
			else:
				eX, eY = event.x, event.y   #keep mouse position so we can change it
				#check if we are inside a letter
				for i in range(len(letters)):
					if letters[i] in self.canvas.find_all():
						x, y = self.canvas.coords(letters[i])
						#test if inside the letter
						if event.x < x + 20 and event.x > x - 20 and event.y < y + 20 and event.y > y - 20:
							eX, eY = x, y
							#set bonded status
							self.endLetter = letters[i]
							self.endConnected = True
				self.end = (eX, eY)

				#calculate snap line to connected letters
				x1, y1 = self.start
				x2, y2 = self.end
				startPoint = self.start     #these two are for the letterBonding array
				endPoint = self.end
				if x1 - x2 != 0:
					angle = math.atan((y1 - y2)/(x1 - x2))
				elif y1 >= y2:
					angle = math.pi/2
				elif y1 < y2:
					angle = -math.pi/2
				if x1 >= x2:
					x1 = x1 - 20*math.cos(angle)
					x2 = x2 + 20*math.cos(angle)
					y1 = y1 - 20*math.sin(angle)
					y2 = y2 + 20*math.sin(angle)
				else:
					x1 = x1 + 20*math.cos(angle)
					x2 = x2 - 20*math.cos(angle)
					y1 = y1 + 20*math.sin(angle)
					y2 = y2 - 20*math.sin(angle)

				#if connected to a letter, snap line to letter
				if self.startConnected:
					self.start = (x1, y1)
				if self.endConnected:
					self.end = (x2, y2)

				AddLine = True

				#don't allow the bond to be created if a bond already exists
				if self.startConnected and self.endConnected:
					if self.startLetter != self.endLetter:
						for j in range(len(letterBondings[letters.index(self.startLetter)])):
							if letterBondings[letters.index(self.startLetter)][j][1] == "STARTwithEND" and letterBondings[letters.index(self.startLetter)][j][2] == self.endLetter:
								AddLine = False
								print("Bond exists")
					#don't allow a letter to bond to itself
					if self.startLetter == self.endLetter:
						AddLine = False
						print("Same Letter")

				#draw line                                                                                                             
				if AddLine: 
					self.line_instance = DoubleBond(self.canvas, self.start, self.end)

				#add lines to letterBondings so we know the objects are supposed to be connected
				#letterBondings:  lineIDs  |   anchor type flags   |   anchors (either a letter or a point, we know the difference from the flag)
				if self.startLetter != -1 and self.endLetter != -1 and AddLine:     #start and end attached to letters
					letterBondings[letters.index(self.startLetter)].append((doubleBonds[len(singleBonds) - 1], "STARTwithEND", self.endLetter))
					letterBondings[letters.index(self.endLetter)].append((doubleBonds[len(singleBonds) - 1], "ENDwithSTART", self.startLetter))    
				elif self.startLetter != -1 and self.endLetter == -1 and AddLine:   #only start attached to a letter
					letterBondings[letters.index(self.startLetter)].append((doubleBonds[len(singleBonds) - 1], "STARTnoEND", endPoint))
				elif self.startLetter == -1 and self.endLetter != -1 and AddLine:   #only end attached to a letter
					letterBondings[letters.index(self.endLetter)].append((doubleBonds[len(singleBonds) - 1], "ENDnoSTART", startPoint))

				self.startLetter = -1
				self.endLetter = -1
				self.startConnected = False
				self.endConnected = False
				
				self.start = None
				self.end = None           

class TripleBondCreator:
	# constructor method. It takes in canvas object and initializes instance variables,
	# start, end, and line instance. It then binds the on_click method to the left mouse
	# button click event on the canvas
	def __init__(self, canvas):
		self.canvas = canvas
		self.start = None
		self.startConnected = False
		self.end = None
		self.endConnected = False
		self.line_instance = None
		self.canvas.bind("<Button-1>", self.on_click)
		self.startLetter = -1
		self.endLetter = -1

	# Checks if line instance is None. If it is, it sets "start" to the current mouse position (event.x, event.y).
	# If it isn't, it sets "end" to the current mouse position and creates a new Bond object using
	# self.canvas, self.start, self.end. Finally it resets "start" and "end" back to None.
	def on_click(self, event):
	   
		if self.line_instance is None:
			if self.start is None:
				eX, eY = event.x, event.y   #keep mouse position so we can change it
				#check if we are inside a letter
				for i in range(len(letters)):
					if letters[i] in self.canvas.find_all():
						x, y = self.canvas.coords(letters[i])
						#test if inside the letter
						if event.x < x + 10 and event.x > x - 10 and event.y < y + 10 and event.y > y - 10:
							eX, eY = x, y
							#set bonded status
							self.startLetter = letters[i]
							self.startConnected = True
				self.start = (eX, eY)
			else:
				eX, eY = event.x, event.y   #keep mouse position so we can change it
				#check if we are inside a letter
				for i in range(len(letters)):
					if letters[i] in self.canvas.find_all():
						x, y = self.canvas.coords(letters[i])
						#test if inside the letter
						if event.x < x + 20 and event.x > x - 20 and event.y < y + 20 and event.y > y - 20:
							eX, eY = x, y
							#set bonded status
							self.endLetter = letters[i]
							self.endConnected = True
				self.end = (eX, eY)

				#calculate snap line to connected letters
				x1, y1 = self.start
				x2, y2 = self.end
				startPoint = self.start     #these two are for the letterBonding array
				endPoint = self.end
				if x1 - x2 != 0:
					angle = math.atan((y1 - y2)/(x1 - x2))
				elif y1 >= y2:
					angle = math.pi/2
				elif y1 < y2:
					angle = -math.pi/2
				if x1 >= x2:
					x1 = x1 - 20*math.cos(angle)
					x2 = x2 + 20*math.cos(angle)
					y1 = y1 - 20*math.sin(angle)
					y2 = y2 + 20*math.sin(angle)
				else:
					x1 = x1 + 20*math.cos(angle)
					x2 = x2 - 20*math.cos(angle)
					y1 = y1 + 20*math.sin(angle)
					y2 = y2 - 20*math.sin(angle)

				#if connected to a letter, snap line to letter
				if self.startConnected:
					self.start = (x1, y1)
				if self.endConnected:
					self.end = (x2, y2)

				AddLine = True

				#don't allow the bond to be created if a bond already exists
				if self.startConnected and self.endConnected:
					if self.startLetter != self.endLetter:
						for j in range(len(letterBondings[letters.index(self.startLetter)])):
							if letterBondings[letters.index(self.startLetter)][j][1] == "STARTwithEND" and letterBondings[letters.index(self.startLetter)][j][2] == self.endLetter:
								AddLine = False
								print("Bond exists")
					#don't allow a letter to bond to itself
					if self.startLetter == self.endLetter:
						AddLine = False
						print("Same Letter")

				#draw line                                                                                                             
				if AddLine: 
					self.line_instance = TripleBond(self.canvas, self.start, self.end)

				#add lines to letterBondings so we know the objects are supposed to be connected
				#letterBondings:  lineIDs  |   anchor type flags   |   anchors (either a letter or a point, we know the difference from the flag)
				if self.startLetter != -1 and self.endLetter != -1 and AddLine:     #start and end attached to letters
					letterBondings[letters.index(self.startLetter)].append((tripleBonds[len(singleBonds) - 1], "STARTwithEND", self.endLetter))
					letterBondings[letters.index(self.endLetter)].append((tripleBonds[len(singleBonds) - 1], "ENDwithSTART", self.startLetter))    
				elif self.startLetter != -1 and self.endLetter == -1 and AddLine:   #only start attached to a letter
					letterBondings[letters.index(self.startLetter)].append((tripleBonds[len(singleBonds) - 1], "STARTnoEND", endPoint))
				elif self.startLetter == -1 and self.endLetter != -1 and AddLine:   #only end attached to a letter
					letterBondings[letters.index(self.endLetter)].append((singleBonds[len(singleBonds) - 1], "ENDnoSTART", startPoint))

				self.startLetter = -1
				self.endLetter = -1
				self.startConnected = False
				self.endConnected = False
				
				self.start = None
				self.end = None




class Dropdown(tk.Frame):
	# constructor method takes in the window object. Calls create_widget function
	# and pack()
	def __init__(self, canvas, window=None): 
		super().__init__(window)
		self.canvas = canvas
		self.window = window
		self.create_widgets()
		self.pack()
	# initializes the "selected" instance variable to a StringVar(iable) with the default value
	# Add Atom, and sets up the options for the dropdown menu.
	def create_widgets(self):
		self.selected = tk.StringVar()
		self.selected.set("Add Atom")
		self.options = ["H","Li","Be","B","C","N","O","F","Na","Mg","Al","Si","P","S","Cl","K","Ca","As","Se","Br","Sr","Sn","Sb","Ba","Pb","Bi","Ra"]
		# creates the dropdown menu using the OptionMenu widget.
		self.dropdown = tk.OptionMenu(self, self.selected, *self.options, command=self.select_option)
		self.dropdown.pack(side="left")
	# method that is called when an option is selected from the dropdown menu.
	# Sets the selectd_option instance variable to the selected option and then resets the
	# dropdown menu to the default value of Add Atom.
	def select_option(self, option):
		self.selected_option = option
		self.selected.set("Add Atom")
		self.canvas.bind("<Button-1>", self.place_letter)

	def place_letter(self, event):
		letter_obj = Letter(self.canvas, self.selected_option, event.x, event.y)
		self.selected_option = None


class Letter:
	# constructor method that takes in canvas object, a letter string, and the x, y, coordinates
	# where the letter should be placed on the canvas.
	def __init__(self, canvas, letter, x, y):
		self.canvas = canvas
		self.letter = letter
		self.textbox = canvas.create_text(x, y, text=self.letter, font=("Arial", 20), tags="letter")#self.letter)
		#add the letter to the global letters array and bonds slot to letterBondings parallel array
		global letters, letterBondings
		letters.append(self.textbox)
		letterBondings.append([])
		self.bind_events()
	# binds the methods select, move, and deselct methods to the appropriate events for the text box on canvas
	def bind_events(self):
		self.canvas.tag_bind(self.textbox, '<Button-1>', self.select)
		self.canvas.tag_bind(self.textbox, '<B1-Motion>', self.move)
		self.canvas.tag_bind(self.textbox, '<ButtonRelease-1>', self.deselect)
	# when textbox on the canvas is clicked it sets the selected instance variable to True and stores
	# the current x and y coordinates of the mouse
	def select(self, event):
		self.selected = True
		self.current_x = event.x
		self.current_y = event.y
	# when the mouse button is being held down on a textbox and selected is True, it calculates the
	# change in x and y coordinates since the last mouse event and moves the textbox by that amount
	def move(self, event):
		if self.selected:
			dx = event.x - self.current_x
			dy = event.y - self.current_y
			self.canvas.move(self.textbox, dx, dy)
			self.current_x = event.x
			self.current_y = event.y

			global letters
			global letterBondings

			#move lines
			index = letters.index(self.textbox)
			for i in range(len(letterBondings[index])):
				#get anchor points for the line
				if letterBondings[index][i][1] == "STARTwithEND":
					x1, y1 = self.canvas.coords(self.textbox)
					x2, y2 = self.canvas.coords(letterBondings[index][i][2])                 
				elif letterBondings[index][i][1] == "ENDwithSTART":
					x1, y1 = self.canvas.coords(letterBondings[index][i][2])
					x2, y2 = self.canvas.coords(self.textbox)
				elif letterBondings[index][i][1] == "STARTnoEND":
					x1, y1 = self.canvas.coords(self.textbox)
					x2, y2 = letterBondings[index][i][2]
				elif letterBondings[index][i][1] == "ENDnoSTART":
					x1, y1 = letterBondings[index][i][2]
					x2, y2 = self.canvas.coords(self.textbox)

				#calculate points for the line
				if x1 - x2 != 0:
					angle = math.atan((y1 - y2)/(x1 - x2))
				elif y1 >= y2:
					angle = math.pi/2
				elif y1 < y2:
					angle = -math.pi/2
				if x1 >= x2:
					x1 = x1 - 20*math.cos(angle)
					x2 = x2 + 20*math.cos(angle)
					y1 = y1 - 20*math.sin(angle)
					y2 = y2 + 20*math.sin(angle)
				else:
					x1 = x1 + 20*math.cos(angle)
					x2 = x2 - 20*math.cos(angle)
					y1 = y1 + 20*math.sin(angle)
					y2 = y2 - 20*math.sin(angle)

				#reset anchors back to point if they aren't attached to a letter, no pivoting
				if letterBondings[index][i][1] == "STARTnoEND":
					x2, y2 = letterBondings[index][i][2]
				elif letterBondings[index][i][1] == "ENDnoSTART":
					x1, y1 = letterBondings[index][i][2]

				#update line
				for lineID in letterBondings[index][i][0]:
					self.canvas.coords(lineID, x1, y1, x2, y2)

				
			
	# sets the selected attribute to False so only one letter will be placed at a time.
	# To add another letter the Add Atom menu needs another selection of what needs added.
	def deselect(self, event):
		self.selected = False
'''


# main class for the GUI application
class Gui_Edit_Molecule():
	def __init__(self, window: tk.Tk):
		#class-wide lists
		self.letters = []			#holds letter IDs
		self.atom_list = []			#holds atom objects
		self.letterBondings = []	#parallel array for letters, holds bonded lines
									#i = letter, j = bond, k = bond info, l (only for k = 0) = parts of bond
		self.singleBonds = []		#holds single bond IDs
		self.doubleBonds = []		#holds double bond IDs
		self.tripleBonds = []		#holds triple bond IDs
		self.bond_list = []			#holds the list of bonds
		self.graph = None			#holds the current graph of the atom

		# takes in a window object, intializes a dropdown and a canvas object
		# and packs them into the window.
		self.window = window
		self.x = self.y = 0

		# screen height is temporarily changed from SH-100 to SH-300 for testing purposes
		self.canvas = tk.Canvas(self.window, bg="white", width=900, height=(self.window.winfo_screenheight()-300))

		#create dropdown menu for atoms
		self.atomDropDownName = tk.StringVar()
		self.atomDropDownName.set("Add Atom")
		self.options = ["H","Li","Be","B","C","N","O","F","Na","Mg","Al","Si","P","S","Cl","K","Ca","As","Se","Br","Sr","Sn","Sb","Ba","Pb","Bi","Ra"]
		self.dropdown = tk.OptionMenu(self.window, self.atomDropDownName, *self.options, command=self.select_option)
		#self.dropdown.pack(side="left")

		self.dropdown.pack(anchor=tk.NW, pady=2)

		# self.canvas = tk.Canvas(self.window, bg="white", width=900, height=600)
		self.canvas.pack(fill=tk.BOTH)
		
		# Intitalizes four Frame objects and packs them in the window for the bond and delete buttons
		self.frame_btn_single_bond = tk.Frame(self.window)
		self.frame_btn_single_bond.pack(side=tk.LEFT, pady=2)
		
		self.frame_btn_double_bond = tk.Frame(self.window)
		self.frame_btn_double_bond.pack(side=tk.LEFT, pady=2)
		
		self.frame_btn_triple_bond = tk.Frame(self.window)
		self.frame_btn_triple_bond.pack(side=tk.LEFT, pady=2)
		
		self.frame_btn_delete = tk.Frame(self.window)
		self.frame_btn_delete.pack(side=tk.LEFT, pady=2)

		self.frame_btn_import_file = tk.Frame(self.window)
		self.frame_btn_import_file.pack(side=tk.LEFT, pady=2)

		self.frame_btn_translate_image = tk.Frame(self.window)
		self.frame_btn_translate_image.pack(side=tk.LEFT, pady=2)

		self.frame_btn_quit = tk.Frame(self.window)
		self.frame_btn_quit.pack(side=tk.LEFT, pady=2)

		# init buttons with frames
		self.btn_single_bond = tk.Button(self.frame_btn_single_bond, text="Single Bond", command=self.create_single_bond)
		self.btn_single_bond.pack()
		self.single_bond_creator = None
		
		self.btn_double_bond = tk.Button(self.frame_btn_double_bond, text="Double Bond", command=self.create_double_bond)
		self.btn_double_bond.pack()
		self.double_bond_creator = None
		
		self.btn_triple_bond = tk.Button(self.frame_btn_triple_bond, text="Triple Bond", command=self.create_triple_bond)
		self.btn_triple_bond.pack()
		self.triple_bond_creator = None
		
		# delete atoms and bonds on canvas
		btn_delete = tk.Button(self.frame_btn_delete, text="Delete", command=self.activate_delete)
		btn_delete.pack()
		self.is_delete_active = False

		btn_import_file = tk.Button(self.frame_btn_import_file, text="Import", command=self.browseFiles)
		btn_import_file.pack()

		btn_translate_image = tk.Button(self.frame_btn_translate_image, text="Translate Image", state = tk.DISABLED, command=self.send_image)
		btn_translate_image.pack()

		btn_quit = tk.Button(self.frame_btn_quit, text="Exit", command=self.window.destroy)
		btn_quit.pack()

#############################################  ATOMS, DROPDOWN and LETTERS   #####################################################

	#for select atom dropdown
	def select_option(self, option):
		self.selected_option = option
		self.atomDropDownName.set("Add Atom")
		self.canvas.bind("<Button-1>", self.place_letter)
	
	#place a letter on the canvas
	def place_letter(self, event):
		self.textbox = self.canvas.create_text(event.x, event.y, text=self.selected_option, font=("Arial", 20), tags="letter")
		self.selected_option = None
		self.letters.append(self.textbox)
		self.letterBondings.append([])
		self.canvas.unbind("<Button-1>")
		self.canvas.tag_bind(self.textbox, '<Button-1>', self.select)
		self.canvas.tag_bind(self.textbox, '<B1-Motion>', self.move)
		self.canvas.tag_bind(self.textbox, '<ButtonRelease-1>', self.deselect)

	def select(self, event):
		self.selected = True
		self.current_x = event.x
		self.current_y = event.y
		print(self.letterBondings)
		for ID in self.letters:
			x, y = self.canvas.coords(ID)
			if event.x < x + 20 and event.x > x - 20 and event.y < y + 20 and event.y > y - 20:
				self.textbox = ID
				break

	def move(self, event):
		if self.selected:
			dx = event.x - self.current_x
			dy = event.y - self.current_y
			self.canvas.move(self.textbox, dx, dy)
			self.current_x = event.x
			self.current_y = event.y

			#move lines
			index = self.letters.index(self.textbox)
			for i in range(len(self.letterBondings[index])):
				#get anchor points for the line
				if self.letterBondings[index][i][1] == "STARTwithEND":
					x1, y1 = self.canvas.coords(self.textbox)
					x2, y2 = self.canvas.coords(self.letterBondings[index][i][2])                 
				elif self.letterBondings[index][i][1] == "ENDwithSTART":
					x1, y1 = self.canvas.coords(self.letterBondings[index][i][2])
					x2, y2 = self.canvas.coords(self.textbox)
				elif self.letterBondings[index][i][1] == "STARTnoEND":
					x1, y1 = self.canvas.coords(self.textbox)
					x2, y2 = self.letterBondings[index][i][2]
				elif self.letterBondings[index][i][1] == "ENDnoSTART":
					x1, y1 = self.letterBondings[index][i][2]
					x2, y2 = self.canvas.coords(self.textbox)

				#calculate points for the line
				if x1 - x2 != 0:
					angle = math.atan((y1 - y2)/(x1 - x2))
				elif y1 >= y2:
					angle = math.pi/2
				elif y1 < y2:
					angle = -math.pi/2
				if x1 >= x2:
					x1 = x1 - 20*math.cos(angle)
					x2 = x2 + 20*math.cos(angle)
					y1 = y1 - 20*math.sin(angle)
					y2 = y2 + 20*math.sin(angle)
				else:
					x1 = x1 + 20*math.cos(angle)
					x2 = x2 - 20*math.cos(angle)
					y1 = y1 + 20*math.sin(angle)
					y2 = y2 - 20*math.sin(angle)

				#reset anchors back to point if they aren't attached to a letter, no pivoting
				if self.letterBondings[index][i][1] == "STARTnoEND":
					x2, y2 = self.letterBondings[index][i][2]
				elif self.letterBondings[index][i][1] == "ENDnoSTART":
					x1, y1 = self.letterBondings[index][i][2]

				#update line
				for lineID in self.letterBondings[index][i][0]:
					self.canvas.coords(lineID, x1, y1, x2, y2)
		
	# sets the selected attribute to False so only one letter will be placed at a time.
	# To add another letter the Add Atom menu needs another selection of what needs added.
	def deselect(self, event):
		self.selected = False

###################################################  PICTURES, AI, and CAMERA  ###################################################

	# draws a rectangle outline for the browseFiles def
	def drawrectangle(self):
		self.canvas.bind("<ButtonPress-1>", self.on_button_press)
		self.canvas.bind("<B1-Motion>", self.on_move_press)
		self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

		self.rect = None

		self.start_x = None
		self.start_y = None

	# gets the first x and y cord and updates it for drawing the rect
	def on_button_press(self, event):
		# save mouse drag start position

		self.start_x = event.x
		self.start_y = event.y

		# create rectangle if not yet exist
		#if not self.rect:
		self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline="black")

	# updates the x and y as the mouse is moved while B1 is pressed
	def on_move_press(self, event):
		curX, curY = (event.x, event.y)

		# expand rectangle as you drag the mouse
		self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

	# once released unbind the mouse events for drawing a rectangle
	def on_button_release(self, event):
		self.canvas.unbind("<ButtonPress-1>")
		self.canvas.unbind("<B1-Motion>")
		self.canvas.unbind("<ButtonRelease-1>")

	def activate_delete(self):
		self.is_delete_active = True
		
		# Change cursor to indicate delete mode
		self.canvas.config(cursor="crosshair")
		
		# Bind click events to handle deletion
		self.canvas.bind('<ButtonPress-1>', self.delete_click)

	def browseFiles(self):
		self.canvas.delete("all")
		image_name = fido.askopenfilename(title = "Pick your image")
		print(image_name)
		if image_name:
			self.image = tk.PhotoImage(file = image_name)
			self.canvas.create_image((0, 0), image = self.image, anchor = tk.NW)
			#self.canvas.create_image((root.winfo_screenheight(),root.winfo_screenmmwidth()), image = self.image, anchor = tk.NW)
		self.drawrectangle()

	def send_image(self):
		self.canvas.delete("all")
		
######################################################   DELETE BUTTON  #####################################################

	def deactivate_delete(self):
		self.is_delete_active = False
		
		# Reset cursor to default
		self.canvas.config(cursor="arrow")
		
		# Unbind click events for deletion
		self.canvas.unbind('<ButtonPress-1>')

	def delete_click(self, event):
		# find closest x and y value that has an object
		item = self.canvas.find_closest(event.x, event.y)[0]
		
		# Check if item is a letter or bond object, delete that item, and return cursor back to normal.
		#if self.canvas.type(item) in ["text", "line"]:
		for i in range(len(self.tripleBonds)):
			if item in self.tripleBonds[i]:
				self.canvas.delete(self.tripleBonds[i][0])
				self.canvas.delete(self.tripleBonds[i][1])
				self.canvas.delete(self.tripleBonds[i][2])
				self.tripleBonds.pop(i)
				break       #the breaks in here are to fix a bug
		for i in range(len(self.doubleBonds)):
			if item in self.doubleBonds[i]:
				self.canvas.delete(self.doubleBonds[i][0])
				self.canvas.delete(self.doubleBonds[i][0])
				self.doubleBonds.pop(i)
				break       #if you pop from array, it doesn't update len(array)
		for i in range(len(self.singleBonds)):
			#delete single bond from singleBonds
			if item in self.singleBonds[i]:
				self.canvas.delete(self.singleBonds[i][0])
				self.singleBonds.pop(i)
				break
		for i in range(len(self.letters)):
			if item == self.letters[i]:
				self.canvas.delete(self.letters[i])
				#delete the lines connected to the letter
				for j in range(len(self.letterBondings[i])):
					for l in range(len(self.letterBondings[i][j][0])):
						self.canvas.delete(self.letterBondings[i][j][0][l])
				#delete the items from the arrays
				self.letters.pop(i)
				self.letterBondings.pop(i)
				break
		#remove lines and letters from associated letterBondings
		for i in range(len(self.letterBondings)):
			for j in range(len(self.letterBondings[i])):
				if item in self.letterBondings[i][j][0] or item in self.letterBondings[i][j]:
					self.letterBondings[i].pop(j)
					break
				
		self.deactivate_delete()

##################################################   BONDS and LINES   ##################################################
	
	# When the Single, Double or Triple Bond button is clicked it initializes
	# Single, Double, and TripleBondCreator object if one doesn't already exist. or if the current
	# SingleBondCreator object is already being used to create a bond.
	def create_single_bond(self):
		self.bond_type = 1
		self.create_bond()
			
	def create_double_bond(self):
		self.bond_type = 2
		self.create_bond()
			
	def create_triple_bond(self):
		self.bond_type = 3
		self.create_bond()

	def create_bond(self):
		self.lineStart = None
		self.startConnected = False
		self.lineEnd = None
		self.endConnected = False
		self.line_instance = None
		self.canvas.bind("<Button-1>", self.on_click)
		self.startLetter = -1
		self.endLetter = -1

	# Checks if line instance is None. If it is, it sets "start" to the current mouse position (event.x, event.y).
	# If it isn't, it sets "end" to the current mouse position and creates a new Bond object using
	# self.canvas, self.start, self.end. Finally it resets "start" and "end" back to None.
	def on_click(self, event):
		print("ok")
		if self.line_instance is None:
			if self.lineStart is None:
				# keep mouse position so we can change it
				point_x, point_y = event.x, event.y

				# check if we are inside a letter
				for letter in self.letters:
					letter_x, letter_y = self.canvas.coords(letter)
					within_x_boundary: bool = event.x < letter_x + 20 and event.x > letter_x - 20
					within_y_boundary: bool = event.y < letter_y + 20 and event.y > letter_y - 20

					if within_x_boundary and within_y_boundary:
						point_x, point_y = letter_x, letter_y

						# set bonded status
						self.startLetter = letter
						self.startConnected = True
						break

				# set start coordinates for bond
				self.lineStart = (point_x, point_y)

			else:
				point_x, point_y = event.x, event.y   # keep mouse position so we can change it

				# check if we are inside a letter

				for letter in self.letters:
					x, y = self.canvas.coords(letter)

					if event.x < x + 20 and event.x > x - 20 and event.y < y + 20 and event.y > y - 20:
						point_x, point_y = x, y

						# set bonded status
						self.endLetter = letter
						self.endConnected = True
						break

				
				self.lineEnd = (point_x, point_y)

				# calculate snap line to connected letters
				start_x, start_y = self.lineStart
				end_x, end_y = self.lineEnd
				startPoint = self.lineStart     # these two are for the letterBonding array
				endPoint = self.lineEnd

				if start_x - end_x != 0:
					angle = math.atan((start_y - end_y)/(start_x - end_x))
				elif start_y >= end_y:
					angle = math.pi/2
				elif start_y < end_y:
					angle = -math.pi/2

				if start_x >= end_x:
					start_x = start_x - 20*math.cos(angle)
					end_x = end_x + 20*math.cos(angle)
					start_y = start_y - 20*math.sin(angle)
					end_y = end_y + 20*math.sin(angle)
				else:
					start_x = start_x + 20*math.cos(angle)
					end_x = end_x - 20*math.cos(angle)
					start_y = start_y + 20*math.sin(angle)
					end_y = end_y - 20*math.sin(angle)

				# if connected to a letter, snap line to letter
				if self.startConnected:
					self.lineStart = (start_x, start_y)
				if self.endConnected:
					self.lineEnd = (end_x, end_y)

				AddLine = True

				# don't allow the bond to be created if a bond already exists
				if self.startConnected and self.endConnected:
					if self.startLetter != self.endLetter:
						for j in range(len(self.letterBondings[self.letters.index(self.startLetter)])):
							if \
								self.letterBondings[self.letters.index(self.startLetter)][j][1] == "STARTwithEND" and \
								self.letterBondings[self.letters.index(self.startLetter)][j][2] == self.endLetter:
								AddLine = False

					# Prevent self bonding
					if self.startLetter == self.endLetter:
						AddLine = False

					#try to form bond
					if self.bond_type == 1:
						self.bond_list.append(self.atom_list(self.letters.index(self.startLetter),
					   self.atom_list(self.letters.index(self.endLetter))))

				# draw line                                                                                                             
				if AddLine:
					if self.bond_type == 1:
						sB = []
						sB.append(self.canvas.create_line(self.lineStart, self.lineEnd, width=4, tags="bond"))
						self.singleBonds.append(sB)
					elif self.bond_type == 2:
						dB = []
						dB.append(self.canvas.create_line(self.lineStart, self.lineEnd, width=12, fill="black", tags="bond"))
						dB.append(self.canvas.create_line(self.lineStart, self.lineEnd, width=4, fill="white", tags="bond"))
						self.doubleBonds.append(dB)
					elif self.bond_type == 3:
						tB = []
						tB.append(self.canvas.create_line(self.lineStart, self.lineEnd, width=20, fill="black", tags="bond"))
						tB.append(self.canvas.create_line(self.lineStart, self.lineEnd, width=12, fill="white", tags="bond"))
						tB.append(self.canvas.create_line(self.lineStart, self.lineEnd, width=4, fill="black", tags="bond"))
						self.tripleBonds.append(tB)

				#add lines to letterBondings so we know the objects are supposed to be connected
				#letterBondings:  lineIDs  |   anchor type flags   |   anchors (either a letter or a point, we know the difference from the flag)
				if self.bond_type == 1:
					if self.startLetter != -1 and self.endLetter != -1 and AddLine:     #start and end attached to letters
						self.letterBondings[self.letters.index(self.startLetter)].append((self.singleBonds[len(self.singleBonds) - 1], "STARTwithEND", self.endLetter))
						self.letterBondings[self.letters.index(self.endLetter)].append((self.singleBonds[len(self.singleBonds) - 1], "ENDwithSTART", self.startLetter))    
					elif self.startLetter != -1 and self.endLetter == -1 and AddLine:   #only start attached to a letter
						self.letterBondings[self.letters.index(self.startLetter)].append((self.singleBonds[len(self.singleBonds) - 1], "STARTnoEND", endPoint))
					elif self.startLetter == -1 and self.endLetter != -1 and AddLine:   #only end attached to a letter
						self.letterBondings[self.letters.index(self.endLetter)].append((self.singleBonds[len(self.singleBonds) - 1], "ENDnoSTART", startPoint))

				elif self.bond_type == 2:
					if self.startLetter != -1 and self.endLetter != -1 and AddLine:     #start and end attached to letters
						self.letterBondings[self.letters.index(self.startLetter)].append((self.doubleBonds[len(self.doubleBonds) - 1], "STARTwithEND", self.endLetter))
						self.letterBondings[self.letters.index(self.endLetter)].append((self.doubleBonds[len(self.doubleBonds) - 1], "ENDwithSTART", self.startLetter))    
					elif self.startLetter != -1 and self.endLetter == -1 and AddLine:   #only start attached to a letter
						self.letterBondings[self.letters.index(self.startLetter)].append((self.doubleBonds[len(self.doubleBonds) - 1], "STARTnoEND", endPoint))
					elif self.startLetter == -1 and self.endLetter != -1 and AddLine:   #only end attached to a letter
						self.letterBondings[self.letters.index(self.endLetter)].append((self.doubleBonds[len(self.doubleBonds) - 1], "ENDnoSTART", startPoint))

				elif self.bond_type == 3:
					if self.startLetter != -1 and self.endLetter != -1 and AddLine:     #start and end attached to letters
						self.letterBondings[self.letters.index(self.startLetter)].append((self.tripleBonds[len(self.tripleBonds) - 1], "STARTwithEND", self.endLetter))
						self.letterBondings[self.letters.index(self.endLetter)].append((self.tripleBonds[len(self.tripleBonds) - 1], "ENDwithSTART", self.startLetter))    
					elif self.startLetter != -1 and self.endLetter == -1 and AddLine:   #only start attached to a letter
						self.letterBondings[self.letters.index(self.startLetter)].append((self.tripleBonds[len(self.tripleBonds) - 1], "STARTnoEND", endPoint))
					elif self.startLetter == -1 and self.endLetter != -1 and AddLine:   #only end attached to a letter
						self.letterBondings[self.letters.index(self.endLetter)].append((self.tripleBonds[len(self.tripleBonds) - 1], "ENDnoSTART", startPoint))

				self.startLetter = -1
				self.endLetter = -1
				self.startConnected = False
				self.endConnected = False
				self.line_instance = 1
				
				self.start = None
				self.end = None
		

