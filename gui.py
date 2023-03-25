import os
import tkinter as tk
from tkinter import filedialog
from tkinter import tix
from tkinter.constants import *
from tkinter import *


import time
import container as Container
import optimizer
import grid as Grid


class GUI:
    def __init__(self):
        self.root = tix.Tk()
        self.root.title("Container Movement Optimizer")
        self.root.state("zoomed")
        # self.root.configure(background = "white")
        self.bayListMain = []
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
        self.task_complete = False

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
        self.topRightFrame = tk.Frame(self.root, width=600)
        self.topRightFrame.grid(row=0, column=1)  # sticky = 'ew')

        # separator bw topRightFrame-topLeftFrame and middleFrame
        # self.horzseparator1 = ttk.Separator(self.root, orient = "horizontal", style = "Thin.TSeparator")
        # self.horzseparator1.grid(row = 1, column = 0, columnspan = 3, sticky = "ew")

        # middle frame
        self.middleFrame = tk.Frame(self.root)
        self.middleFrame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        # middle left frame
        self.middleLeftFrame = tk.Frame(self.middleFrame)
        self.middleLeftFrame.grid(row=0, column=0, pady=150, sticky="sw")
        # self.middleFrame.add(self.middleLeftFrame)

        # middle right frame
        self.middleRightFrame = tk.Frame(self.middleFrame)
        self.middleRightFrame.grid(row=0, column=1, padx=400, pady=150, sticky="se")
        # self.middleFrame.add(self.middleRightFrame)

        # separator bw middleFrame and bottomFrame
        # self.horzseparator2 = ttk.Separator(self.root, orient = "horizontal", style = "Thin.TSeparator")
        # self.horzseparator2.grid(row = 2, column = 0, columnspan = 3, sticky = "ew")

        # bottom top frame
        self.bottomTopFrame = tk.Frame(self.root, width=1400, height=125)
        self.bottomTopFrame.grid(row=2, column=0, columnspan=2, sticky="sew")
        self.bottomTopFrame.columnconfigure(0, weight=1)
        self.bottomTopFrame.rowconfigure(0, weight=1)

        # bottom bottom frame
        self.bottomBottomFrame = tk.Frame(self.root, width=1400, height=50)
        self.bottomBottomFrame.grid(row=3, column=0, columnspan=2, sticky="sew")
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
        tk.Label(self.topLeftFrame, text="Enter User: ", anchor="w").grid(row=0, column=0, sticky="w")
        self.nameEntry = tk.Entry(self.topLeftFrame)
        self.nameEntry.grid(row=0, column=1)

        tk.Label(self.topLeftFrame, text="Current User: ", anchor="w").grid(row=1, column=0, sticky="w")

        self.currUserInputDisplay = tk.Label(self.topLeftFrame, text=" ")
        self.currUserInputDisplay.grid(row=1, column=1)

        self.signInButton = tk.Button(self.topLeftFrame, text="Sign In", width=12, height=1, command=self.change_user)
        self.signInButton.grid(row=0, column=2, sticky="w")

        # manifest stuff
        tk.Label(self.topLeftFrame, text="Current Manifest: ", anchor="w").grid(row=2, column=0, sticky="w")

        self.currManifestFileDisplay = tk.Label(self.topLeftFrame, text=" ")
        self.currManifestFileDisplay.grid(row=2, column=1)

        self.selectManifestButton = tk.Button(self.topLeftFrame, text="Select Manifest", width=12, height=1, command=self.load_manifest)
        self.selectManifestButton.grid(row=2, column=2)

        # task stuff
        tk.Label(self.topLeftFrame, text="Current Task: ", anchor="w").grid(row=3, column=0, sticky="w")

        self.currTaskDisplay = tk.Label(self.topLeftFrame, text=" ")
        self.currTaskDisplay.grid(row=3, column=1)

        self.taskSelectorButton = tk.Button(self.topLeftFrame, text="Select Task", width=12, height=1, command=self.choose_task)
        self.taskSelectorButton.grid(row=3, column=2)

        # widgets in topRightFrame
        # step stuff
        tk.Label(self.topRightFrame, text="Step: ", anchor="w").grid(row=0, column=0, sticky="w")
        self.currStepDisplay = tk.Label(self.topRightFrame, text=" ")
        self.currStepDisplay.grid(row=0, column=1)

        # time esitmate stuff
        tk.Label(self.topRightFrame, text="Estimated Time Remaining: ", anchor="w").grid(row=1, column=0, sticky="w")
        self.currTimeEstimateDisplay = tk.Label(self.topRightFrame, text=" ")
        self.currTimeEstimateDisplay.grid(row=1, column=1)

        # move instruction stuff
        self.moveInstructionDisplay = tk.Label(self.topRightFrame, text="")
        self.moveInstructionDisplay.grid(row=2, column=0, columnspan=3)

        # advance step stuff
        self.nextStepButton = tk.Button(self.topRightFrame, text="Next Step", width=14, height=1, command=self.progress_animation)
        self.nextStepButton.grid(row=0, column=2)

        # download manifest stuff
        self.dlManifestButton = tk.Button(self.topRightFrame, text="Download Manifest", width=14, height=1, command=self.download_manifest)
        self.dlManifestButton.grid(row=3, column=0, columnspan=3)

        # widgets in bottomTopFrame
        # log file stuff
        self.logFileDisplay = tk.Text(self.bottomTopFrame)  # width = 1500, height = 200)
        self.logFileDisplay.grid(row=0, column=0, sticky="nsew")

        self.update_log_viewer()

        # widgets in bottomBottomFrame
        # comment stuff
        self.commentEntry = tk.Entry(self.bottomBottomFrame)
        self.commentEntry.grid(row=0, column=0, sticky="nsew")
        self.commentButton = tk.Button(self.bottomBottomFrame, text="Add", command=self.add_comment)
        self.commentButton.grid(row=0, column=1, padx=5, pady=5)

    def change_user(self):
        self.user = self.nameEntry.get()
        self.currUserInputDisplay.config(text=self.user)
        self.write_to_log("%s signed in." % self.user)

    def write_to_log(self, string):
        log = open(self.log_path, "a", encoding="ascii")
        log_time = time.localtime()[0:5]
        log.write("%s/%s/%s %s:%s : %s\n" % (log_time[0], log_time[1], log_time[2], log_time[3], log_time[4], string))
        log.close()
        self.update_log_viewer()

    def load_manifest(self):
        if self.user == None:
            self.write_to_log("ERROR: No user has been signed in. Please sign in before choosing a manifest.")
            return
        desktopPath = os.path.join(os.path.expanduser("~"), "Desktop")
        filePath = filedialog.askopenfilename(initialdir=desktopPath, title="Select file", filetypes=(("Text files", "*.txt"),))
        fileName = os.path.basename(filePath)
        self.currManifestFileDisplay.config(text=fileName)
        self.manifest = filePath
        self.write_to_log("Manifest %s has been selected." % (self.manifest))
        self.read_manifest()
        self.write_to_log("Parsing manifest %s is complete." % (self.manifest))
        self.display_bay_grid()
        self.display_buffer_grid()

    def update_log_viewer(self):
        self.logFileDisplay["state"] = "normal"
        with open(self.log_path, "r") as logFile:
            logFileLines = logFile.readlines()
        lastThreeLines = logFileLines[-8:]
        self.logFileDisplay.delete("1.0", "end")
        for logFileLines in lastThreeLines:
            self.logFileDisplay.insert("end", logFileLines)
        self.logFileDisplay["state"] = "disabled"

    def progress_animation(self):
        if self.task is None:
            self.write_to_log("ERROR: No task has been selected. Please select a task before advancing to the next step.")
            return

        if self.current_step < self.total_steps and not self.task_complete:
            self.currStepDisplay.config(text=str(self.current_step + 1) + "/" + str(self.total_steps))
            self.display_animation()
            self.current_step += 1
        else:
            if self.current_step == self.total_steps:
                self.task_complete = True
            if self.task_complete and self.task is not None:
                self.write_to_log("Task %s has been completed." % self.task)
                self.ship_bay = self.animation[0].get_bay()
                self.current_step = 0
                self.total_steps = 999
                self.task = None
                self.currStepDisplay.config(text="")
                self.onloadSelected = False
                self.offloadSelected = False
                self.offloadList = []
                self.onloadList = []

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
        self.task_complete = False
        self.start_offload_selection()
        self.start_onload_selection()

    def balance_selection(self):
        self.task = "Balancing"
        self.currTaskDisplay.config(text=self.task)
        self.task_complete = False
        self.taskSelectorPopup.withdraw()
        self.calculate_balance()

    # offload pop up
    def start_offload_selection(self):
        self.offloadPopup = Toplevel(self.root)
        self.offloadPopup.geometry("500x500")
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
                container = self.ship_bay.get_container(row, column)
                containerBox = tk.Label(self.containerGrid, background="white", bd=4, relief="raised", width=4, height=2, text=container.get_description() if container is not None else "")
                containerBox.grid(row=row, column=column)
                containerBox.grid_propagate(False)
                containerName = tix.Balloon(self.containerGrid)
                containerName.bind_widget(containerBox, balloonmsg=container.get_description() if container is not None else "")
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
            self.write_to_log("Calculating loading...")
            print(self.onloadList)
            print(self.offloadList)
            self.generate_animation(self.optimizer.load(self.ship_bay, self.buffer, self.onloadList, self.offloadList))
            self.write_to_log("Finished calculation, displaying to grid")

    def calculate_balance(self):
        self.generate_animation(self.optimizer.balance(self.ship_bay, self.buffer))

    def get_root(self):
        return self.root

    def generate_animation(self, move_tree):
        num_steps = 0
        move = move_tree[0]
        time_total = 0
        animation = []
        time_total = move.get_cost()
        while move is not None:
            print("Move %s from %s to %s" % (move.get_container(), move.get_init_pos(), move.get_end_pos()))
            print(move.get_bay())
            num_steps += 1
            animation.append(move)
            move = move.get_parent_move()

        self.total_steps = num_steps - 1
        self.time_estimate = time_total
        self.animation = animation
        self.update_time_estimate()
        self.currStepDisplay.config(text=str(self.current_step) + "/" + str(self.total_steps))

    def display_move(self, string):
        self.moveInstructionDisplay.config(text=string)

    def display_animation(self):
        for i in range(96):
            self.bayListMain[i][1].config(background="white")
            self.bufferList[i][1].config(background="white")

        index = self.total_steps - 1 - self.current_step
        curr_move = self.animation[index]
        curr_bay = curr_move.get_bay()
        curr_cost = curr_move.get_cost()
        curr_buff = curr_move.get_buffer()
        curr_move_end_in_bay = curr_move.get_in_bay()
        prev_move_end_in_bay = self.animation[index + 1].get_in_bay()
        animation = curr_move.get_animation()

        self.update_manifest(curr_bay)
        for i in range(96):
            bay_loc = curr_bay.index_mapper(i)

            s_row = bay_loc[0]
            s_column = bay_loc[1]

            buff_loc = curr_buff.index_mapper(i)

            b_row = buff_loc[0]
            b_column = buff_loc[1]

            ship_cont = curr_bay.get_container(s_row, s_column)
            buff_cont = curr_buff.get_container(b_row, b_column)
            self.bayListMain[i][0].bind_widget(self.bayListMain[i][1], balloonmsg=ship_cont.get_description() if ship_cont is not None else "")
            self.bayListMain[i][1].config(text=ship_cont.get_description() if ship_cont is not None else "")
            self.bufferList[i][0].bind_widget(self.bufferList[i][1], balloonmsg=buff_cont.get_description() if buff_cont is not None else "")
            self.bufferList[i][1].config(text=buff_cont.get_description() if buff_cont is not None else "")

        init_pos = animation[0]
        cont_pos = animation[1]
        end_pos = animation[2]
        cont_to_move = curr_move.get_container()
        str_end_pos = ""
        str_init_pos = ""
        str_cont_pos = ""
        if end_pos == (-1, 0):
            str_end_pos = "Ship Bay"
        elif end_pos == (-1, 23):
            str_end_pos = "Buffer"
        else:
            str_end_pos = str((end_pos[0] + 1, end_pos[1] + 2))

        if init_pos == (-1, 0):
            str_init_pos = "Ship Bay"
        elif init_pos == (-1, 23):
            str_init_pos = "Buffer"
        else:
            str_init_pos = str((init_pos[0] + 1, init_pos[1] + 1))

        str_cont_pos = str((cont_pos[0] + 1, cont_pos[1] + 2))

        if cont_pos is not None and cont_to_move is not None:
            if cont_to_move in prev_move_end_in_bay.get_offload_list():
                self.display_move("Step %s: Move Crane from %s to %s, then offload container %s to truck" % (self.current_step + 1, str_init_pos, str_cont_pos, cont_to_move.get_description(), str_end_pos))
                self.write_to_log("Step %s: Move Crane from %s to %s, then offload container %s to truck" % (self.current_step + 1, str_init_pos, str_cont_pos, cont_to_move.get_description(), str_end_pos))
            else:
                self.display_move("Step %s: Move Crane from %s to %s, then move container %s to %s" % (self.current_step + 1, str_init_pos, str_cont_pos, cont_to_move.get_description(), str_end_pos))
                self.write_to_log("Step %s: Move Crane from %s to %s, then move container %s to %s" % (self.current_step + 1, str_init_pos, str_cont_pos, cont_to_move.get_description(), str_end_pos))

        elif cont_to_move is not None and cont_pos is None:
            self.display_move("Step %s: Pickup container %s from %s then load it to %s" % (self.current_step + 1, cont_to_move.get_description(), str_init_pos, str_end_pos))
            self.write_to_log("Step %s: Pickup container %s from %s then load it to %s" % (self.current_step + 1, cont_to_move.get_description(), str_init_pos, str_end_pos))
        else:
            self.display_move("Step %s: Move Crane from %s to %s" % (self.current_step + 1, str_init_pos, str_end_pos))
            self.write_to_log("Step %s: Move Crane from %s to %s" % (self.current_step + 1, str_init_pos, str_end_pos))

        if curr_move_end_in_bay and prev_move_end_in_bay:
            if init_pos == (-1, 0):
                init = 0
            else:
                init = curr_bay.index_unmap(init_pos)
            if end_pos == (-1, 0):
                end = 0
            else:
                end = curr_bay.index_unmap(end_pos) + curr_bay.get_columns()

            if cont_pos is not None:
                cont = curr_bay.index_unmap(cont_pos) + curr_bay.get_columns()
                self.bayListMain[cont][1].config(background="red")

            self.bayListMain[init][1].config(background="blue")
            self.bayListMain[cont][1].config(background="red")
            self.bayListMain[cont][1].config(text=cont_to_move.get_description() if cont_to_move is not None else "")
            self.bayListMain[end][1].config(background="green")
            self.bayListMain[end][1].config(text=cont_to_move.get_description() if cont_to_move is not None else "")

        elif not curr_move_end_in_bay and prev_move_end_in_bay:
            if end_pos == (-1, 23):
                end = 23
            else:
                end = curr_buff.index_unmap(end_pos) + curr_buff.get_columns()
            if init_pos == (-1, 0):
                init = 0
            else:
                init = curr_bay.index_unmap(init_pos)
            if cont_pos is not None:
                cont = curr_bay.index_unmap(cont_pos) + curr_bay.get_columns()
                self.bayListMain[cont][1].config(background="red")
            if cont_to_move not in prev_move_end_in_bay.get_offload_list():
                self.bufferList[end][1].config(background="green")
            self.bayListMain[init][1].config(background="blue")
        elif curr_move_end_in_bay and not prev_move_end_in_bay:
            if end_pos == (-1, 0):
                end = 0
            else:
                end = curr_bay.index_unmap(end_pos) + curr_bay.get_columns()
            if init_pos == (-1, 23):
                init = 23
            else:
                init = curr_buff.index_unmap(init_pos)
            if cont_pos is not None:
                cont = curr_buff.index_unmap(cont_pos) + curr_buff.get_columns()
                self.bufferList[cont][1].config(background="red")

            self.bufferList[init][1].config(background="blue")
            self.bayListMain[end][1].config(background="green")
        elif not curr_move_end_in_bay and not prev_move_end_in_bay:
            if end_pos == (-1, 23):
                end = 23
            else:
                end = curr_buff.index_unmap(end_pos) + curr_buff.get_columns()
            if init_pos == (-1, 23):
                init = 23
            else:
                init = curr_buff.index_unmap(init_pos)
            if cont_pos is not None:
                cont = curr_buff.index_unmap(cont_pos) + curr_buff.get_columns()
                self.bufferList[cont][1].config(background="red")

            self.bufferList[init][1].config(background="blue")
            self.bufferList[end][1].config(background="green")
        else:
            print("Error in animation")

        self.time_estimate = curr_cost
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
        self.buffer.convert_grid_to_stack()
        manifest_file.close()

    def download_manifest(self):
        if not self.task_complete:
            self.write_to_log("Task is not complete. Please complete the task before downloading the manifest.")
            return

        manifest_to_download = open(self.manifest.split(".")[0] + "OUTBOUND.txt", "w", encoding="ascii")
        manifest_to_read_from = open(self.manifest.split(".")[0] + "TEMP.txt", "r", encoding="ascii")

        manifest_lines = manifest_to_read_from.readlines()
        for line in manifest_lines[::-1]:
            manifest_to_download.write(line)

        self.write_to_log("Manifest has been downloaded. Please select a new manifest or task.")
        manifest_to_download.close()
        manifest_to_read_from.close()

    def update_manifest(self, bay):
        manifest = open(self.manifest.split(".")[0] + "TEMP.txt", "w", encoding="ascii")
        grid = bay.get_grid()
        for i in range(8):
            for j in range(12):
                cont = grid[i][j]
                if cont is not None:
                    manifest.write(cont.manifest_format(i, j))
                else:
                    manifest.write("[%02d, %02d], {%05d}, %s\n" % (8 - i, j + 1, 0, "UNUSED"))

    def display_buffer_grid(self):
        for row in range(4):
            for column in range(24):
                containerBox = tk.Label(self.middleLeftFrame, background="white", bd=4, relief="raised", width=4, height=2)
                containerBox.grid(row=row, column=column)
                containerName = tix.Balloon(self.middleLeftFrame, initwait=50)
                container = self.buffer.get_container(row, column)
                containerName.bind_widget(containerBox, balloonmsg=container.get_description() if container is not None else "")
                self.bufferList.append((containerName, containerBox))

    def display_bay_grid(self):
        for row in range(8):
            for column in range(12):
                container = self.ship_bay.get_container(row, column)
                containerBox = tk.Label(self.middleRightFrame, background="white", bd=4, relief="raised", width=4, height=2, text=container.get_description() if container is not None else "")
                containerBox.grid(row=row, column=column)
                containerName = tix.Balloon(self.middleRightFrame, initwait=50)
                containerName.bind_widget(containerBox, balloonmsg=container.get_description() if container is not None else "")
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

    def add_comment(self):
        self.write_to_log("%s commented: %s" % (self.user, self.commentEntry.get()))
