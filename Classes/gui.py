
import tkinter as tk
import math
from tkinter import NORMAL, Label, Toplevel, filedialog as fido
from tkinter import ttk # duplicate
from Classes.graph import Graph
from Classes.bonds import Bond
from Classes.bonds import CovalentBond
from Classes.bonds import SingleBond
from Classes.bonds import DoubleBond
from Classes.bonds import TripleBond
from Classes.atom import Atom
import Classes.constants as CONSTANT
from Classes.adapter_classes import mapped_edge, mapped_node, edge_map, translate_molecule

# main class for the GUI application
class Gui_Edit_Molecule():
	def __init__(self, window: tk.Tk):
		#class-wide lists
		self.letters = []			#holds letter IDs
		self.atom_list = []			#holds atom objects for graph
		self.letterBondings = []	#parallel array for letters, holds bonded lines
									#i = letter, j = bond, k = bond info, l (only for k = 0) = parts of bond
		
		self.singleBonds = []		#holds single bond IDs
		self.doubleBonds = []		#holds double bond IDs
		self.tripleBonds = []		#holds triple bond IDs
		self.single_bond_list = []	#holds single bond objects for the graph
		self.double_bond_list = []	#holds double bond objects for the graph
		self.triple_bond_list = []	#holds triple bond objects for the graph
		#kinda sucks to have 3 lists for the bonds, but it is much easier to manage the lists this way
		self.graph = Graph([])

		# takes in a window object, intializes a dropdown and a canvas object
		# and packs them into the window.
		self.window = window
		self.x = self.y = 0

		# screen height is temporarily changed from SH-100 to SH-300 for testing purposes
		self.canvas = tk.Canvas(self.window, bg="white", width=(self.window.winfo_screenwidth()-300), height=(self.window.winfo_screenheight()-300))

		#create dropdown menu for atoms
		self.atomDropDownName = tk.StringVar()
		self.atomDropDownName.set("Add Atom")
		self.options = ["H","Li","Be","B","C","N","O","F","Na","Mg","Al","Si","P","S","Cl","K","Ca","As","Se","Br","Sr","Sn","Sb","Ba","Pb","Bi","Ra"]
		self.dropdown = tk.OptionMenu(self.window, self.atomDropDownName, *self.options, command=self.dropdown_select_option)
		#self.dropdown.pack(side="left")

		self.dropdown.grid(row = 0, column = 0)

		# self.canvas = tk.Canvas(self.window, bg="white", width=900, height=600)
		self.canvas.grid(row = 1, column = 0, columnspan = 10)		
		
		# Intializes an empty list letters to store the Letters objects.
		self.letters = []
		
		# binds the place_letter method to the canvas object to listen for mouse clicks on the canvas.
		#self.canvas.bind("<Button-1>", self.place_letter)

		# init for Input Field
		self.Comment_Field = tk.Entry(width = 200)
		self.Comment_Field.grid(row = 2, column = 0, columnspan = 10)

		# init buttons with frames
		self.btn_single_bond = tk.Button(text="Single Bond", command=self.create_single_bond)
		self.btn_single_bond.grid(row = 3, column = 0)
		self.single_bond_creator = None
		
		self.btn_double_bond = tk.Button(text="Double Bond", command=self.create_double_bond)
		self.btn_double_bond.grid(row = 3, column = 1)
		self.double_bond_creator = None
		
		self.btn_triple_bond = tk.Button(text="Triple Bond", command=self.create_triple_bond)
		self.btn_triple_bond.grid(row = 3, column = 2)
		self.triple_bond_creator = None
		
		# delete atoms and bonds on canvas
		self.btn_delete = tk.Button(text="Delete", command=self.activate_delete)
		self.btn_delete.grid(row = 3, column = 3)
		self.is_delete_active = False

		self.btn_clear = tk.Button(text="Clear", command=self.clear)
		self.btn_clear.grid(row = 3, column = 4)

		self.btn_import_file = tk.Button(text="Import", command=self.browseFiles)
		self.btn_import_file.grid(row = 3, column = 5)

		self.btn_translate_image = tk.Button(text="Translate Image", state = tk.DISABLED, command=self.send_image)
		self.btn_translate_image.grid(row = 3, column = 6)

		self.btn_photo = tk.Button(text = "Photo")
		self.btn_photo.grid(row = 3, column = 7)

		self.btn_quit = tk.Button(text="Exit", command=self.window.destroy)
		self.btn_quit.grid(row = 3, column = 8)

#############################################  ATOMS, DROPDOWN and LETTERS   #####################################################

	#for select atom dropdown
	def dropdown_select_option(self, option):
		self.selected_option = option
		self.canvas.bind("<Button-1>", self.place_letter)
	
	#place a letter on the canvas
	def place_letter(self, event):
		self.textbox = self.canvas.create_text(event.x, event.y, text=self.selected_option, font=("Arial", 20), tags="letter")
		self.letters.append(self.textbox)

		#add atom object
		atom = Atom(self.selected_option)
		self.atom_list.append(atom)
		self.graph.add_node_via_atom_obj(atom)
		self.selected_option = None
		self.letterBondings.append([])
		self.canvas.unbind("<Button-1>")
		self.canvas.tag_bind(self.textbox, '<Button-1>', self.select_textbox)
		self.canvas.tag_bind(self.textbox, '<B1-Motion>', self.move_textbox)
		self.canvas.tag_bind(self.textbox, '<ButtonRelease-1>', self.deselect_textbox)
		self.atomDropDownName.set("Add Atom")

	def select_textbox(self, event):
		self.selected = True
		self.current_x = event.x
		self.current_y = event.y
		print(self.letterBondings)
		for ID in self.letters:
			x, y = self.canvas.coords(ID)
			if event.x < x + 20 and event.x > x - 20 and event.y < y + 20 and event.y > y - 20:
				self.textbox = ID
				break

	def move_textbox(self, event):
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
				x1, y1 = self.canvas.coords(self.textbox)
				x2, y2 = self.canvas.coords(self.letterBondings[index][i][1])     
				
				# if self.letterBondings[index][i][1] == "STARTwithEND":
				# 	x1, y1 = self.canvas.coords(self.textbox)
				# 	x2, y2 = self.canvas.coords(self.letterBondings[index][i][2])                 
				# elif self.letterBondings[index][i][1] == "ENDwithSTART":
				# 	x1, y1 = self.canvas.coords(self.letterBondings[index][i][2])
				# 	x2, y2 = self.canvas.coords(self.textbox)
				# elif self.letterBondings[index][i][1] == "STARTnoEND":
				# 	x1, y1 = self.canvas.coords(self.textbox)
				# 	x2, y2 = self.letterBondings[index][i][2]
				# elif self.letterBondings[index][i][1] == "ENDnoSTART":
				# 	x1, y1 = self.letterBondings[index][i][2]
				# 	x2, y2 = self.canvas.coords(self.textbox)

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
				# if self.letterBondings[index][i][1] == "STARTnoEND":
				# 	x2, y2 = self.letterBondings[index][i][2]
				# elif self.letterBondings[index][i][1] == "ENDnoSTART":
				# 	x1, y1 = self.letterBondings[index][i][2]

				#update line
				for lineID in self.letterBondings[index][i][0]:
					self.canvas.coords(lineID, x1, y1, x2, y2)
		
	# sets the selected attribute to False so only one letter will be placed at a time.
	# To add another letter the Add Atom menu needs another selection of what needs added.
	def deselect_textbox(self, event):
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
		if self.canvas.find_all() == ():
			self.Comment_Field.delete(0, "end")
			self.Comment_Field.insert(0, "No item to delete")
		else:
			self.disable_buttons()
			self.Comment_Field.delete(0, "end")
			self.Comment_Field.insert(0, "Select item to be deleted, deleting a bonded atom will remove the bond!")
			
			# Change cursor to indicate delete mode
			self.canvas.config(cursor="crosshair")
			
			# Bind click events to handle deletion
			self.canvas.bind('<ButtonPress-1>', self.delete_click)

	# Command for the import button
	def browseFiles(self):
		if self.canvas.find_all() == ():
			self.fileb_exe()
		else:
			self.fileb_popup()


	# Command for translate image button
	def send_image(self):
		self.Comment_Field.delete(0, "end")
		self.Comment_Field.insert(0, "Image Transfered to Recognizer")
		self.canvas.delete("all")
		self.translate_enable_buttons()

	# Creates a popup window after the filebrowser has selected an image.
	def crop_popup(self):

		self.disable_buttons()

		def accept():
			self.Comment_Field.delete(0, "end")
			self.Comment_Field.insert(0, "Image Accepted")
			self.btn_translate_image.configure(state = tk.NORMAL)
			popup.destroy()

		def crop():
			self.Comment_Field.delete(0, "end")
			self.Comment_Field.insert(0, "Crop Image Please")
			self.btn_translate_image.configure(state = tk.NORMAL)
			popup.destroy()
			self.drawrectangle()

		def cancel():
			self.Comment_Field.delete(0, "end")
			self.Comment_Field.insert(0, "Import Canceled")
			self.translate_enable_buttons()
			popup.destroy()
			self.canvas.delete("all")

		popup = tk.Tk()
		popup.title("Confirm")

		button_accept = ttk.Button(popup, text = "Accept", command = accept)
		button_accept.grid(row = 1, column = 1,)

		button_crop = ttk.Button(popup, text = "Crop", command = crop)
		button_crop.grid(row = 1, column = 2)

		button_cancel = ttk.Button(popup, text = "Cancel", command = cancel)
		button_cancel.grid(row = 1, column = 3)

		popup.mainloop()

	# Clear canvas popup window, will ask if they want to clear the whole canvas or not
	def clear(self):
		self.disable_buttons()

		def yes():
			self.canvas.delete("all")
			warning.destroy()
			self.enable_buttons()
		def no():
			warning.destroy()
			self.enable_buttons()
		
		warning = tk.Tk()
		warning.title("Warning")

		warning_label = Label(warning, text = "Are you sure you want to delete all items?")
		warning_label.pack()

		button_yes = ttk.Button(warning, text = "Yes", command = yes)
		button_yes.pack()

		button_no = ttk.Button(warning, text = "No", command = no)
		button_no.pack()

		warning.mainloop()

	# Popup for the file import button, will give the option to continue with the import and clear the screen or
	# cancel the import and keep what is on the canvas
	def fileb_popup(self):
		self.disable_buttons()

		def yes():
			self.canvas.delete("all")
			warning.destroy()
			self.enable_buttons()
			self.fileb_exe()
		def no():
			warning.destroy()
			self.enable_buttons()
		
		warning = tk.Tk()
		warning.title("Warning")

		warning_label = Label(warning, text = "This action will clear workspace, are you sure you want to continue?")
		warning_label.pack()

		button_yes = ttk.Button(warning, text = "Yes", command = yes)
		button_yes.pack()

		button_no = ttk.Button(warning, text = "No", command = no)
		button_no.pack()

		warning.mainloop()
	
	# Function for opening the file browser
	def fileb_exe(self):
		self.canvas.delete("all")
		image_name = fido.askopenfilename(title = "Pick your image")
		print(image_name)
		if image_name:
			self.image = tk.PhotoImage(file = image_name)
			self.canvas.create_image((0, 0), image = self.image, anchor = tk.NW)
			#self.canvas.create_image((root.winfo_screenheight(),root.winfo_screenmmwidth()), image = self.image, anchor = tk.NW)
		
		# Creates popup window
		self.crop_popup()


	# functions to disable/enable buttons
	
	# Specific for the translate_image being disabled after it translates the image
	def translate_enable_buttons(self):
		self.btn_single_bond.configure(state = tk.NORMAL)
		self.btn_double_bond.configure(state = tk.NORMAL)
		self.btn_triple_bond.configure(state = tk.NORMAL)
		self.btn_delete.configure(state = tk.NORMAL)
		self.btn_clear.configure(state = tk.NORMAL)
		self.btn_import_file.configure(state = tk.NORMAL)
		self.btn_translate_image.configure(state = tk.DISABLED)
		self.btn_photo.configure(state = tk.NORMAL)

	def disable_buttons(self):
		self.btn_single_bond.configure(state = tk.DISABLED)
		self.btn_double_bond.configure(state = tk.DISABLED)
		self.btn_triple_bond.configure(state = tk.DISABLED)
		self.btn_delete.configure(state = tk.DISABLED)
		self.btn_clear.configure(state = tk.DISABLED)
		self.btn_import_file.configure(state = tk.DISABLED)
		self.btn_photo.configure(state = tk.DISABLED)

	def enable_buttons(self):
		self.btn_single_bond.configure(state = tk.NORMAL)
		self.btn_double_bond.configure(state = tk.NORMAL)
		self.btn_triple_bond.configure(state = tk.NORMAL)
		self.btn_delete.configure(state = tk.NORMAL)
		self.btn_clear.configure(state = tk.NORMAL)
		self.btn_import_file.configure(state = tk.NORMAL)
		self.btn_photo.configure(state = tk.NORMAL)
		
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
		self.enable_buttons()
		self.Comment_Field.delete(0, "end")
		
		# Check if item is a letter or bond object, delete that item, and return cursor back to normal.
		#if self.canvas.type(item) in ["text", "line"]:
		for i in range(len(self.tripleBonds)):
			if item in self.tripleBonds[i]:
				self.canvas.delete(self.tripleBonds[i][0])
				self.canvas.delete(self.tripleBonds[i][1])
				self.canvas.delete(self.tripleBonds[i][2])
				self.tripleBonds.pop(i)
				self.graph.remove_bond_via_bond_obj(self.triple_bond_list[i])
				self.triple_bond_list.pop(i)
				break       #the breaks in here are to fix a bug
		for i in range(len(self.doubleBonds)):
			if item in self.doubleBonds[i]:
				self.canvas.delete(self.doubleBonds[i][0])
				self.canvas.delete(self.doubleBonds[i][0])
				self.doubleBonds.pop(i)
				self.graph.remove_bond_via_bond_obj(self.double_bond_list[i])
				self.double_bond_list.pop(i)
				break       #if you pop from array, it doesn't update len(array)
		for i in range(len(self.singleBonds)):
			#delete single bond from singleBonds
			if item in self.singleBonds[i]:
				self.canvas.delete(self.singleBonds[i][0])
				self.singleBonds.pop(i)
				self.graph.remove_bond_via_bond_obj(self.single_bond_list[i])
				self.single_bond_list.pop(i)
				break
		for i in range(len(self.letters)):
			if item == self.letters[i]:
				self.canvas.delete(self.letters[i])
				#delete the lines connected to the letter
				for j in range(len(self.letterBondings[i])):
					#delete lines from canvas
					for l in range(len(self.letterBondings[i][j][0])):
						self.canvas.delete(self.letterBondings[i][j][0][l])
					#delete bonds from single, double, and triple bonds
					if self.letterBondings[i][j][0] in self.singleBonds:
						#self.graph.remove_bond_via_bond_obj(self.singleBonds.index(self.letterBondings[i][j][0]))
						self.single_bond_list.pop(self.singleBonds.index(self.letterBondings[i][j][0]))
						self.singleBonds.remove(self.letterBondings[i][j][0])
					elif self.letterBondings[i][j][0] in self.doubleBonds:
						#self.graph.remove_bond_via_bond_obj(self.singleBonds.index(self.letterBondings[i][j][0]))
						self.double_bond_list.pop(self.doubleBonds.index(self.letterBondings[i][j][0]))
						self.doubleBonds.remove(self.letterBondings[i][j][0])
					elif self.letterBondings[i][j][0] in self.tripleBonds:
						#self.graph.remove_bond_via_bond_obj(self.singleBonds.index(self.letterBondings[i][j][0]))
						self.triple_bond_list.pop(self.tripleBonds.index(self.letterBondings[i][j][0]))
						self.tripleBonds.remove(self.letterBondings[i][j][0])
				#delete the items from the arrays
				self.graph.delete_atom_via_atom_object(self.atom_list[i])
				self.letters.pop(i)
				self.letterBondings.pop(i)
				self.atom_list.pop(i)
				break
		#remove lines and letters from associated letterBondings
		for i in range(len(self.letterBondings)):
			for j in range(len(self.letterBondings[i])):
				if item in self.letterBondings[i][j][0] or item in self.letterBondings[i][j]:
					self.letterBondings[i].pop(j)
					break

		print(self.graph)
				
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
		self.disable_buttons()
		self.lineStart = None
		self.startConnected = False
		self.lineEnd = None
		self.endConnected = False
		self.line_instance = None
		self.canvas.bind("<Button-1>", self.on_click_bond)
		self.startLetter = -1
		self.endLetter = -1
		self.Comment_Field.delete(0, "end") # clears for potential bond errors
		self.Comment_Field.insert(0, "Select Two Atoms to Make Bond")

	# Checks if line instance is None. If it is, it sets "start" to the current mouse position (event.x, event.y).
	# If it isn't, it sets "end" to the current mouse position and creates a new Bond object using
	# self.canvas, self.start, self.end. Finally it resets "start" and "end" back to None.
	def on_click_bond(self, event):
		print("ok")
		if self.line_instance is None:
			if self.lineStart is None:
				# keep mouse position so we can change it
				point_x, point_y = -1, -1

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
				if point_x == -1 and point_y == -1:
					self.Comment_Field.delete(0, "end")
					self.Comment_Field.insert(0, "Error: Each bond must be bound to two atoms, please start over and select two atoms")

					self.startLetter = -1
					self.endLetter = -1
					self.startConnected = False
					self.endConnected = False
					self.line_instance = 1
					
					self.start = None
					self.end = None
				else:
					# set start coordinates for bond
					self.lineStart = (point_x, point_y)
					

			else:
				point_x, point_y = event.x, event.y   # keep mouse position so we can change it
				point_x, point_y = -1, -1   # must bind to letter

				# check if we are inside a letter

				for letter in self.letters:
					x, y = self.canvas.coords(letter)

					if event.x < x + 20 and event.x > x - 20 and event.y < y + 20 and event.y > y - 20:
						point_x, point_y = x, y

						# set bonded status
						self.endLetter = letter
						self.endConnected = True
						break

				if (point_x == -1 and point_y == -1 ):
					self.Comment_Field.delete(0, "end")
					self.Comment_Field.insert(0, "Error: Each bond must be bound to two atoms, please start over and select two atoms")
				else:
					# atom is bound to both
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

					# actions to take if both anchors are letters
					if self.startConnected and self.endConnected:
						if self.startLetter != self.endLetter:
							# don't allow the bond to be created if a bond already exists
							for j in range(len(self.letterBondings[self.letters.index(self.startLetter)])):
								# if \
								# 	self.letterBondings[self.letters.index(self.startLetter)][j][1] == "STARTwithEND" and \
								# 	self.letterBondings[self.letters.index(self.startLetter)][j][2] == self.endLetter:
								# 	AddLine = False

								if \
									self.letterBondings[self.letters.index(self.startLetter)][j][1] == self.endLetter:
									
									AddLine = False

						# Prevent self bonding
						if self.startLetter == self.endLetter:
							AddLine = False
							self.Comment_Field.delete(0, "end")
							self.Comment_Field.insert(0, "Error: Cannot self bond")

						#form bonds
						try:
							if self.bond_type == 1:
								#print(self.atom_list[self.letters.index(self.startLetter)])
								#print(self.atom_list[self.letters.index(self.endLetter)])
								bond = SingleBond(self.atom_list[self.letters.index(self.startLetter)], \
								self.atom_list[self.letters.index(self.endLetter)])
								self.single_bond_list.append(bond)
							elif self.bond_type == 2:
								bond = DoubleBond(self.atom_list[self.letters.index(self.startLetter)], \
								self.atom_list[self.letters.index(self.endLetter)])
								self.double_bond_list.append(bond)
							elif self.bond_type == 3:
								bond = TripleBond(self.atom_list[self.letters.index(self.startLetter)], \
								self.atom_list[self.letters.index(self.endLetter)])
								self.triple_bond_list.append(bond)
							#add to graph
							self.graph.add_bond_via_bond_obj(bond)
							#self.graph
							print(self.graph)

						except NameError as err:
							print(err)
							AddLine = False

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
							# self.letterBondings[self.letters.index(self.startLetter)].append((self.singleBonds[len(self.singleBonds) - 1], "STARTwithEND", self.endLetter))
							# self.letterBondings[self.letters.index(self.endLetter)].append((self.singleBonds[len(self.singleBonds) - 1], "ENDwithSTART", self.startLetter))    

							self.letterBondings[self.letters.index(self.startLetter)].append((self.singleBonds[len(self.singleBonds) - 1],  self.endLetter))
							self.letterBondings[self.letters.index(self.endLetter)].append((self.singleBonds[len(self.singleBonds) - 1], self.startLetter))    
						# elif self.startLetter != -1 and self.endLetter == -1 and AddLine:   #only start attached to a letter
						# 	self.letterBondings[self.letters.index(self.startLetter)].append((self.singleBonds[len(self.singleBonds) - 1], "STARTnoEND", endPoint))
						# elif self.startLetter == -1 and self.endLetter != -1 and AddLine:   #only end attached to a letter
						# 	self.letterBondings[self.letters.index(self.endLetter)].append((self.singleBonds[len(self.singleBonds) - 1], "ENDnoSTART", startPoint))

					elif self.bond_type == 2:
						if self.startLetter != -1 and self.endLetter != -1 and AddLine:     #start and end attached to letters
							# self.letterBondings[self.letters.index(self.startLetter)].append((self.doubleBonds[len(self.doubleBonds) - 1], "STARTwithEND", self.endLetter))
							# self.letterBondings[self.letters.index(self.endLetter)].append((self.doubleBonds[len(self.doubleBonds) - 1], "ENDwithSTART", self.startLetter))  

							self.letterBondings[self.letters.index(self.startLetter)].append((self.doubleBonds[len(self.doubleBonds) - 1],  self.endLetter))
							self.letterBondings[self.letters.index(self.endLetter)].append((self.doubleBonds[len(self.doubleBonds) - 1], self.startLetter))    
						# elif self.startLetter != -1 and self.endLetter == -1 and AddLine:   #only start attached to a letter
						# 	self.letterBondings[self.letters.index(self.startLetter)].append((self.doubleBonds[len(self.doubleBonds) - 1], "STARTnoEND", endPoint))
						# elif self.startLetter == -1 and self.endLetter != -1 and AddLine:   #only end attached to a letter
						# 	self.letterBondings[self.letters.index(self.endLetter)].append((self.doubleBonds[len(self.doubleBonds) - 1], "ENDnoSTART", startPoint))

					elif self.bond_type == 3:
						if self.startLetter != -1 and self.endLetter != -1 and AddLine:     #start and end attached to letters
							# self.letterBondings[self.letters.index(self.startLetter)].append((self.tripleBonds[len(self.tripleBonds) - 1], "STARTwithEND", self.endLetter))
							# self.letterBondings[self.letters.index(self.endLetter)].append((self.tripleBonds[len(self.tripleBonds) - 1], "ENDwithSTART", self.startLetter))    

							self.letterBondings[self.letters.index(self.startLetter)].append((self.tripleBonds[len(self.tripleBonds) - 1],  self.endLetter))
							self.letterBondings[self.letters.index(self.endLetter)].append((self.tripleBonds[len(self.tripleBonds) - 1],  self.startLetter))  
						# elif self.startLetter != -1 and self.endLetter == -1 and AddLine:   #only start attached to a letter
						# 	self.letterBondings[self.letters.index(self.startLetter)].append((self.tripleBonds[len(self.tripleBonds) - 1], "STARTnoEND", endPoint))
						# elif self.startLetter == -1 and self.endLetter != -1 and AddLine:   #only end attached to a letter
						# 	self.letterBondings[self.letters.index(self.endLetter)].append((self.tripleBonds[len(self.tripleBonds) - 1], "ENDnoSTART", startPoint))

				self.startLetter = -1
				self.endLetter = -1
				self.startConnected = False
				self.endConnected = False
				self.line_instance = 1
				
				self.start = None
				self.end = None

				print('structure of letterBondings:\n')
				for index, value in enumerate(self.letterBondings):
					print('index[', str(index), ']:', str(value))
				
				print('structure of single bond group')
				for index, value in enumerate(self.singleBonds):
					print('index[', str(index), ']: ', str(self.singleBonds[index]))

				print('structure of double bond group')
				for index, value in enumerate(self.doubleBonds):
					print('index[', str(index), ']: ', str(self.doubleBonds[index]))
				print('structure of each bond group')
				for index, value in enumerate(self.tripleBonds):
					print('index[', str(index), ']: ', str(self.tripleBonds[index]))
		self.enable_buttons()
		self.Comment_Field.delete(0, "end")