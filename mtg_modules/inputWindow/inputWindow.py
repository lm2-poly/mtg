"""
-------------------------------------------------------------------------------------------------------------------------
Multinozzle Toolpath Generator (MTG) for FACMO Chair multinozzle printhead
(inputWindow.py)

Author : Jean-François Chauvette, M.Sc.A, PhD candidate
Email : jean-francois.chauvette@polymtl.ca, chauvettejf@gmail.com
Project : FACMO Chair - Objective 4

Laboratory for Multiscale Mechanics (LM2)
Date created : 2019-11-29

Definition: 
    The class creates an instance of an input window that is used to initialize
    the various MTG parameters.

-------------------------------------------------------------------------------------------------------------------------
Example of import:

    from mtg_modules.inputWindow import inputWindow

Example of implementation:

    # Window creation
    title = 'Project parameters'
    instructions = 'Provide the specifc parameters for your program by filling the following fields.'
    windowWidth = 375               # Width of the window in pixels
    fields = ['String param','Integer param','comboBox']           # Number of field entries matching the variables that you want a user input for.
    defaultVal = [myStringVar, myIntegerVar,['a','b',1]]             # Number of default values must fit the number of fields. For combobox, the last data is an integer representing the index of the selected item by default
    photo = ['path\picture.png',100,127]                # file path, width, height. If a picture isn't needed, set to None.
    smallFields = False;                # To reduce the width of the input field, set to True.
    myWindow = inputWindow.inputWindow(title, instructions, width, fields, defaultVal, columns infosImage, smallFields)            # With this instruction, the window will appear

    # Values assignments
    if myWindow.values:
        [myStringVar, myIntegerVar, myComboBoxChoice] = myWindow.values

    # All values are output as string and must be converted after depending on the expected type. For example :
    myIntegerVar = int(myIntegerVar)

Combo box choice:
    A list of values can be sent within defaultVal. e.g. : defaultVal = [value1, [value2.1, value2.2], value3].
    This will change the text field for a combobox where the user can choose among options.
-------------------------------------------------------------------------------------------------------------------------
Update notes

Date		    Notes
¯¯¯¯¯¯¯¯¯¯		¯¯¯¯¯¯¯¯¯¯
2022-06-06      Added columns compatibility and export_json function

2022-11-17      Moved all basic math functions of the MTG in its own script

-------------------------------------------------------------------------------------------------------------------------
"""
import tkinter as tk
from tkinter import ttk
import collections
import math
import os
import json

class inputWindow:
    def __init__(self, title, instructions, width, height, fields, defaultVal, infosImage=None, smallFields=False, columns=None):
        self.root = None         # Shortcut for tk.Tk()
        self.ents = None         # Entries a textfield
        self.values = []         # List of final values
        self.folderPath = ''     # Folder of where this script is located
        self.fields = fields
        self.hasColumns = columns is not None

        # Gettting the script folder path
        filePath = os.path.realpath(__file__)
        self.folderPath = filePath[0:filePath.rfind('\\')]

        if self.hasColumns:
            nb_cols = len(defaultVal)
        else:
            nb_cols = 1

        colspanLab = 2
        colspanEnt = 2

        infosImage = [0,0,50] if infosImage is None else infosImage
        self.root = tk.Tk()
        self.root.title(title)
        self.v = tk.IntVar()
        self.ents = self.makeform(instructions, width, fields, defaultVal, infosImage, smallFields, columns, nb_cols, colspanLab, colspanEnt)
        self.root.bind('<Return>', self.callback_enter)
        self.ents[next(iter(self.ents))].focus()

        # Adding the OK and Cancel buttons
        col = nb_cols * (colspanLab + colspanEnt) - 1
        b2 = tk.Button(self.root, text='Cancel', width=80, command=(lambda e=self.ents: self.clearValues(e)))
        b2.grid(row=len(fields)+3,column=col, sticky='e', padx=5, pady=20)
        b1 = tk.Button(self.root, text='OK', width=80, command=(lambda e=self.ents: self.assignValues(e)))
        b1.grid(row=len(fields)+3,column=col-1, sticky='e', padx=5, pady=20)

        # Managing window size and screen position
        #extraHeight = 50
        # self.center_window(width, infosImage[2] + len(fields)*22 + extraHeight) # Width = Constant, Height = (Subtitle + nb of fields*height + subtitle + row of buttons)
        self.center_window(width, height)
        self.root.tk.call('wm', 'iconphoto', self.root._w, tk.PhotoImage(file=self.folderPath+'\images\Logo-LM2-fav_icon.ico'))
        self.root.lift()
        self.root.attributes("-topmost", True)
        self.root.mainloop()

    # Function for generating the window with the project parameters
    # Return entries as a dictionnary
    def makeform(self, instructions, width, fields, defVal, infosImage, smallFields, columns, nb_cols, colspanLab, colspanEnt):
        entries = collections.OrderedDict()

        # Adding the image
        colSpanImg = 0
        if infosImage[0] != 0:
            colSpanImg = 2
            #photo = tk.PhotoImage(file=self.folderPath+'\images\\'+infosImage[0])
            photo = tk.PhotoImage(file=infosImage[0])
            img = tk.Label(self.root, image = photo, width=infosImage[1], height=infosImage[2], anchor='w')
            img.image = photo
            img.grid(row=0, column=0, columnspan=colSpanImg, sticky='w', padx=10, pady=10)

        # Adding the instructions
        colspan = nb_cols * (colspanLab + colspanEnt) - colSpanImg
        instr = tk.Label(self.root, text=instructions, justify='left' , anchor='w', wraplength = width - 10)#wraplength=width-15-infosImage[1]-(30 if infosImage[0] != 0 else 0))
        instr.grid(row=0, column=colSpanImg, columnspan=colspan, sticky='w e', padx=10, pady=10)

        # Adding the fields entry
        if fields is not None:
            col_sub_div = colspanLab + colspanEnt
            if smallFields:
                colspanLab += 1
                colspanEnt -= 1
            idxRow = 0
            idxCol = 0

            for field in fields:
                # Index management for multiple columns
                if self.hasColumns:
                    currVal = defVal[idxCol]
                    colNameOffset = 2
                else:
                    currVal = defVal
                    colNameOffset = 0

                # Column name
                if self.hasColumns and idxRow == 0:
                    heading = tk.Label(self.root, text=columns[idxCol], anchor='w')#, width=5)
                    heading.grid(row=idxRow + colNameOffset-1, column=idxCol*col_sub_div, columnspan=col_sub_div, sticky='w', padx=10)
                    separator = ttk.Separator(self.root, orient="horizontal", style = 'grey.TSeparator')
                    separator.grid(row = idxRow + colNameOffset, column = idxCol*col_sub_div, columnspan=col_sub_div, padx=10, pady=5, sticky='we')

                # Label
                lab = tk.Label(self.root, text=field+" : ", anchor='w')#, width=5)
                lab.grid(row=idxRow + 1 + colNameOffset, column=idxCol*col_sub_div, columnspan=colspanLab, sticky='w', padx=10)

                # Field
                if type(currVal[idxRow]) is list:
                    ent = ttk.Combobox(self.root, values = currVal[idxRow][0:-1], state='readonly')
                    ent.current(currVal[idxRow][-1])
                    #ent.bind('<<ComboboxSelected>>', self.callback_comboBox)
                else:
                    ent = tk.Entry(self.root)#, width=35)
                    ent.insert(0, currVal[idxRow])
                ent.grid(row=idxRow + 1 + colNameOffset, column=idxCol*col_sub_div + colspanLab, columnspan=colspanEnt, sticky='w e', padx=10)

                entries[field] = ent

                if idxRow == len(currVal)-1:
                    idxCol += 1
                    idxRow = 0
                else:
                    idxRow += 1

        # Managing column's automatic width
        for i in range(col_sub_div*nb_cols):
            self.root.grid_columnconfigure(i, weight=1, uniform="foo")

        return entries

    # Function for centering the window
    def center_window(self, width, height):
        # get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # calculate position x and y coordinates
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.root.geometry('%dx%d+%d+%d' % (width, height, x, y))

    # Callback function of window for pressing enter
    def callback_enter(self,event):
        self.assignValues(self.ents)

    # def callback_comboBox(self,event):
    #     self.center_window(100, 500)

    # Function for assigning values from the window
    def assignValues(self,e):
        for key in e:   # clears all the field
            self.values.append(e[key].get())
        self.root.destroy()

    # Function for clearing the window form
    def clearValues(self,e):
        for key in e:   # clears all the field
            e[key].delete(0, tk.END)
        e[next(iter(e))].focus() # focus the first field
        self.root.destroy()

    # Function for exporting a json file of the last used values
    def export_json(self, filename, defaultVal):
        if self.hasColumns:
            defaultVal = [j for sub in defaultVal for j in sub]

        paramDict = dict(zip(self.fields, defaultVal))

        #Writing json file
        for p in range(len(self.values)):
            # looping through the window values to reconstruct a valid dict (with correct variable types) for the json file
            paramValue = self.values[p]
            paramField = paramDict[self.fields[p]]

            # if the parameter to update is the index of a list
            if type(paramDict[self.fields[p]]) is list:

                # if it's a list of bool, just update the index with True = 0 and False = 1
                if paramValue == 'True':
                    paramDict[self.fields[p]][-1] = 0
                elif paramValue == 'False':
                    paramDict[self.fields[p]][-1] = 1
                # otherwise, just update the index with the right paramValue as key to the dict
                else:
                    try:
                        paramValue = int(paramValue)
                    except:
                        paramValue = str(paramValue)
                    choiceIndex = paramField.index(paramValue)
                    paramDict[self.fields[p]][-1] = choiceIndex
            # if any other type than list, update with the corresponding type of the original dict
            else:
                paramDict[self.fields[p]] = type(paramField)(paramValue)
        
        with open(filename, 'w') as outfile:
            json.dump(paramDict, outfile)