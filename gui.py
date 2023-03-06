import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import *

root = tk.Tk()
root.geometry('1500x900')
root.title('Container Movement Optimizer')

# set style ???
style = ttk.Style()
style.configure('Thin.TSeparator', background = 'black', thickness = 3)

# top left frame
topLeftFrame = tk.Frame(root, width = 750, height = 50)
topLeftFrame.grid(row = 0, column = 0, sticky = 'nsew')

# separator bw topLeftFrame and topRightFrame
vertseparator1 = ttk.Separator(root, orient = 'vertical', style = 'Thin.TSeparator')
vertseparator1.grid(row = 0, column = 1, sticky = 'ns')

# top right frame
topRightFrame = tk.Frame(root, width = 750, height = 50)
topRightFrame.grid(row = 0, column = 2, sticky = 'nsew')

# separator bw topRightFrame-topLeftFrame and middleFrame
horzseparator1 = ttk.Separator(root, orient = 'horizontal', style = 'Thin.TSeparator')
horzseparator1.grid(row = 1, column = 0, columnspan = 3, sticky = 'ew')

# middle frame
middleFrame = tk.Frame(root, width = 1500, height = 600)
middleFrame.grid(row = 2, column = 0, columnspan = 3, sticky = 'nsew')

# separator bw middleFrame and bottomFrame
horzseparator2 = ttk.Separator(root, orient = 'horizontal', style = 'Thin.TSeparator')
horzseparator2.grid(row = 3, column = 0, columnspan = 3, sticky = 'ew')

# bottom frame
bottomFrame = tk.Frame(root, width = 1500, height = 200)
bottomFrame.grid(row = 4, column = 0, columnspan = 3, sticky = 'nsew')

# set grid
root.columnconfigure(0, weight = 1)
root.columnconfigure(1, weight = 0)
root.columnconfigure(2, weight = 1)
root.rowconfigure(0, weight = 1)
root.rowconfigure(1, weight = 0)
root.rowconfigure(2, weight = 1)
root.rowconfigure(3, weight = 0)
root.rowconfigure(4, weight = 1)

# widgets in topLeftFrame
# sign in stuff
Label(topLeftFrame, text = 'Name: ').grid(row = 0, column = 0)
nameEntry = Entry(topLeftFrame)
nameEntry.grid(row = 0, column = 1)

Label(topLeftFrame, text = 'Current User: ').grid(row = 1, column = 0)

currUserInputDisplay = Label(topLeftFrame, text = ' ')
currUserInputDisplay.grid(row = 1, column = 1)
def updateCurrUserName():
    currUserInputDisplay.config(text = nameEntry.get())
    
signInButton = Button(topLeftFrame, text = 'Sign In', command = updateCurrUserName)
signInButton.grid(row = 2, column = 1)

#manifest stuff
Label(topLeftFrame, text = 'Current Manifest: ').grid(row = 1, column = 2)

currManifestFileDisplay = Label(topLeftFrame, text = ' ')
currManifestFileDisplay.grid(row = 1, column = 3)
def selectAndUpdateCurrManifestName():
	desktopPath = os.path.join(os.path.expanduser("~"), "Desktop")
	filePath = filedialog.askopenfilename(initialdir = desktopPath, title = 'Select file', filetypes = (('Text files', '*.txt'),))
	fileName = os.path.basename(filePath)
	currManifestFileDisplay.config(text = fileName)

selectManifestButton = Button(topLeftFrame, text = 'Select Manifest', command = selectAndUpdateCurrManifestName)
selectManifestButton.grid(row = 2, column = 2)

# task stuff
Label(topLeftFrame, text = 'Current Task: ').grid(row = 1, column = 4)



root.mainloop()