# Setup Guide
This page will walk you through the steps to get the simulation up and running, and provide some suggestions for parameters to try out.

Currently, some basic knowledge of installing and running python packages and programs is recommended – this guide assumes you know what a command line is and already have python installed on your computer.

These instructions are primarily designed for a Unix command line such as those found on Linux or MacOS. They may not work in Command Prompt on a Windows system.

## Install Dependencies
Python packages:
- pygame
- pybox2d
This program was developed on Python 3.13.11, but any moderately recent python environment should work so long as all the dependencies install.

You can install the required packages with the following command:
`pip install box2d`
`pip install pygame`

If you use Anaconda to manage your python environments, note that as of Dec 2025, I was unable to install box2d from the condaforge channel, so I used pip instead. However, pygame may be installed via `conda install pygame` instead of pip if desired.

## Clone the Repository
Copy the files in this repository to your own computer, either with the download button on github or, if you have git on your computer, with the following command:

```
cd /path/to/your/directory/
git clone https://github.com/zachbernheimer/SelfAssemblySim.git
```


## Run the program
Navigate to the project dierectory:
`cd SelfAssemblySim`

Run the main.py program:
`python main.py`


## Example Parameters
Once you have the program running, here are some parameters you can try out!

### Self-complementary NPs
This is the default configuration of the simulation on startup. You can add multiple groups of self-interacting particles with different properties to see how they form different regions within the crystal. A system of identicle self-interacting particles will form a hexagonal crystal lattice as pictured below, which is the close-packed lattice for 2D particles.

![Failed to display image](https://github.com/zachbernheimer/SelfAssemblySim/blob/main/images/self-interacting.png)

### Binary NPs - equal radii
Getting this simulation to produce the expected crystal structure is tricky because – unlike the 3D system, which has only one expected lattice configuration (BCC) – this 2D system has several lattices which are essentially equivalent, rotated versions of the expected square lattice. Following the rule that NPs maximize the number of possible connections, in a 2D world of binary NPs each particle should have 4 connecteions and be arranged in an alternating grid. However, the same number of connections is also achieved by hexagonally packed layers of NPs with alternating types, which actually form an orthorhombic lattice. When an external driving force such as gravity is applied, the lattice where the spheres are close-packed becomes favored, but without gravity we see both structures throughout the simulation. The possiblility for mutliple equivalent lattices makes it difficult to judge the actual structure of the material.

I've found that with the settings in the following image, by letting the simulation run with bond rotation enabled for a minute or so and then disabling bond rotation, I am able to see the lattice more clearly. This is likely because bond rotation makes the particles more mobile, which allows them to form the maximum possible connections, but also allowing the lattice to squish and deform, meaning it is constantly transitioning from square to orthorhombic and back. Disabling bond rotation forces the particles to space themselves out further and maintain a consistent angle to each other, making the lattice more easily visible. 

![Failed to display image](https://github.com/zachbernheimer/SelfAssemblySim/blob/main/images/binary.png)

### Binary NPs - different radii
This system demonstrates the impact of radius ratio on the crystal structure of the system. For the equal radii system above, there were multiple stable lattice configurations, but in this version the size constraints lead to a single stable geometry, revealing the distinct crystal facets seen in the image below.
![Failed to display image](https://github.com/zachbernheimer/SelfAssemblySim/blob/main/images/binary%20two%20size.png)

