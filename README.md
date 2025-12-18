# SelfAssemblySim
Simplified 2D DNA nanoparticle self-assembly simulator

## Required libraries
pybox2d: "pip install box2d"
* condaforge source broken at time of writing, use pip package

pygame: "conda/pip install pygame"

## About This Project
This program was created as a learning tool to help students explore DNA nanoparticle self-assembly in a simplified 2D environment. The simulation demonstrates how complex crystal structures can spontenously arise from simple rules and conditions. The inspiration for this project was [this paper](https://doi.org/10.1126/science.1210493) by Robert Macfarlane et. al.

Since this project is a simplified 2D model for DNA NP self-assembly, the crystal structures we can observe are different from those seen in the paper. The simplifications also make this program unsuited for actual thermodynmic simulations of self-assembly.

### Particle types
In the simulation, we define particle groups with a radius, mass, and ability to interact with other particles. The radius variable represents the **hydrodynamic radius** of the DNA NP, that is, the sum of the inner core radius and DNA linker length. The different layers of the NP are not represented in this simulation.

The "interactions" variable represents which other groups of NPs a given group can interact with. This is a stand-in for the **nucleotide linker sequence** which connects NPs in the Macfarlane paper.

Each particle group has an integer ID, which is used to set the connections of each group. For example, if the "interactions" field of particle 0 is set to `0`, particles in group 0 are self-interacting. Multiple groups can be specified seperated by commas (without spaces), to create particles with more complex interactions.

### Interactions
When two particles collide, the program checks if their respective groups can interact. If so, a bond is formed between the two particles. At every timestep, we use a random number generator to determine if the bond should break, based on the dissociation rate provided in the menu, in units of % chance of dissociation per second. A 0 in this field means the bonds never dissociate, and the field is capped at 99 to prevent a math error in the equation which processes this value.

### Temperature


### Warnings
This was written quickly, so some things like proper input verification were neglected. If you find you can't type a specific number into a given input feild, 
try a lower value, as some have upper limits to prevent crashes which are not clearly labeled in the menu yet.

### Acknowledgements
This project depends on the Pygame and PyBox2D python libraries. All dependencies are used in accordance with their respective liscenses.
