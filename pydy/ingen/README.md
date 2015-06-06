###Introduction
pydy-ingen provides an interface to easily define system in terms of joints, bodies, forces and constraints.

###Example
This is a simple example for a one degree of freedom translational spring-mass-damper.

```
from pydy.ingen import *
from sympy import symbols

system = MultiBodySystem()
particle = Particle()
# Can directly link to pydy-viz using decorators
# self contained API to specify
# work on addDecoration.
# particle.addDecoration( Sphere(0.1) );
# Added pin joint between ground and particle
# which axes
# RigidBody can be replace with system.addBody()
# 1. vector to rotate
# 2. location of pin to parent
# 3. location of pin to child
# vector representing the axes of rotation should always be defined wtf to the parent body.
# 3 tuple with magnitudes w.r.t parent/ sympy vectors (error if reference frame )
# ground, vector (locate pin joint in ground frame), axis(), particle (rigidbody) , vector(in rigidbody's referenceframe) , axis (3 tuple w.r.t ground frame)
# point and two vectors
# particleJoint = Pin( system.ground,  particle )
# create a Spring of length c with spring constant k
# force needs a direction an a point
# two coms and two points where the joint is.
# need direction and the point (com by default)
# magnitude and direction, point
# sprint needs to know two points
# how to apply force???
particle.applyForce( SpringForce( system.ground.x ) )

# initialize visualization
viz = Visualize( system )

# Other details for passing initial conditions and  other animation
# related things will be added soon
```

1. make current classes work.
2. Does this API give easier picture of just including it with current classes.
a. Create example with few lines for each line explaining what they do.
b. Can we avoid having the redundant classes.
c. make this demo work.
d. write unit tests for the API specifically for this demo.
e. mail chris about struggling.
f. michael sherman is very fiendly guy. cc jim, jason, chris mail him. You designed simbody.
do you think your API design is we should mimic simbodies api design.
sd fast symbolic based dynamic engine based on kane's method and it had the ordered in dynamics algo to symbolic
generate the most efficient EoMs.
g. multiple bodies  a parent.
h.




```
from pydy.ingen import *
from sympy import Symbol
system = MultiBodySystem()
particle1 = Particle('par1')
pinJoint = PinJoint(system.ground, 0*system.reference_frame.x, par1, system.reference_frame.y*Symbol('l'))
pinJoint.add_joint()


```