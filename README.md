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

The Bond cooldown field controls how long after a bond breaks it must wait to reform. This doesn't prevent the particles from forming new bonds with other particles in the same viscinity.

Bonds are modeled as distance joints in Box2D, which have a fixed distance but free to rotate. If the "Allow bond rotation" button is active, the particles are connected from their respective centers, which means nothing prevents them from spinning around each other. When this button is off, the joint is instead made at the contact point, and the particles are allowed to collide with each other. This prevents rolling and rotation but leads to some weird collision behavior when the joint is stiff, and I would look for a better way to accomplish this in the future, perhaps through a combination of the two joints with collisions dissabled.

If the bond stiffness field is greater than zero, the joints are modeled as springs with the specified characteristic frequency. I recommend using a relatively high stiffness to start. This is meant to allow a degree of freedom in NP motion which would represent the bonding and debonding of dozens or hundreds of DNA linkers, as well as chain uncoiling and recoiling.

### Temperature
The "Temp analog" field is not actually representative of the system temperature. Instead, it sets the average magnitude of a force which is applied in a random direction to each particle at every timestep. This is a very rough approximation of brownian motion. The goal is to ensure the particels always have enough energy to move around if they aren't bonded.

Unlike in real life, this "temperature" DOES NOT EFFECT the rate of bond dissociation. If you want a system with high mobility, you must rais both the dissociation chance and the temperature independently. The bonds in this simulation are currently not impacted in any way by the force on them, and the dissociation is purely statistical. However, a simulation at a higher temperature means that when a bond is broken, the particles tend to move further away from each other. Temperature is also useful in creating space in the crystal network, especialy when using gravity, and can help reveal the structure of the network by making the particles sit further apart on average.

### Gravity
This lets you apply an acceleration to all the particles. This is very good for getting a dense hexagonal lattice, but can crush the less entropically stable lattices that don't align with regular sphere packings. 



## Future notes
I might not work on this again, but if I do, I would want to add:
* Better joint management and more tuned friction / degrees of freedom
* Temp linked to dissociation chance
* Probabilistic association, not just dissociation
* Temperature/dissociation chance gradient across simulation box
* Seed crystals/facets

## Warnings
This was written quickly, so some things like proper input verification were neglected. If you find you can't type a specific number into a given input feild, 
try a lower value, as some have upper limits to prevent crashes which are not clearly labeled in the menu yet.

## Acknowledgements
This project depends on the Pygame and PyBox2D python libraries. All dependencies are used in accordance with their respective liscenses.
