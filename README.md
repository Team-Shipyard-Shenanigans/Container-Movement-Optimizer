# Container Movement Optimizer (CMO)
By Vahagn Tovmasian and Aditi Behera

## Project Description
The Container Movement Optimizer is our project for our Artificial Intelligence Capstone. The basic goal was to develop software that can calculate the optimal sequence of moves that minimizes the time spent moving containers when a container ship is at port. It is capable of finding the optimal sequence for a target set of containers to load and unload or to calculate the sequence of moves required to balance the ship such that the mass of the lighter side is greater than or equal to 90% of the mass of the heavier side.

## Technical Information
### Development Tools
The CMO was built using Python. Python was chosen due to our groups common knowledge of the language, with the hopes that it would reduce development overhead, even if it meant a cost towards performance.

We utilized the following orimary libraries/modules in order assist us with the project.

* [Tkinter](https://docs.python.org/3/library/tkinter.html#module-tkinter), natively packaged with Python, was used to implement the GUI.
* [PyTest](https://docs.pytest.org/en/7.2.x/), used for our unit testing suite.
* [PyInstaller](https://pyinstaller.org/en/stable/), used for building our executable and distributable files for release.

### Solution Calculation and Heuristics
The CMO relies on A* with heuristics to search the solution space of move sequences to find the sequence that minimizes the time spent. The heuristics used for loading and unloading search relies on the knowledge of which containers need to be moved, and how their current location in the ship bay and buffer impacts the minimum number of moves required to load or unload those containers. 

Let $W_l, W_r$ be defined as the sum of the waits of the containers of the left partition and right partition of the ship. A ship is considered balanced if the following inequality is true
```math
\frac{\min(W_l, W_r)}{\max(W_l,W_r)} >= 0.9 
```

The load/unload heuristic $L$ was defined as follows. Let $n$ be the number of containers we need to offload. Let $m$ be the number of containers we need to onload, and let $T(i)$ be the cost to transfer a container between the ship and buffer. 

```math
L = \sum_{i = 1}^{n} (M(i) + T(i)) + \sum_{j=1}^{n-m} T(j)
```

Where $M(i)$ is the recurrence relation that describes the sum of the the minimum cost to move all containers above a particular container $i$

The balance heuristic $B$ was defined similarly, however instead of $n$ being the number of containers we need to offload it would be the minimum number of containers we'd need to move to achieve balance. $T(i)$ is defined as the cost to transfer a container from one side of the ship to the other side.

```math
B = \sum_{i = 1}^{n} (M(i) + T(i))
```

## Complications
The primary complications that occurred during the development phase were during integration. 

The original goal of the software was to create a separate execution thread for the GUI and the main Runner so that execution would not be hampered by running it all synchronously. Due to lack of time and issues with lack of familiarity with multithreading in Pythonwe were not able to incorporate this functionality, so the Runner was fully incorporated into the GUI. 

After incorporation we encountered lots of small issueus in debugging the final product post integration, but ultimately resolved them.

## Acknowledgements

We would like to acknowledge our professor, Dr. Eamonn Keogh for all of the assistance and guidance he provided us in making this project come to fruition.
