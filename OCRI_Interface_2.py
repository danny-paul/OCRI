import tkinter as tk
import math
from tkinter import filedialog as fido

#globals
letters = []                #holds letter IDs
letterBondings = []        #parallel array for letters, holds bonded line points for 
singleBonds = []            #holds single bond IDs
doubleBonds = []            #holds double bond IDs
tripleBonds = []            #holds triple bond IDs

class SingleBond:
    # constructor method. It takes in a canvas object, and two points (start and end)
    # and creates a line between them with the create_line method of the canvas object.
    def __init__(self, canvas, start, end):
        #we don't need the array for single bonds, but I'm putting it here for consistency
        sB = []
        sB.append(canvas.create_line(start, end, width=4, tags="bond"))
        global singleBonds
        singleBonds.append(sB)
   
class DoubleBond:
    # constructor method. It takes in a canvas object, and two points (start and end)
    # and creates two lines between them with the create_line method of the canvas object.
    def __init__(self, canvas, start, end):
        dB = []
        dB.append(canvas.create_line(start, end, width=12, fill="black", tags="bond"))
        dB.append(canvas.create_line(start, end, width=4, fill="white", tags="bond"))
        global doubleBonds
        doubleBonds.append(dB)

class TripleBond:
    # constructor method. It takes in a canvas object, and two points (start and end)
    # and creates three lines between them with the create_line method of the canvas object.
    def __init__(self, canvas, start, end):
        tB = []
        tB.append(canvas.create_line(start, end, width=20, fill="black", tags="bond"))
        tB.append(canvas.create_line(start, end, width=12, fill="white", tags="bond"))
        tB.append(canvas.create_line(start, end, width=4, fill="black", tags="bond"))
        global tripleBonds
        tripleBonds.append(tB)

class SingleBondCreator:
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

# main class for the GUI application
class Main:
    def __init__(self, window):
        # takes in a window object, intializes a dropdown and a canvas object
        #and packs them into the window.
        self.window = window
        self.x = self.y = 0
        #screen height is temporarily changed from SH-100 to SH-300 for testing purposes
        self.canvas = tk.Canvas(self.window, bg="white", width=900, height=(root.winfo_screenheight()-300))
        self.dropdown = Dropdown(self.canvas, window=self.window)
        self.dropdown.pack(anchor=tk.NW, pady=2)       
        #self.canvas = tk.Canvas(self.window, bg="white", width=900, height=600)
        self.canvas.pack(fill=tk.X)
        
        # Intitalizes four Frame objects and packs them in the window for the bond and delete buttons
        self.bond1 = tk.Frame(self.window)
        self.bond1.pack(side=tk.LEFT, pady=2)
        
        self.bond2 = tk.Frame(self.window)
        self.bond2.pack(side=tk.LEFT, pady=2)
        
        self.bond3 = tk.Frame(self.window)
        self.bond3.pack(side=tk.LEFT, pady=2)
        
        self.deleted = tk.Frame(self.window)
        self.deleted.pack(side=tk.LEFT, pady=2)

        self.importf = tk.Frame(self.window)
        self.importf.pack(side=tk.LEFT, pady=2)

        self.translatei = tk.Frame(self.window)
        self.translatei.pack(side=tk.LEFT, pady=2)

        self.quit = tk.Frame(self.window)
        self.quit.pack(side=tk.LEFT, pady=2)
        
        # Intializes an empty list letters to store the Letters objects.
        self.letters = []
        
        # binds the place_letter method to the canvas object to listen for mouse clicks on the canvas.
        #self.canvas.bind("<Button-1>", self.place_letter)

        # Initializes three button objects for creating single, double, and triple bonds.
        # Initalizes three None values. These are used to track which bond is being created and
        # to handle creating the bond.
        self.single_bond_button = tk.Button(self.bond1, text="Single Bond", command=self.create_single_bond)
        self.single_bond_button.pack()
        self.single_bond_creator = None
        
        self.double_bond_button = tk.Button(self.bond2, text="Double Bond", command=self.create_double_bond)
        self.double_bond_button.pack()
        self.double_bond_creator = None
        self.doubleBonds = []
        
        self.triple_bond_button = tk.Button(self.bond3, text="Triple Bond", command=self.create_triple_bond)
        self.triple_bond_button.pack()
        self.triple_bond_creator = None
        self.tripleBonds = []
        
        # delete atoms and bonds on canvas
        delete_button = tk.Button(self.deleted, text="Delete", command=self.activate_delete)
        delete_button.pack()
        self.is_delete_active = False

        import_button = tk.Button(self.importf, text="Import", command=self.browseFiles)
        import_button.pack()

        translate_image = tk.Button(self.translatei, text="Translate Image", state = tk.DISABLED, command=self.send_image)
        translate_image.pack()

        quit_button = tk.Button(self.quit, text="Exit", command=root.destroy)
        quit_button.pack()

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
        global letters, letterBondings, singleBonds, doubleBonds, tripleBonds
        for i in range(len(tripleBonds)):
            if item in tripleBonds[i]:
                self.canvas.delete(tripleBonds[i][0])
                self.canvas.delete(tripleBonds[i][1])
                self.canvas.delete(tripleBonds[i][2])
                tripleBonds.pop(i)
                break       #the breaks in here are to fix a bug
        for i in range(len(doubleBonds)):
            if item in doubleBonds[i]:
                self.canvas.delete(doubleBonds[i][0])
                self.canvas.delete(doubleBonds[i][0])
                doubleBonds.pop(i)
                break       #if you pop from array, it doesn't update len(array)
        for i in range(len(singleBonds)):
            #delete single bond from singleBonds
            if item in singleBonds[i]:
                self.canvas.delete(singleBonds[i][0])
                singleBonds.pop(i)
                break
        for i in range(len(letters)):
            if item == letters[i]:
                self.canvas.delete(letters[i])
                #delete the lines connected to the letter
                for j in range(len(letterBondings[i])):
                    for l in range(len(letterBondings[i][j][0])):
                        self.canvas.delete(letterBondings[i][j][0][l])
                #delete the items from the arrays
                letters.pop(i)
                letterBondings.pop(i)
                break
        #remove lines and letters from associated letterBondings
        for i in range(len(letterBondings)):
            for j in range(len(letterBondings[i])):
                if item in letterBondings[i][j][0] or item in letterBondings[i][j]:
                    letterBondings[i].pop(j)
                    break
                
        self.deactivate_delete()
    
    # When the Single, Double or Triple Bond button is clicked it initializes
    # Single, Double, and TripleBondCreator object if one doesn't already exist. or if the current
    # SingleBondCreator object is already being used to create a bond.
    def create_single_bond(self):
        if self.single_bond_creator is None or self.single_bond_creator.line_instance is not None:
            self.single_bond_creator = SingleBondCreator(self.canvas)
            
    def create_double_bond(self):
        if self.double_bond_creator is None or self.double_bond_creator.line_instance is not None:
            self.double_bond_creator = DoubleBondCreator(self.canvas)
            
    def create_triple_bond(self):
        if self.triple_bond_creator is None or self.triple_bond_creator.line_instance is not None:
            self.triple_bond_creator = TripleBondCreator(self.canvas)
    
# Creates a Tk object, assigns it to the root variable, sets the title of the window, creates
# a Main object with root as the window parameter, and starts the main loop of the application.
if __name__ == "__main__":
    root = tk.Tk()
    root.title("OCRI Interface")
    app = Main(root)
    #root.attributes('-fullscreen',True) # Makes the root frame start in fullscreen
    root.resizable(False,False)         # Does not allow user to resize the frame
    root.mainloop()
