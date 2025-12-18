#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2D DNA Nanoparticle Self-assembly Simulation

@author: zach

This project makes use of (modified) code from various pybox2d example scripts in addition to 
the library itself, as permitted under the pybox2d zlib license.

"""

import pygame, random, math
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN, MOUSEBUTTONUP)

import Box2D  # The main library
# Box2D.b2 maps Box2D.b2Vec2 to vec2 (and so on)
from Box2D.b2 import (world, polygonShape, circleShape, staticBody, dynamicBody)

pygame.init()
from gui import GUI

# --- constants ---
# Box2D deals with meters, but we want to display pixels,
# so define a conversion factor:
PPM = 20.0  # pixels per meter
TARGET_FPS = 60
TIME_STEP = 1.0 / TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720


class ParticleGroup():
    def __init__(self, radius, mass, color, groupID, interactIDs=[], num=0):
        self.radius = radius
        self.mass = mass
        self.color = color
        self.groupID = groupID
        self.interactIDs = interactIDs
        self.num = num
        
    
    def can_join(a, b):
        return b.groupID in a.interactIDs



class Particle():
    def __init__(self, group, world, position, velocity=(0,0)):
        #position = tuple, velocity = tuple
        self.group = group
        
        self.body = world.CreateDynamicBody(position=position)
        self.body.CreateCircleFixture(radius=group.radius, density=1, friction=0.1, restitution=0.8)
        
        self.body.linearVelocity = velocity
        self.body.mass = group.mass
        self.body.linearDamping = 0.1
        self.body.angularDamping = 0
        
        self.body.userData = self
        self.body.enableSleep = False
        self.bonds = {}
        
        self.vmean = 0
        self.vspread = 1
        
        self.amean = 0
        self.aspread = 1
    
    def addBond(self, other, bond):
        self.bonds[other] = bond
    
    def removeBond(self, other):
        del self.bonds[other]
    
    def setRandomVel(self, vmean=None, vspread=None):
        self.vmean = vmean if vmean is not None else self.vmean
        self.vspread = vspread if vspread is not None else self.vspread
        
        v_abs = random.gauss(self.vmean, self.vspread)
        v_theta = random.random() * 2*math.pi
        
        vx = v_abs*math.cos(v_theta)
        vy = v_abs*math.sin(v_theta)
        self.body.linearVelocity=(vx,vy)
    
    def update(self, zeroV=False, amean=6, aspread=0):
        # apply a random force to the particle
        
        if zeroV:
            self.body.linearVelocity=(0,0)
        
        aspread = amean/10 if aspread == 0 else aspread
        
        f_abs = 0 if amean == 0 else random.gauss(amean, aspread)
        f_theta = random.random() * 2*math.pi
        
        fx = f_abs*math.cos(f_theta)
        fy = f_abs*math.sin(f_theta)
        
        self.body.ApplyForce((fx,fy), point=self.body.worldCenter, wake=True)
    
    def draw(self):
        for fixture in self.body.fixtures:
            shape = fixture.shape

            position = self.body.transform * shape.pos * PPM
            position = (position[0], SCREEN_HEIGHT - position[1])
            pygame.draw.circle(screen, self.group.color, [int(x) for x in position], int(shape.radius * PPM))

        
class Bond():
    bondList = []
    stiffness = 1
    anchorContact = False
    resetAll = False
    
    def __init__(self, pA, pB, point=None):
        self.members = {pA, pB}
        self.distJoint = None
        self.revJoint = None
        self.newbond = True
        self.cooldown = False
        self.point = point
        
        pA.addBond(pB, self)
        pB.addBond(pA, self)
        
        Bond.bondList.append(self)
    
    def makeJoint(self):
        pA, pB = list(self.members)
        style = "distance"
        if style == "distance":
            self.distJoint = world.CreateDistanceJoint(
                bodyA=pA.body,
                bodyB=pB.body,
                anchorA=self.point if Bond.anchorContact else pA.body.worldCenter,
                anchorB=self.point if Bond.anchorContact else pB.body.worldCenter,
                collideConnected = Bond.anchorContact or Bond.stiffness > 0,
                frequencyHz= Bond.stiffness,
                dampingRatio=1
                )
            if Bond.stiffness == 0:
                self.distJoint.enableSpring = False
                
        #style = "revolute"
        if style == "revolute":
            self.revJoint = world.CreateRevoluteJoint(
                bodyA=pA.body,
                bodyB=pB.body,
                anchor=pA.body.worldCenter,
                maxMotorTorque = 0.2,
                motorSpeed = 0.0,
                enableMotor = True,
                collideConnected=False)
        
    
    def getMembers(self):
        return self.members
    
    def update(self, dissocChance, cooldown):
        if not (self.cooldown or self.newbond):
            r = random.random()
            
            if self.distJoint is not None:
                force = self.distJoint.GetReactionForce(TARGET_FPS).lengthSquared
                
                if force > 100000:
                    #print(force)
                    pass
                
                # update stiffness
                self.distJoint.frequency = Bond.stiffness
                
                if Bond.stiffness == 0:
                    self.distJoint.enableSpring = False
                    #pass
                    
            if self.revJoint is not None:
                force = self.revJoint.GetReactionForce(TARGET_FPS)
                torque = self.revJoint.GetReactionTorque(TARGET_FPS)
                
                if force.lengthSquared > 100000:
                    print(force.lengthSquared)
                    r = 1 # dissociate the bond
                if torque > 1:
                    print("torque: " + torque)
            
            if r < dissocChance:
                if self.distJoint is not None:
                    world.DestroyJoint(self.distJoint)
                    self.distJoint = None
                if self.revJoint is not None:                    
                    world.DestroyJoint(self.revJoint)
                    self.revJoint = None
                self.cooldown = cooldown
                pA, pB = list(self.members)
                #pA.setRandomVel()
                
                pA.update(zeroV=True)
                pB.update(zeroV=True)
        else:
            self.cooldown -= 1
            if self.cooldown <= 0:
                pA, pB = list(self.members)
                pA.removeBond(pB)
                pB.removeBond(pA)
                Bond.bondList.remove(self)
                


class overlapQueryCallback(Box2D.b2QueryCallback):
    def __init__(self): 
        Box2D.b2QueryCallback.__init__(self)
        self.overlap = False

    def ReportFixture(self, fixture):
        self.overlap = True

        return False # stop the query

class particleContactListener(Box2D.b2ContactListener):
    def __init__(self):
        Box2D.b2ContactListener.__init__(self)
    def BeginContact(self, contact):
        fixtureA = contact.fixtureA
        bodyA = fixtureA.body
        particleA = bodyA.userData
        fixtureB = contact.fixtureB
        bodyB = fixtureB.body
        particleB = bodyB.userData
        
        if isinstance(particleA, Particle) and isinstance(particleB, Particle):            
            if ParticleGroup.can_join(particleA.group, particleB.group):
                if particleB not in particleA.bonds.keys():
                    Bond(particleA,particleB, contact.worldManifold.points[0])    
        
    def EndContact(self, contact):
        pass
    def PreSolve(self, contact, oldManifold):
        pass
    def PostSolve(self, contact, impulse):
        pass
    
# Extend Box2d shape with pygame drawing function
def draw_polygon(polygon, body, fixture):
    vertices = [(body.transform * v) * PPM for v in polygon.vertices]
    vertices = [(v[0], SCREEN_HEIGHT - v[1]) for v in vertices]
    pygame.draw.polygon(screen, "grey", vertices)
polygonShape.draw = draw_polygon


def makeParticles(group, box, world, vmean=1, vspread=0.25, particles=[], max_tries=50):
    """Create the specified number of particles within the specified box"""
    num = group.num
    n = 0
    for n in range(num):
        
        i=0
        while i < max_tries:     
            posx = Box2D.b2Random(*box[0])
            posy = Box2D.b2Random(*box[1])
            #print(posx, posy)
            # Make a box to test overlap.
            aabb = Box2D.b2AABB(lowerBound=(posx-group.radius, posy-group.radius), upperBound=(posx+group.radius, posy+group.radius))

            # Query the world for overlapping shapes.
            query = overlapQueryCallback()
            world.QueryAABB(query, aabb)
            

            if not query.overlap:
                p = Particle(group, world, (posx,posy))
                p.setRandomVel(vmean, vspread)
                particles.append(p)
                break
            
            i += 1
        if i == max_tries:
            print("Overlapping!")
            break
    print("{0} group {1} particles created".format(n+1, group.groupID))
    
    return particles


def resetSim(world, gui, groups, particles):
    Bond.bondList.clear()
    for p in particles:
        world.DestroyBody(p.body)
    
    particles.clear()
    groups.clear()
    
    inVars = gui.inputVars
    
    
    for k in inVars.keys():
        if k.startswith("group_"):
            
            groupData = inVars[k].getData()
            #print(groupData)
            # radius, mass, color, id, connections, number
            g = ParticleGroup(*groupData)
            groups.append(g)
            
            makeParticles(g, box, world, vmean=5, particles=particles)

    

# --- pygame setup ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('2D Self-Assembly simulator')
clock = pygame.time.Clock()

# --- pybox2d world setup ---
# Create the world
world = world(gravity=(0, 0), doSleep=True, contactListener=particleContactListener())


width = SCREEN_WIDTH/PPM
height = SCREEN_HEIGHT/PPM


# Add borders
floor = world.CreateStaticBody(
    position=(0, 0),
    shapes=polygonShape(box=(width, 1)),
    
)
ceiling = world.CreateStaticBody(
    position=(0, height),
    shapes=polygonShape(box=(width, 1)),
)
left_wall = world.CreateStaticBody(
    position=(0, 0),
    shapes=polygonShape(box=(1, height)),
)
right_wall = world.CreateStaticBody(
    position=(width, 0),
    shapes=polygonShape(box=(1, height)),
)

Box2D.b2Body.fixtures
static_bodies = [floor, left_wall, right_wall, ceiling]

for sb in static_bodies:
    sb.enableSleep = True
    sb.isAwake = False
    for f in sb.fixtures:
        f.friction = 0.5
        f.restitution = 0.8
    


## make groups - later do this from menu

np = [500,500]
groups = [
    ParticleGroup(0.4, 1, "blue", 0, [1], np[0]),
    ParticleGroup(0.25, 1, "orange", 1, [0], np[1]),
    ]

np = [400,400,200]
groups = [
    ParticleGroup(0.5, 1, "blue", 0, [0,1], np[0]),
    ParticleGroup(0.5, 1, "orange", 1, [0], np[1]),
    #ParticleGroup(0.7, 1, "green", 2, [2], np[1]),
    ]

groups = []
# Create particles
box = ((1,width-1),(1,height-1))

particles = []

for i in range(len(groups)):
    g = groups[i]
    makeParticles(g, box, world, vmean = 1, particles=particles)



dissociationRate = 25 # % of bonds which will dissociate each second
jointCooldown = 10 # timesteps to wait before allowing new joint with same particle
temp = 5.0

dissociationChance = 1-math.exp(math.log(1-dissociationRate/100)/TARGET_FPS) # convert from rate in dissociation probability per second to chance per timestep
#print(dissociationChance)

# --- main game loop ---
running = True
frames = 0
printInterval = 5 # seconds

def simResetCallback(value, button):
    resetSim(world, gui, groups, particles)


# --- GUI setup ---
gui = GUI(screen, simResetCallback, pos=(5,30))

resetSim(world,gui,groups,particles)

#fps = []

while running:
    # Check the event queue
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            # The user closed the window or pressed escape
            running = False
        elif event.type in (MOUSEBUTTONDOWN, MOUSEBUTTONUP):
            gui.handleClick(event)
        elif event.type == KEYDOWN:
            gui.handleKey(event)
    # update variables
    
    paused = gui.inputVars["paused"]
    
    if gui.inputVars["dissocRate"]:
        dissociationChance = 1-math.exp(math.log(1- float(gui.inputVars["dissocRate"])/100)/TARGET_FPS)
    if gui.inputVars["cooldown"]:
        jointCooldown = int(float(gui.inputVars["cooldown"])*60)
    if gui.inputVars["gravity"]:
        try:
            world.gravity = (float(gui.inputVars["gravity"]), 0)
        except:
            pass
    if gui.inputVars["temp"]:
        try:
            temp = float(gui.inputVars["temp"])
        except:
            pass
    if gui.inputVars["stiffness"]:
        try:
            Bond.stiffness = float(gui.inputVars["stiffness"])
        except:
            pass
    if Bond.anchorContact == gui.inputVars["allowRotation"]:
        Bond.anchorContact = not gui.inputVars["allowRotation"]
        Bond.resetAll = True

    # Run scheduled tasks
    if frames >= printInterval*TARGET_FPS:
        print("There are {} bonds".format(len(Bond.bondList)))
        #print(clock.get_fps())
        frames = 0
        
    #fps.append("{0},{1:.4f}\n".format(pygame.time.get_ticks(), clock.get_fps()))
    
    
    # Fill the background
    screen.fill(pygame.Color(0,0,0))
    
    # Update Bonds

        
    for b in Bond.bondList:
        if b.newbond:
            b.makeJoint()
            b.newbond = False
        elif Bond.resetAll and not b.cooldown:
            world.DestroyJoint(b.distJoint)
            b.makeJoint()
            
        Bond.resetAll = False
        b.update(dissociationChance, jointCooldown)
    
    # Draw the world
    
    # Draw static bodies (ground, ceiling, walls):
    for body in static_bodies:
        for fixture in body.fixtures:
            pass
            #fixture.shape.draw(body, fixture)
    
    # Draw particles
    for p in particles:
        p.update(amean=temp)
        p.draw()
    
    
    # Draw GUI on top of world
    gui.draw()
    #print(gui.inputVars["showMenu"])
    
    # Make Box2D simulate the physics of our world for one step.
    # Instruct the world to perform a single step of simulation.
    if not paused:
        world.Step(TIME_STEP, 10, 10)

    # Flip the screen and try to keep at the target FPS
    pygame.display.flip()
    clock.tick(TARGET_FPS)
    frames += 1
    
#logFile = open("log.csv", mode='w')
#logFile.writelines(fps)
pygame.quit()


