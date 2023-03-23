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

import time
import container as Container
import optimizer
import grid as Grid


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.tk.eval("package require Tix")
        self.root.title("Container Movement Optimizer")
        self.root.geometry("1400x700")
        # self.root.configure(background = "white")
        self.bayListMain = [[None * 12] * 8]
        self.bayListOffload = []

        self.log_file_name = "".join(["KeoghLongBeach", str(time.localtime()[0]), ".txt"])
        self.log_folder_path = "C:\CMO\logs"
        if not os.path.exists(self.log_folder_path):
            os.makedirs(self.log_folder_path)
        self.log_path = os.path.join(self.log_folder_path, self.log_file_name)
        if not os.path.exists(self.log_path):
            open(self.log_path, "a").close()

        self.user = None
        self.manifest = None
        self.task = None
        self.offloadList = []
        self.onloadList = []
        self.bufferList = []
        self.current_step = 0
        self.total_steps = 999
        self.ship_bay = Grid.ShipBay()
        self.buffer = Grid.Buffer()
        self.optimizer = optimizer.Optimizer()
        self.animation = None
        self.time_estimate = 0
        self.onloadSelected = False
        self.offloadSelected = False

        self.initUI()

        self.root.mainloop()

    def initUI(self):
        # self.style = ttk.Style()
        # self.style.configure('Thin.TSeparator', background = 'black', thickness = 3)

        # top left frame
        self.topLeftFrame = tk.Frame(self.root, width=800)  # background = '#ffe6cd', height = 20)
        self.topLeftFrame.grid(row=0, column=0)  # sticky = 'ew')

        # separator bw topLeftFrame and topRightFrame
        # self.vertseparator1 = ttk.Separator(self.root, orient = "vertical", style = "Thin.TSeparator")
        # self.vertseparator1.grid(row = 0, column = 1, sticky = "ns")

        # top right frame
        self.topRightFrame = tk.Frame(self.root, width=600)  # background = '#d5e8d4', height = 20)
        self.topRightFrame.grid(row=0, column=1)  # sticky = 'ew')

        # separator bw topRightFrame-topLeftFrame and middleFrame
        # self.horzseparator1 = ttk.Separator(self.root, orient = "horizontal", style = "Thin.TSeparator")
        # self.horzseparator1.grid(row = 1, column = 0, columnspan = 3, sticky = "ew")

        # middle frame
        self.middleFrame = tk.Frame(self.root, width=1400, height=400)
        self.middleFrame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        # middle left frame
        self.middleLeftFrame = tk.Frame(self.middleFrame, width=800, height=400)
        self.middleLeftFrame.grid(row=0, column=0, ipady=50, ipadx=50)
        # self.middleFrame.add(self.middleLeftFrame)

        # middle right frame
        self.middleRightFrame = tk.Frame(self.middleFrame, width=600, height=400)
        self.middleRightFrame.grid(row=0, column=1, ipady=50, ipadx=50)
        # self.middleFrame.add(self.middleRightFrame)

        # separator bw middleFrame and bottomFrame
        # self.horzseparator2 = ttk.Separator(self.root, orient = "horizontal", style = "Thin.TSeparator")
        # self.horzseparator2.grid(row = 2, column = 0, columnspan = 3, sticky = "ew")

        # bottom top frame
        self.bottomTopFrame = tk.Frame(self.root, width=1400, height=250)
        self.bottomTopFrame.grid(row=2, column=0, columnspan=2, sticky="nsew")
        self.bottomTopFrame.columnconfigure(0, weight=1)
        self.bottomTopFrame.rowconfigure(0, weight=1)

        # bottom bottom frame
        self.bottomBottomFrame = tk.Frame(self.root, width=1400, height=50)
        self.bottomBottomFrame.grid(row=3, column=0, columnspan=2, sticky="nsew")
        self.bottomBottomFrame.columnconfigure(0, weight=1)
        self.bottomBottomFrame.rowconfigure(0, weight=1)

        # set grid
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        # self.root.columnconfigure(2, weight = 1)
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        # self.root.rowconfigure(3, weight = 0)
        # self.root.rowconfigure(4, weight = 1)

        # widgets in topLeftFrame
        # sign in stuff
        tk.Label(self.topLeftFrame, text="Enter User: ").grid(row=0, column=0)
        self.nameEntry = tk.Entry(self.topLeftFrame)
        self.nameEntry.grid(row=0, column=1)

        tk.Label(self.topLeftFrame, text="Current User: ").grid(row=1, column=0)

        self.currUserInputDisplay = tk.Label(self.topLeftFrame, text=" ")
        self.currUserInputDisplay.grid(row=1, column=1)

        self.signInButton = tk.Button(self.topLeftFrame, text="Sign In", command=self.change_user)
        self.signInButton.grid(row=0, column=2)

        # manifest stuff
        tk.Label(self.topLeftFrame, text="Current Manifest: ").grid(row=2, column=0)

        self.currManifestFileDisplay = tk.Label(self.topLeftFrame, text=" ")
        self.currManifestFileDisplay.grid(row=2, column=1)

        self.selectManifestButton = tk.Button(self.topLeftFrame, text="Select Manifest", command=self.load_manifest)
        self.selectManifestButton.grid(row=2, column=2)

        # task stuff
        tk.Label(self.topLeftFrame, text="Current Task: ").grid(row=3, column=0)

        self.currTaskDisplay = tk.Label(self.topLeftFrame, text=" ")
        self.currTaskDisplay.grid(row=3, column=1)

        self.taskSelectorButton = tk.Button(self.topLeftFrame, text="Select Task", command=self.choose_task)
        self.taskSelectorButton.grid(row=3, column=2)

        # widgets in topRightFrame
        # step stuff
        tk.Label(self.topRightFrame, text="Step ").grid(row=0, column=0)
        self.currStepDisplay = tk.Label(self.topRightFrame, text=" ")
        self.currStepDisplay.grid(row=0, column=1)

        # time esitmate stuff
        tk.Label(self.topRightFrame, text="Estimated Time Remaining: ").grid(row=1, column=0)
        self.currTimeEstimateDisplay = tk.Label(self.topRightFrame, text=" ")
        self.currTimeEstimateDisplay.grid(row=1, column=1)

        # advance step stuff
        self.nextStepButton = tk.Button(self.topRightFrame, text="Next Step", command=self.progress_animation)
        self.nextStepButton.grid(row=2, column=0, columnspan=2)

        # widgets in bottomTopFrame
        # log file stuff
        self.logFileDisplay = tk.Text(self.bottomTopFrame)  # width = 1500, height = 200)
        self.logFileDisplay.grid(row=0, column=0, sticky="nsew")

        self.update_log_viewer()

        # widgets in bottomBottomFrame
        # comment stuff
        self.commentEntry = tk.Entry(self.bottomBottomFrame)
        self.commentEntry.grid(row=0, column=0, sticky="nsew")
        self.commentButton = tk.Button(self.bottomBottomFrame, text="Add", command=self.get_comment)
        self.commentButton.grid(row=0, column=1, padx=5, pady=5)

    def change_user(self):
        self.user = self.nameEntry.get()
        self.currUserInputDisplay.config(text=self.user)
        self.write_to_log("User changed to %s" % self.user)

    def write_to_log(self, string):
        log = open(self.log_path, "a", encoding="ascii")
        log_time = time.localtime()[0:5]
        log.write("%s/%s/%s %s:%s : %s\n" % (log_time[0], log_time[1], log_time[2], log_time[3], log_time[4], string))
        log.close()
        self.update_log_viewer()

    def load_manifest(self):
        desktopPath = os.path.join(os.path.expanduser("~"), "Desktop")
        filePath = filedialog.askopenfilename(initialdir=desktopPath, title="Select file", filetypes=(("Text files", "*.txt"),))
        fileName = os.path.basename(filePath)
        self.currManifestFileDisplay.config(text=fileName)
        self.manifest = filePath
        self.write_to_log("Manifest %s has been selected. Parsing manifest..." % (self.manifest))
        self.read_manifest()
        self.write_to_log("Parsing manifest %s is complete." % (self.manifest))
        self.display_bay_grid()
        self.display_buffer_grid()

    def update_log_viewer(self):
        self.logFileDisplay["state"] = "normal"
        with open(self.log_path, "r") as logFile:
            logFileLines = logFile.readlines()
        lastThreeLines = logFileLines[-3:]
        self.logFileDisplay.delete("1.0", "end")
        for logFileLines in lastThreeLines:
            self.logFileDisplay.insert("end", logFileLines)
        self.logFileDisplay["state"] = "disabled"

    def progress_animation(self):
        if self.current_step < self.total_steps:
            self.current_step += 1
        self.currStepDisplay.config(text=str(self.current_step) + "/" + str(self.total_steps))
        self.display_animation()

    def update_time_estimate(self):
        hours = self.time_estimate / 60
        minutes = self.time_estimate % 60
        self.currTimeEstimateDisplay.config(text="%2dH %2dM" % (hours, minutes))

    # task selection pop up
    def choose_task(self):
        self.taskSelectorPopup = Toplevel(self.root)
        self.taskSelectorPopup.title("Select Task")
        self.offOnLoadButton = tk.Button(self.taskSelectorPopup, text="OffLoad/Onload", command=self.offload_onload_selection)
        self.offOnLoadButton.grid(row=0, column=0, padx=100, pady=100)
        self.balancingButton = tk.Button(self.taskSelectorPopup, text="Balancing", command=self.balance_selection)
        self.balancingButton.grid(row=0, column=1, padx=100, pady=100)

    # offload/onload pop up
    def offload_onload_selection(self):
        self.task = "Loading"
        self.currTaskDisplay.config(text=self.task)
        self.taskSelectorPopup.withdraw()
        self.start_offload_selection()
        self.start_onload_selection()

    def balance_selection(self):
        self.task = "Balancing"
        self.currTaskDisplay.config(text=self.task)
        self.taskSelectorPopup.withdraw()
        self.calculate_balance()

    # offload pop up
    def start_offload_selection(self):
        self.offloadPopup = Toplevel(self.root)
        self.offloadPopup.geometry("400x400")
        self.offloadPopup.title("Offload")
        self.selectedContainer = None
        tk.Label(self.offloadPopup, text="Container Name: ").grid(row=0, column=0)
        self.searchEntry = tk.Entry(self.offloadPopup)
        self.searchEntry.grid(row=0, column=1)
        self.searchButton = tk.Button(self.offloadPopup, text="Search", command=self.search_offload_containers)
        self.searchButton.grid(row=0, column=2, padx=20, pady=20)
        self.containerGrid = tk.Frame(self.offloadPopup)
        self.containerGrid.grid(row=1, column=0, columnspan=3)
        for row in range(8):
            for column in range(12):
                containerBox = tk.Frame(self.containerGrid, background="white", bd=4, relief="raised", width=30, height=30)
                containerBox.grid(row=row, column=column)
                container = self.ship_bay.get_container(row, column)

                containerName = tix.Balloon(self.containerGrid, initwait=50)
                containerName.bind_widget(containerBox, balloonmsg=container.get_description() if container is not None else "None")
                self.bayListOffload.append((container.get_description() if container is not None else "None", containerBox))
                containerBox.bind("<Button-1>", lambda event, row=row, column=column: self.select_offload_container(row, column))
        self.offloadDoneButton = tk.Button(self.offloadPopup, text="Done", command=self.end_offload_selection)
        self.offloadDoneButton.grid(row=2, column=0, columnspan=3, padx=20, pady=20)

    def search_offload_containers(self):
        query = self.searchEntry.get().lower()
        for container in self.bayListOffload:
            containerName = container[0].lower()
            if query in containerName:
                container[1].configure(background="yellow")
            else:
                container[1].configure(background="white")

    def select_offload_container(self, row, column):
        container = self.bayListOffload[row * 12 + column]
        container[1].configure(background="green")
        self.offloadList.append(Container.Container(0, container[0]))

    def end_offload_selection(self):
        self.offloadPopup.withdraw()
        self.offloadSelected = True
        self.calculate_loading()

    # onload pop up
    def start_onload_selection(self):
        self.onloadPopup = Toplevel(self.root)
        self.onloadPopup.geometry("300x300")
        self.onloadPopup.title("Onload")
        tk.Label(self.onloadPopup, text="Container Name: ").grid(row=0, column=0)
        self.onloadName = tk.Entry(self.onloadPopup)
        self.onloadName.grid(row=0, column=1)
        tk.Label(self.onloadPopup, text="Container Weight: ").grid(row=1, column=0)
        self.onloadWeight = tk.Entry(self.onloadPopup)
        self.onloadWeight.grid(row=1, column=1)
        tk.Label(self.onloadPopup, text="Container Quantity: ").grid(row=2, column=0)
        self.onloadQuantity = tk.Spinbox(self.onloadPopup, from_=1, to=96, increment=1)
        self.onloadQuantity.grid(row=2, column=1)
        self.onloadAddButton = tk.Button(self.onloadPopup, text="Add", command=lambda: self.onloadList.extend([Container.Container(self.onloadWeight.get(), self.onloadName.get())] * int(self.onloadQuantity.get())))
        self.onloadAddButton.grid(row=3, column=0, padx=20, pady=20)
        self.onloadDoneButton = tk.Button(self.onloadPopup, text="Done", command=self.end_onload_selection)
        self.onloadDoneButton.grid(row=3, column=1, padx=20, pady=20)

    def end_onload_selection(self):
        self.onloadPopup.withdraw()
        self.onloadSelected = True
        self.calculate_loading()

    def calculate_loading(self):
        if self.onloadSelected and self.offloadSelected:
            print(self.onloadList)
            print(self.offloadList)
            self.generate_animation(self.optimizer.load(self.ship_bay, self.buffer, self.onloadList, self.offloadList))

    def calculate_balance(self):
        self.generate_animation(self.optimizer.balance(self.ship_bay, self.buffer))

    def get_root(self):
        return self.root

    def generate_animation(self, move_tree):
        num_steps = 0
        move = move_tree[0]
        animation = []
        time_total = 0
        while move is not None:
            print("Move %s from %s to %s" % (move.get_container(), move.get_init_pos(), move.get_end_pos()))
            print(move.get_bay())
            num_steps += 1
            time_total += move.get_cost()
            animation.append(move)
            move = move.get_parent_move()

        self.total_steps = num_steps - 1
        self.time_estimate = time_total
        self.animation = animation

    def display_animation(self):
        index = self.total_steps - 1 - self.current_step
        curr_move = self.animation[index]
        curr_bay = curr_move.get_bay()
        curr_cost = curr_move.get_cost()
        curr_buff = curr_move.get_buffer()
        curr_move_end_in_bay = curr_move.get_in_bay()
        prev_move_end_in_bay = self.animation[index - 1].get_in_bay()
        animation = curr_move.get_animation()
        for i in range(96):
            bay_loc = curr_bay.index_mapper(i)

            s_row = bay_loc[0]
            s_column = bay_loc[1]

            buff_loc = curr_buff.index_mapper(i)

            b_row = buff_loc[0]
            b_column = buff_loc[1]

            ship_cont = curr_bay.get_container(s_row, s_column)
            buff_cont = curr_buff.get_container(b_row, b_column)
            self.bayListMain[i][0].bind_widget(self.bayListMain[i][1], balloonmsg=ship_cont.get_description() if ship_cont is not None else "None")
            self.bufferList[i][0].bind_widget(self.bufferList[i][1], balloonmsg=buff_cont.get_description() if buff_cont is not None else "None")
            # self.bayListMain[i][0] = Container.get_description()
            # containerName = tk.Label(self.bayList.get(i), text = container.get_description(), background = 'white', width = 10, height = 2)
        for i in range(96):
            bay_loc = curr_bay.index_mapper(i)
            buff_loc = curr_buff.index_mapper(i)
            if curr_move_end_in_bay and prev_move_end_in_bay:
                if bay_loc == animation[0]:
                    self.bayListMain[i][1].config(background="blue")
                    self.bayListMain[i][1].config(text="1")
                elif bay_loc == animation[1]:
                    self.bayListMain[i][1].config(background="green")
                    self.bayListMain[i][1].config(text="2")
                elif bay_loc == animation[2]:
                    self.bayListMain[i][1].config(background="yellow")
                    self.bayListMain[i][1].config(text="3")
            elif curr_move_end_in_bay and not prev_move_end_in_bay:
                if buff_loc == animation[0]:
                    self.bufferList[i][1].config(background="blue")
                    self.bufferList[i][1].config(text="1")
                elif bay_loc == animation[2]:
                    self.bayListMain[i][1].config(background="yellow")
                    self.bayListMain[i][1].config(text="3")
            elif not curr_move_end_in_bay and prev_move_end_in_bay:
                if buff_loc == animation[2]:
                    self.bufferList[i][1].config(background="blue")
                    self.bufferList[i][1].config(text="3")
                elif bay_loc == animation[0]:
                    self.bayListMain[i][1].config(background="blue")
                    self.bayListMain[i][1].config(text="1")
            elif not curr_move_end_in_bay and not prev_move_end_in_bay:
                if buff_loc == animation[0]:
                    self.bufferList[i][1].config(background="blue")
                    self.bufferList[i][1].config(text="1")
                elif buff_loc == animation[1]:
                    self.bufferList[i][1].config(background="green")
                    self.bufferList[i][1].config(text="2")
                elif buff_loc == animation[2]:
                    self.bufferList[i][1].config(background="yellow")
                    self.bufferList[i][1].config(text="3")
            else:
                self.bayListMain[i][1].config(background="white")
                self.bayListMain[i][1].config(text="")
                self.bufferList[i][1].config(background="white")
                self.bufferList[i][1].config(text="")
        self.time_estimate -= curr_cost
        self.update_time_estimate()

    def read_manifest(self):
        manifest_file = open(self.manifest, "r", encoding="ascii")
        for line in manifest_file:
            line = line.replace("[", "").replace("]", "").replace("{", "").replace("}", "")
            data = line.split(",")
            if str(data[3].strip()) != "UNUSED":
                row = self.ship_bay.get_height() - int(data[0])
                column = int(data[1]) - 1
                cont = Container.Container(weight=int(data[2].strip()), description=str(data[3].strip()), on_ship=True)
                self.ship_bay.add_container(cont, row, column)
        self.ship_bay.convert_grid_to_stack()
        manifest_file.close()

    def update_manifest(self):
        manifest = open(self.manifest, "w", encoding="ascii")
        for i in self.ship_bay.get_grid():
            for j in i:
                manifest.write(j.manifest_format())

    def display_buffer_grid(self):
        for row in range(4):
            for column in range(24):
                containerBox = tk.Frame(self.middleLeftFrame, background="white", bd=4, relief="raised", width=30, height=30)
                containerBox.grid(row=row, column=column)
                containerName = tix.Balloon(self.middleLeftFrame, initwait=50)
                container = self.buffer.get_container(row, column)
                containerName.bind_widget(containerBox, balloonmsg=container.get_description() if container is not None else "None")
                self.bufferList.append((containerName, containerBox))

    def display_bay_grid(self):
        for row in range(8):
            for column in range(12):
                containerBox = tk.Frame(self.middleRightFrame, background="white", bd=4, relief="raised", width=30, height=30)
                containerBox.grid(row=row, column=column)
                containerName = tix.Balloon(self.middleRightFrame, initwait=50)
                container = self.ship_bay.get_container(row, column)
                containerName.bind_widget(containerBox, balloonmsg=container.get_description() if container is not None else "None")
                self.bayListMain.append((containerName, containerBox))
                # containerName = tk.Label(containerBox, text = '%s,%s'%(row, column), width = 4, height = 2).grid(row = 0, column = 0)

    # get funcs
    def get_transfer_lists(self):
        return self.offloadList, self.onloadList

    def get_task(self):
        return self.task

    def get_user(self):
        return self.user

    def get_manifest(self):
        return self.manifest

    def get_comment(self):
        return self.commentEntry


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

GUI()
