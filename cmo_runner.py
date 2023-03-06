import grid as Grid
import container as Container
import stack as Stack
import optimizer as Optimizer
import gui as GUI
import os


def main():
    manifestPath = os.path.join(os.path.expanduser("~"), "Desktop")
    logPath = None
    userName = None
    currentStep = 0
    totalSteps = 999
    selectedTask = None

    



    while(gui.closeWindow() is false):
