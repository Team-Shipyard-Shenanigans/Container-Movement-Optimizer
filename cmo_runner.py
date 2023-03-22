import grid as Grid
import container as Container
import stack as Stack
import optimizer as Optimizer
import gui
import os
import time


class Runner:
    states = {1: "Init", 2: "Log In", 3: "Wait Manifest", 4: "Select Task", 5: "Loading", 6: "Balancing", 7: "Calculating", 8: "Animating", 9: "Update Manifest", 10: "Stopping", 11: "Resetting"}

    def __init__(self):
        self.gui = gui.GUI()
        # self.log = open(self.log_path, "a")
        self.manifest = open()
        self.manifest_path = ""
        self.log_path = "".join(["C:/CMO/logs/KeoghLongBeach", time.localtime()[0], ".txt"])
        self.optimizer = None
        self.user = None
        self.current_step = 0
        self.total_steps = 999
        self.selected_task = None

        self.ship_bay = Grid.ShipBay()
        self.buffer = Grid.Buffer()

        self.offload_list = []
        self.onload_list = []
        self.bufferAnimation = []
        self.bayAnimation = []
        self.state = None

    def init_optimizer(self):
        self.optimizer = Optimizer.Optimizer(self.ship_bay, self.buffer)

    def read_manifest(self):
        for line in self.manifest:
            line = line.replace("[", "").replace("]", "").replace("{", "").replace("}", "")
            data = line.split(",")
            if str(data[3].strip()) != "UNUSED":
                row = self.ship_bay.get_height() - int(data[0])
                column = int(data[1]) - 1
                cont = Container.Container(weight=int(data[2].strip()), description=str(data[3].strip()), on_ship=True)
                self.ship_bay.add_container(cont, row, column)

    def load_manifest(self):
        self.manifest = open(self.gui.getManifestPath(), "r", encoding="ascii")

    def update_manifest(self):
        manifest = open(self.manifest, "w", encoding="ascii")
        for i in self.ship_bay.get_grid():
            for j in i:
                manifest.write(j.manifest_format())

    def log_in(self):
        self.user = self.gui.getUser()
        self.gui.setUserChanged(False)
        self.write_to_log("%s logged in." % (self.user))

    def display_animation(self):
        if self.gui.getStepCompleted():
            self.current_step += 1
            if self.current_step == self.total_steps:
                self.bufferAnimation = []
                self.bayAnimation = []
        self.gui.updateAnimation(self.bufferAnimation, self.bayAnimation)
        self.gui.updateCurrStep(self.current_step, self.total_steps)
        hours, minutes = self.calculateTime()
        self.gui.updateCurrTimeEstimate("%2dH %2dM" % (hours, minutes))
        self.write_to_log("Now displaying step %d, move %s from %s to %s." % (self.current_step, self.bayAnimation[self.current_step][0], self.bayAnimation[self.current_step][1][0], self.bayAnimation[self.current_step][1].peek()))

    def stop_runner(self):
        pass

    def calculateTime(self):
        hours = 0
        minutes = 0
        ## TODO calculate time based on remaining moves + buffer transition in minutes
        return hours, minutes

    def tick(self):
        if self.states[self.state] == "Init":
            self.state = 2
        elif self.states[self.state] == "Log In":
            if self.gui.userChanged():
                self.log_in()
                self.state = 3
        elif self.states[self.state] == "Wait Manifest":
            if self.gui.manifestSelected():
                self.load_manifest()
                self.write_to_log("Manifest %s has been selected. Parsing manifest..." % (self.manifest_path))
                self.read_manifest()
                self.write_to_log("Parsing manifest %s is complete." % (self.manifest_path))
                self.state = 4
        elif self.states[self.state] == "Select Task":
            if self.gui.taskSelected():
                self.selected_task = self.gui.getTask()
                if self.selected_task is "Loading":
                    self.state = 5
                elif self.selected_task is "Balancing":
                    self.state = 6
                else:
                    raise ValueError("Task must be either Loading or Balancing!")
            self.write_to_log("%s selected %s task" % (self.user, self.selected_task))

        elif self.states[self.state] == "Loading":
            if self.gui.transferListReady():
                self.offload_list, self.onload_list = self.gui.getTransferList()
                self.state = 7
            self.state = 5
        elif self.states[self.state] == "Balancing":
            self.state = 7
        elif self.states[self.state] == "Calculating":
            self.write_to_log("Beginning calculation for %s" % (self.selected_task))
            start = time.time()
            bayAnimation, bufferAnimation = self.optimizer.load(self.ship_bay, self.buffer, self.onload_list, self.offload_list) if self.selected_task == "Loading" else self.optimizer.balance(self.ship_bay)
            end = time.time()
            self.write_to_log("Calculation completed in %d" % (end - start))
            self.state = 8
        elif self.states[self.state] == "Animating":
            if self.current_step < self.total_steps:
                self.display_animation()
            else:
                self.write_to_log("%s task completed.")
                self.state = 9
        elif self.states[self.state] == "Update Manifest":
            self.write_to_log("Generating outbound manifest %sOUTBOUND.txt")
            self.update_manifest()
            self.state = 11
        elif self.states[self.state] == "Resetting":
            if self.gui.confirmedManifestSent():
                self.write_to_log("Manifest completed, awaiting next manifest.")
                self.state = 4

        if self.gui.userChanged():
            self.log_in()

    def write_to_log(self, string):
        log = open(self.log_path, "w", encoding="ascii")
        log.write("%s : %s" % (time.localtime()[0:5], string))
        log.close()
