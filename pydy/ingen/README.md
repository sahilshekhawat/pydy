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
particle.addDecoration( Sphere(0.1) );
# Added pin joint between ground and particle
particleJoint = Pin( system.ground,  particle )
# creats a Spring of length c with spring constant k
particle.applyForce( SpringForce( system.ground.x ) )
# initialize visualization
viz = Visualize( system )

# Other details for passing initial conditions and  other animation
# related things will be added soon
```
