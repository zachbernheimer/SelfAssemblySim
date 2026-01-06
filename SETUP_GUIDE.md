# Getting Started
This page will walk you through the steps to get the simulation up and running, and provide some suggestions for parameters to try out.

Some basic knowledge of installing and running python packages and programs is recommended – this guide assumes you know what a command line is and already have python installed on your computer. This program was developed on Python 3.13.11, but any moderately recent version should work so long as all the dependencies install.

## Create the Environment
I recommend creating a virtual environment with venv (built in for python version ≥ 3.3) to keep this project from interfering with your other python environments. If you use Anaconda to manage your python environments, note that as of Dec 2025, I was unable to install box2d from the condaforge channel, so I used pip instead. Due to this issue, I do not suggest using Anaconda in this instance.

Open the terminal or command prompt. On Windows, you may need to select "run as administrator" to complete the setup.

Create and navigate to the folder where you will store the project, then create and activate the virtual environment.

### On Unix/macOS:
```
mkdir /path/to/project/directory    # create the project directory
cd /path/to/project/directiory      # enter the project directory
python -m venv simenv               # create the virtual environment
source ./simenv/bin/activate        # activate the environment
```

### On Windows:
```
mkdir "C:\\path\to\project\directory"   # create the project directory
cd "C:\\path\to\project\directiory"     # enter the project directory
py -m venv simenv                       # create the virtual environment
./simenv/bin/activate                   # activate the environment
```

You can deactivate the virtual environment with the command `deactivate`. Remember to reactivate it the next time you want to use the simulation!

## Install Dependencies
Required packages:
- [pygame](https://www.pygame.org/wiki/about)
- [Box2D](https://github.com/pybox2d/pybox2d)

You can install the required packages with the following command:
```
python -m pip install pygame box2d
```
On Windows, replace `python` with `py`

## Download the Project
In the upper right-hand corner of the [repository home page](https://github.com/zachbernheimer/SelfAssemblySim), select the green "Code" button, then select "Download ZIP". Move the downloaded file into your project directory, then unzip the file. You can rename the new folder "SelfAssemblySim-main" to "SelfAssemblySim" or adapt future `cd` commands to reflect the actual directory name.

If you have git on your computer, you can instead clone the repository with the following command:
```
git clone https://github.com/zachbernheimer/SelfAssemblySim.git
```

## Run the program
Navigate to the source directory and run `main.py`

### On Unix/macOS:
```
cd SelfAssemblySim/sim
python main.py
```

### On Windows:
```
cd SelfAssemblySim\sim
py main.py
```

## Example Parameters
Once you have the program running, here are some parameters you can try out!

### Self-complementary NPs
This is the default configuration of the simulation on startup. You can add multiple groups of self-interacting particles with different properties to see how they form different regions within the crystal. A system of identicle self-interacting particles will form a hexagonal crystal lattice as pictured below, which is the close-packed lattice for 2D particles.

![Blue circles cluster into a hexagonal lattice.](https://github.com/zachbernheimer/SelfAssemblySim/blob/main/images/self-interacting.png)

### Binary NPs - equal radii
Getting this simulation to produce the expected crystal structure is tricky because – unlike the 3D system, which has only one expected lattice configuration (BCC) – this 2D system has several lattices which are essentially equivalent, rotated versions of the expected square lattice. Following the rule that NPs maximize the number of possible connections, in a 2D world of binary NPs each particle should have 4 connecteions and be arranged in an alternating grid. However, the same number of connections is also achieved by hexagonally packed layers of NPs with alternating types, which actually form an orthorhombic lattice. When an external driving force such as gravity is applied, the lattice where the spheres are close-packed becomes favored, but without gravity we see both structures throughout the simulation. The possiblility for mutliple equivalent lattices makes it difficult to judge the actual structure of the material.

I've found that with the settings in the following image, by letting the simulation run with bond rotation enabled for a minute or so and then disabling bond rotation, I am able to see the lattice more clearly. This is likely because bond rotation makes the particles more mobile, which allows them to form the maximum possible connections, but also allowing the lattice to squish and deform, meaning it is constantly transitioning from square to orthorhombic and back. Disabling bond rotation forces the particles to space themselves out further and maintain a consistent angle to each other, making the lattice more easily visible. 

![Equal-sized blue and purple circles form an alternating checkerboard pattern which is not uniform across the image. There are many gaps and misaligned regions.](https://github.com/zachbernheimer/SelfAssemblySim/blob/main/images/binary.png)

### Binary NPs - different radii
This system demonstrates the impact of radius ratio on the crystal structure of the system. For the equal radii system above, there were multiple stable lattice configurations, but in this version the size constraints lead to a single stable geometry, revealing the distinct crystal facets seen in the image below.

![Small blue circles fill gaps between larger purple circles, creating several regions of well-defined square grids of purple circles. There are distinct regions with defects at the boundaries between them.](https://github.com/zachbernheimer/SelfAssemblySim/blob/main/images/binary%20two%20size.png)

## Closing Out
To exit the program, close the window or press the escape key. Once you are done running the simulation, exit the virtual environment with the command `deactivate`.

## Learn More
For more detailed discussion of the interface, simulation, and the theory behind it, check out the [README file](https://github.com/zachbernheimer/SelfAssemblySim) on the homepage of the repository.
