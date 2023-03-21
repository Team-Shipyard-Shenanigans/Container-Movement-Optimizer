import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import tix
from tkinter.constants import *
from tkinter import *
# import tkinter.tix as tix
# from tkinter.tix import Balloon
# from ttkwidgets import Balloon

# import cmo_runner as cmor

class GUI:
	def __init__(self):
		self.root = tk.Tk()
		self.root.tk.eval('package require Tix')
		self.root.title("Container Movement Optimizer")
		self.root.geometry("1400x700")
		# self.root.configure(background = "white")

		self.user = None
		self.manifest = None
		self.task = None
		self.log_path = 'KeoghLongBeach.txt'
		self.offloadList = []
		self.onloadList = []
		self.bufferList = []
		self.bayListMain = []
		self.bayListOffload = []

		self.userChanged = False
		self.manifestSelected = False
		self.taskSelected = False
		self.transferListUploaded = False

		self.initUI()
		self.root.mainloop()

	def initUI(self):
		# self.style = ttk.Style()
		# self.style.configure('Thin.TSeparator', background = 'black', thickness = 3)

		# top left frame
		self.topLeftFrame = tk.Frame(self.root, width = 800) #background = '#ffe6cd', height = 20)
		self.topLeftFrame.grid(row = 0, column = 0) #sticky = 'ew')

		# separator bw topLeftFrame and topRightFrame
		# self.vertseparator1 = ttk.Separator(self.root, orient = "vertical", style = "Thin.TSeparator")
		# self.vertseparator1.grid(row = 0, column = 1, sticky = "ns")

		# top right frame
		self.topRightFrame = tk.Frame(self.root, width = 600) #background = '#d5e8d4', height = 20)
		self.topRightFrame.grid(row = 0, column = 1) #sticky = 'ew')

		# separator bw topRightFrame-topLeftFrame and middleFrame
		# self.horzseparator1 = ttk.Separator(self.root, orient = "horizontal", style = "Thin.TSeparator")
		# self.horzseparator1.grid(row = 1, column = 0, columnspan = 3, sticky = "ew")

		# middle frame
		self.middleFrame = tk.Frame(self.root, width = 1400, height = 400)
		self.middleFrame.grid(row = 1, column = 0, columnspan = 2, sticky = 'nsew')

		# middle left frame
		self.middleLeftFrame = tk.Frame(self.middleFrame, width = 800, height = 400)
		self.middleLeftFrame.grid(row = 0, column = 0, ipady = 50, ipadx = 50)
		# self.middleFrame.add(self.middleLeftFrame)

		# middle right frame
		self.middleRightFrame = tk.Frame(self.middleFrame, width = 600, height = 400)
		self.middleRightFrame.grid(row = 0, column = 1, ipady = 50, ipadx = 50)
		# self.middleFrame.add(self.middleRightFrame)

		# separator bw middleFrame and bottomFrame
		# self.horzseparator2 = ttk.Separator(self.root, orient = "horizontal", style = "Thin.TSeparator")
		# self.horzseparator2.grid(row = 2, column = 0, columnspan = 3, sticky = "ew")

		# bottom top frame
		self.bottomTopFrame = tk.Frame(self.root, width = 1400, height = 250)
		self.bottomTopFrame.grid(row = 2, column = 0, columnspan = 2, sticky = 'nsew')
		self.bottomTopFrame.columnconfigure(0, weight = 1)
		self.bottomTopFrame.rowconfigure(0, weight = 1)

		# bottom bottom frame
		self.bottomBottomFrame = tk.Frame(self.root, width = 1400, height = 50)
		self.bottomBottomFrame.grid(row = 3, column = 0, columnspan = 2, sticky = 'nsew')
		self.bottomBottomFrame.columnconfigure(0, weight = 1)
		self.bottomBottomFrame.rowconfigure(0, weight = 1)

		# set grid
		self.root.columnconfigure(0, weight = 1)
		self.root.columnconfigure(1, weight = 1)
		# self.root.columnconfigure(2, weight = 1)
		self.root.rowconfigure(0, weight = 0)
		self.root.rowconfigure(1, weight = 1)
		self.root.rowconfigure(2, weight = 1)
		# self.root.rowconfigure(3, weight = 0)
		# self.root.rowconfigure(4, weight = 1)

		# widgets in topLeftFrame
		# sign in stuff
		tk.Label(self.topLeftFrame, text = 'Enter User: ').grid(row = 0, column = 0)
		self.nameEntry = tk.Entry(self.topLeftFrame)
		self.nameEntry.grid(row = 0, column = 1)

		tk.Label(self.topLeftFrame, text = 'Current User: ').grid(row = 1, column = 0)

		self.currUserInputDisplay = tk.Label(self.topLeftFrame, text = ' ')
		self.currUserInputDisplay.grid(row = 1, column = 1)
			
		self.signInButton = tk.Button(self.topLeftFrame, text = 'Sign In', command = self.updateCurrUser)
		self.signInButton.grid(row = 0, column = 2)

		#manifest stuff
		tk.Label(self.topLeftFrame, text = 'Current Manifest: ').grid(row = 2, column = 0)

		self.currManifestFileDisplay = tk.Label(self.topLeftFrame, text = ' ')
		self.currManifestFileDisplay.grid(row = 2, column = 1)

		self.selectManifestButton = tk.Button(self.topLeftFrame, text = 'Select Manifest', command = self.updateCurrManifest)
		self.selectManifestButton.grid(row = 2, column = 2)

		# task stuff
		tk.Label(self.topLeftFrame, text = 'Current Task: ').grid(row = 3, column = 0)

		self.currTaskDisplay = tk.Label(self.topLeftFrame, text = ' ')
		self.currTaskDisplay.grid(row = 3, column = 1)
			
		self.taskSelectorButton = tk.Button(self.topLeftFrame, text = 'Select Task', command = self.updateCurrTask)
		self.taskSelectorButton.grid(row = 3, column = 2)

		# widgets in topRightFrame
		# step stuff
		tk.Label(self.topRightFrame, text = 'Step ').grid(row = 0, column = 0)
		self.currStepDisplay = tk.Label(self.topRightFrame, text = ' ')
		self.currStepDisplay.grid(row = 0, column = 1)

		# time esitmate stuff
		tk.Label(self.topRightFrame, text = 'Estimated Time Remaining: ').grid(row = 1, column = 0)
		self.currTimeEstimateDisplay = tk.Label(self.topRightFrame, text = ' ')
		self.currTimeEstimateDisplay.grid(row = 1, column = 1)

		# advance step stuff
		self.nextStepButton = tk.Button(self.topRightFrame, text = 'Next Step', command = self.nextStepAnimation)
		self.nextStepButton.grid(row = 2, column = 0, columnspan = 2)

		# widgets in middleFrame
		# buffer stuff (middleLeftFrame)
		self.bufferGrid()

		# bay stuff (middleRightFrame)
		self.bayGrid()

		# widgets in bottomTopFrame
		# log file stuff
		self.logFileDisplay = tk.Text(self.bottomTopFrame) #width = 1500, height = 200)
		self.logFileDisplay.grid(row = 0, column = 0, sticky = 'nsew')

		self.updateLogFile()

		# widgets in bottomBottomFrame
		# comment stuff
		self.commentEntry = tk.Entry(self.bottomBottomFrame)
		self.commentEntry.grid(row = 0, column = 0, sticky = 'nsew')
		self.commentButton = tk.Button(self.bottomBottomFrame, text = 'Add', command = self.getComment)
		self.commentButton.grid(row = 0, column = 1, padx = 5, pady = 5)

	def updateCurrUser(self):
		self.user = self.nameEntry.get()
		self.userChanged = True
		self.currUserInputDisplay.config(text = self.user)

	def updateCurrManifest(self):
		desktopPath = os.path.join(os.path.expanduser("~"), "Desktop")
		filePath = filedialog.askopenfilename(initialdir = desktopPath, title = 'Select file', filetypes = (('Text files', '*.txt'),))
		fileName = os.path.basename(filePath)
		self.currManifestFileDisplay.config(text = fileName)
		self.manifest = filePath

	def updateLogFile(self):
		self.logFileDisplay['state'] = 'normal'
		with open(self.log_path, 'r') as logFile:
			logFileLines = logFile.readlines()
		lastThreeLines = logFileLines[-3:]
		for logFileLines in lastThreeLines:
			self.logFileDisplay.insert('end', logFileLines)
		self.logFileDisplay['state'] = 'disabled'
	
	def updateCurrStep(self, currStep, totalSteps):
		self.currStepDisplay.config(text = str(currStep) + '/' + str(totalSteps))
		self.stepCompleted = False

	def nextStepAnimation(self):
		self.stepCompleted = True

	def updateCurrTimeEstimate(self, currTimeEstimate):
		self.currTimeEstimateDisplay.config(text = str(currTimeEstimate))

	def updateCurrTask(self):
		# self.task = taskString
		# self.taskSelected = True
		# self.currTaskDisplay.config(text = self.task)
		self.taskSelectorWin()

	# task selection pop up
	def taskSelectorWin(self):
		self.taskSelectorPopup = Toplevel(self.root)
		self.taskSelectorPopup.title('Select Task')
		self.offOnLoadButton = tk.Button(self.taskSelectorPopup, text = 'OffLoad/Onload', command = self.offOnLoad)
		self.offOnLoadButton.grid(row = 0, column = 0, padx = 100, pady = 100)
		self.balancingButton = tk.Button(self.taskSelectorPopup, text = 'Balancing', command = self.balancing)
		self.balancingButton.grid(row = 0, column = 1, padx = 100, pady = 100)

	# offload/onload pop up
	def offOnLoad(self):
		self.task = 'Offload/Onload'
		self.taskSelected = True
		self.currTaskDisplay.config(text = self.task)
		self.taskSelectorPopup.withdraw()
		self.startOffload()
		self.startOnload()

	# offload pop up
	def startOffload(self):
		self.offloadPopup = Toplevel(self.root)
		self.offloadPopup.geometry('400x400')
		self.offloadPopup.title('Offload')
		self.selectedContainer = None
		tk.Label(self.offloadPopup, text = 'Container Name: ').grid(row = 0, column = 0)
		self.searchEntry = tk.Entry(self.offloadPopup)
		self.searchEntry.grid(row = 0, column = 1)
		self.searchButton = tk.Button(self.offloadPopup, text = 'Search', command = self.searchContainers)
		self.searchButton.grid(row = 0, column = 2, padx = 20, pady = 20)
		self.containerGrid = tk.Frame(self.offloadPopup)
		self.containerGrid.grid(row = 1, column = 0, columnspan = 3)
		for row in range(8):
			for column in range(12):
				containerBox = tk.Frame(self.containerGrid, background = 'white', bd = 4, relief = 'raised', width = 30, height = 30)
				containerBox.grid(row = row, column = column) 
				containerName = tk.Label(containerBox, text = '%s,%s'%(row, column))   
				# containerBox.bind("<Enter>", containerName.place(x=event.x_root, y=event.y_root))
				# containerBox.bind("<Leave>", containerName.place_forget())
				containerName = tix.Balloon(self.containerGrid, initwait = 50)
				containerName.bind_widget(containerBox, balloonmsg = '%s,%s'%(row, column))
				self.bayListOffload.append(('%s,%s'%(row, column), containerBox))
				containerBox.bind('<Button-1>', lambda event, row = row, column = column: self.selectContainer(row, column))
	# 	self.offloadNameSearched = tk.StringVar(self.offloadPopup)
	# 	self.offloadNameSearched.trace('w', lambda name, index, mode, var = self.offloadNameSearched: self.updateContainers(var))
	# 	self.offloadName = tk.Entry(self.offloadPopup, textvariable = self.offloadNameSearched)
	# 	self.offloadName.grid(row = 0, column = 0)
	# 	self.offloadDropdown = tk.OptionMenu(self.offloadPopup, self.offloadNameSearched, *self.bayList)
	# 	self.offloadDropdown.grid(row = 1, column = 0)
	# 	# self.updateContainers()
		self.offloadDoneButton = tk.Button(self.offloadPopup, text = 'Done', command = self.endOffload)
		self.offloadDoneButton.grid(row = 2, column = 0, columnspan = 3, padx = 20, pady = 20)
	# 	# bind close button to closeOffloadPopup function
	# 	# self.offloadPopup.protocol("WM_DELETE_WINDOW", self.closeOffloadPopup)
	
	# def show_tooltip(self, event):
	# 	containerName.place(x=event.x_root, y=event.y_root)

	# def hide_tooltip(self, event):
	# 	containerName.place_forget()

	def searchContainers(self):
		query = self.searchEntry.get().lower()
		print(query)
		for container in self.bayListOffload:
			# container[0].motion(container[1])
			containerName = container[0].lower()
			print(containerName)
			# containerName = container[0].subwidget_list['label'].cget('text').lower()
			if query in containerName:
				container[1].configure(background = 'yellow')
			else:
				container[1].configure(background = 'white')
                
	def selectContainer(self, row, column):
		container = self.bayListOffload[row*12 + column]
		container[1].configure(background = 'green')
		self.offloadList.extend(container[0])
		print(self.offloadList)
	# 	self.selectedContainer = container
        
	# def getSelectedContainer(self):
	# 	if self.selectedContainer is not None:
	# 		return self.selectedContainer[0]
	# 	else:
	# 		return None

	# def updateContainers(self, var):
	# 	query = var.get().lower()
	# 	filteredContainersMatch = [containers for containers in self.bayList if query in containers.lower()]
	# 	filteredContainersMatchDropdown = self.offloadDropdown['menu']
	# 	filteredContainersMatchDropdown.delete(0, 'end')
	# 	for containers in filteredContainersMatch:
	# 		if query.lower() in containers.lower():
	# 			filteredContainersMatchDropdown.add_command(label = containers, command = tk._setit(self.offloadNameSearched, containers))

	# def closeOffloadPopup(self):
	# 	self.offloadPopup.withdraw()

	def endOffload(self):
		# if self.offloadPopup == self.offloadPopup.focus_get():
		self.offloadPopup.withdraw()
		# self.offloadList = self.optionSelected.get()
		self.transferListUploaded = True
		# send offload list to algo

	# onload pop up
	def startOnload(self):
		self.onloadPopup = Toplevel(self.root)
		self.onloadPopup.geometry('300x300')
		self.onloadPopup.title('Onload')
		tk.Label(self.onloadPopup, text = 'Container Name: ').grid(row = 0, column = 0)
		self.onloadName = tk.Entry(self.onloadPopup)
		self.onloadName.grid(row = 0, column = 1)
		tk.Label(self.onloadPopup, text = 'Container Quantity: ').grid(row = 1, column = 0)
		self.onloadQuantity = tk.Spinbox(self.onloadPopup, from_ = 1, to = 96, increment = 1)
		self.onloadQuantity.grid(row = 1, column = 1)
		self.onloadAddButton = tk.Button(self.onloadPopup, text = 'Add', command = lambda: self.onloadList.extend([self.onloadName.get()] * int(self.onloadQuantity.get())))
		self.onloadAddButton.grid(row = 2, column = 0, padx = 20, pady = 20)
		self.onloadDoneButton = tk.Button(self.onloadPopup, text = 'Done', command = self.endOnload)
		self.onloadDoneButton.grid(row = 2, column = 1, padx = 20, pady = 20)
		# bind close button to closeOnloadPopup function
		# self.onloadPopup.protocol("WM_DELETE_WINDOW", self.closeOnloadPopup)
	
	# def closeOnloadPopup(self):
	# 	self.onloadPopup.withdraw()

	def endOnload(self):
		# if self.onloadDoneButton == self.onloadPopup.focus_get():
		print(self.onloadList)
		self.onloadPopup.withdraw()
		self.transferListUploaded = True
		# send onload list to algo

	# balancing pop up window
	def balancing(self):
		self.task = 'Balancing'
		self.taskSelected = True
		self.currTaskDisplay.config(text = self.task)
		# send balance command to algo
		self.taskSelectorPopup.withdraw()

	# def updateOffloadList(self):
	# 	self.offloadList = self.offloadEntry.get()
	# 	self.transferListUploaded = True

	# def updateOnloadList(self):
	# 	self.onloadList = self.onloadEntry.get()
	# 	self.transferListUploaded = True

	def updateBay(self, bay):
		self.bay = bay

	def bufferGrid(self):
		for row in range(4):
			for column in range(24):
				containerBox = tk.Frame(self.middleLeftFrame, background = 'white', bd = 4, relief = 'raised', width = 30, height = 30)
				containerBox.grid(row = row, column = column)
				containerName = tix.Balloon(self.middleLeftFrame, initwait = 50)
				containerName.bind_widget(containerBox, balloonmsg = '%s,%s'%(row, column))
				self.bufferList.append((containerName, containerBox))
				
	def bayGrid(self):
		for row in range(8):
			for column in range(12):
				containerBox = tk.Frame(self.middleRightFrame, background = 'white', bd = 4, relief = 'raised', width = 30, height = 30)
				containerBox.grid(row = row, column = column)	
				containerName = tix.Balloon(self.middleRightFrame, initwait = 50)
				containerName.bind_widget(containerBox, balloonmsg = '%s,%s'%(row, column))
				self.bayListMain.append((containerName, containerBox))
				# containerName = tk.Label(containerBox, text = '%s,%s'%(row, column), width = 4, height = 2).grid(row = 0, column = 0)		


	def transferListReady(self):
		return self.transferListUploaded
	
	def updateAnimation(self, bufferAnimation, bayAnimation):
		self.bufferAnimation = bufferAnimation
		for i in range(96):
			location = self.buffer.index_mapper(i)
			if location in self.animation: 
				self.bufferList[i][1].config(background = 'red')
			# containerName = tk.Label(self.bufferList.get(i), text = container.get_description(), background = 'white', width = 10, height = 2)
		
		self.bayAnimation = bayAnimation
		for i in range(96):
			location = self.bay.index_mapper(i)
			if location in self.animation: 
				self.bayListMain[i][1].config(background = 'red')
			# containerName = tk.Label(self.bufferList.get(i), text = container.get_description(), background = 'white', width = 10, height = 2)

	def displayAnimation(self):
		for i in range(96):
			location = self.bay.index_mapper(i)
			row = location[0]
			column = location[1]
			container = self.bay.get_container(row, column)
			self.bayListMain[i][0].bind_widget(self.bayListMain[i][1], balloonmsg = container.get_description())
			# self.bayListMain[i][0] = Container.get_description()
			# containerName = tk.Label(self.bayList.get(i), text = container.get_description(), background = 'white', width = 10, height = 2)

	# get funcs
	def getTransferList(self):
		return self.offloadList, self.onloadList
	
	def getTask(self):
		return self.task
	
	def getUser(self):
		return self.user
	
	def getManifest(self):
		return self.manifest
	
	def getUserChanged(self):
		return self.userChanged
	
	def getManifestSelected(self):
		return self.manifestSelected
	
	def getTaskSelected(self):
		return self.taskSelected
	
	def getTransferListUploaded(self):
		return self.transferListUploaded
	
	def getStepCompleted(self):
		return self.stepCompleted
	
	def getComment(self):
		return self.commentEntry
	
	# set funcs
	def setUserChanged(self, userChanged):
		self.userChanged = userChanged



# class HoverFrame(tk.Frame):
# 	def __init__(self, parent, text):
# 		tk.Frame.__init__(self, parent, bg="white")
# 		self.config(width = 29, height = 29)
# 		self.pack_propagate(0)

#         # Create a label to display the text
# 		self.tooltip_label = tk.Label(self, text=text, bg="white", bd=1, relief="solid", font=('Arial', 8))
# 		self.tooltip_label.place_forget()
        
#         # Bind the Enter and Leave events to show/hide the label
# 		self.bind('<Enter>', self.show_tooltip)
# 		self.bind('<Leave>', self.hide_tooltip)
        
# 	def show_tooltip(self, event):
#         # Position and display the label when the mouse enters the frame
# 		x = self.winfo_rootx() - self.winfo_x()
# 		y = self.winfo_rooty() - self.winfo_y() - 30  # adjust y position to show label above HoverFrame
# 		self.tooltip_label.place(x=x, y=y)
# 		self.tooltip_label.lift()
        
# 	def hide_tooltip(self, event):
#         # Hide the label when the mouse leaves the frame
# 		self.tooltip_label.place_forget()