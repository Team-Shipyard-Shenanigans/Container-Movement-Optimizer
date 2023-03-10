import grid as Grid
import container as Container
import stack as Stack
import optimizer as Optimizer
import gui as GUI
import os
import time


class Runner:
    manifest = open()
    manifest_path = ""
    log_path = "".join(["C:/CMO/logs/KeoghLongBeach", time.localtime()[0], ".txt"])
    log = None
    gui = None
    optimizer = None
    user = None
    current_step = 0
    total_steps = 999
    selected_task = None

    ship_bay = None
    buffer = None

    offload_list = []
    onload_list = []
    state = None
    states = {1: "Init", 2: "Log In", 3: "Wait Manifest", 4: "Select Task", 5: "Loading", 6: "Balancing", 7: "Calculating", 8: "Animating", 9: "Update Manifest", 10: "Stopping", 11: "Resetting"}

    def __init__(self):
        # self.gui = GUI.GUI()
        self.log = open(self.log_path, "a")

    def init_optimizer(self):
        self.optimizer = Optimizer.Optimizer(self.ship_bay, self.buffer)

    def read_manifest(self):
        for line in self.manifest:
            line.replace("[", "").replace("]", "").replace("{", "").replace("}", "")
            data = line.split(",")
            location = (self.ship_bay.get_height() - int(data[0]) - 1, int(data[1]) - 1)
            cont = Container.Container(weight=int(data[2]), description=str(data[3]), on_ship=True)
            cont.move(location)
            self.ship_bay.add_container(cont)

    def load_manifest(self):
        # self.manifest = open(gui.getManifestPath(), "r")
        pass

    def update_manifest(self):
        # TODO add new manifest format function
        manifest = open("", "w")
        for i in self.ship_bay.get_grid():
            for j in i:
                manifest.write(j.manifest_format())

    def log_in(self):
        pass

    def task_selection(self):
        pass

    def calculate_loading(self):
        pass

    def calculate_balancing(self):
        pass

    def display_animation(self):
        pass

    def stop_runner(self):
        pass

    def tick(self):
        if self.states[self.state] == "Init":
            self.state = 2
        elif self.states[self.state] == "Log In":
            if self.gui.userChanged():
                self.user = self.gui.getUser()
                self.state = 3
        elif self.states[self.state] == "Wait Manifest":
            if self.gui.manifestSelected():
                self.load_manifest()
                self.state = 4
        elif self.states[self.state] == "Select Task":
            if self.gui.taskSelected():
                self.selected_task = self.gui.getTask()
                if self.selected_task is "Loading":
                    self.state = 5
                elif self.selected_task is "Balancing":
                    self.state = 6
        elif self.states[self.state] == "Loading":
            ##TODO NEED TRANSFER LIST INPUTS
            self.state = 7
        elif self.states[self.state] == "Balancing":
            self.state = 7
        elif self.states[self.state] == "Calculating":
            self.state = 8
        elif self.states[self.state] == "Animating":
            # TODO display to GUI
            pass
        elif self.states[self.state] == "Update Manifest":
            self.update_manifest()
            self.state = 11
        elif self.states[self.state] == "Resetting":
            if self.gui.confirmedManifestSent():
                self.state = 4

        if self.gui.userChanged():
            self.user = self.gui.getUser()
