# SelfAssemblySim
Simplified 2D DNA nanoparticle self-assembly simulator

**Check out the "Example Parameters" section at the end of this page for help getting started!**

## Required Libraries
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

## Example Parameters
### Tips
One factor that limits the effectiveness of the 2D simulation is that for real NP assembly, the third dimension allows particles to be much more mobile. In the 2D simulation, particles can more easily become trapped in unfavorable positions. While this occurs in 3D assembly as well, it can be trickier to anneal the crystal structure in the 2D simulation because particles simply have fewer degrees of freedom. In complex systems, this often leads to small regions which have the predicted structure scattered within an amorphous region. Playing with variables such as temperature, bond stiffness, gravity, dissociation rate, cooldown, and the "allow bond rotation" button while the simulation is running can help tune the resulting structure.

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


## Future notes
If I work on this project again, I would want to add:
* Better joint management and more tuned friction / degrees of freedom
* Temp linked to dissociation chance
* Probabilistic association, not just dissociation
* Temperature/dissociation chance gradient across simulation box
* Seed crystals/facets

## Warnings
This was developed in a relatively short period of time, so some things like proper input verification for the particle group inputs were neglected. Invalid inputs here could crash the program. For the other inputs (which are updated live insted of on sim reset) there is basic input validation. If you find you can't type a specific number into a given input field, 
try a lower value, as some have upper limits to prevent crashes which are not clearly labeled in the menu yet.

## Acknowledgements
This project depends on the Pygame and PyBox2D python libraries, among others. All dependencies are used in accordance with their respective liscenses.

This project was inspired by [*Nanoparticle Superlattice Engineering with DNA*](https://doi.org/10.1126/science.1210493), by Robert Macfarlane et. al. I am not affiliated with the authors in any way.

