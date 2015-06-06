__all__ = ['Ground', 'RigidBody', 'Particle']

from sympy.physics.mechanics import ReferenceFrame, Point
import sympy.physics.mechanics as sympy_mechanics
from sympy import oo, Symbol


class Ground(object):
    """
    Root body with name 'ground'. It is added to MultiBodySystem by
    default. It can be accessed by:

        >>> from pydy.ingen import MultiBodySystem
        >>> system = MultiBodySystem()
        >>> ground = system.ground()

    It returns a RigidBody which is always the parent of the first
    body added to the system.
    """
    def __init__(self, system):
        self.name = 'ground'
        self.reference_frame = ReferenceFrame(self.name + 'frame')
        self.origin = Point('O')
        self.center_of_mass = self.origin
        self.origin.set_vel(self.reference_frame, 0)
        self.system = system
        self._mass = oo
        self.child = None


class Body(object):
    """Base class for RigidBody and Particle

    Attributes
    ==========
    name: string
        sets the name of the body which defines other things.
    point: Point
        its the center of mass of the body.
    """
    def __init__(self, name, system=None):
        self.name = name
        self.center_of_mass = Point(name + 'Point')
        self.mass = Symbol(self.name + 'Mass')
        self.reference_frame = ReferenceFrame(self.name + 'frame')
        self.system = system


class RigidBody(Body):
    """
    This can also be included in sympy.physics.mechanics.RigidBody itself
    The only difference is that here, it is necessary for every RigidBody
    to have a Reference Frame.

    Attributes
    =========
    name: string
        specifies the name of the rigidBody

    Example
    =======

        >>> from pydy.ingen import RigidBody
        >>> from sympy import Symbol
        >>> mass = Symbol('m')
        >>> center_of_mass = Point('com')
        >>> body = RigidBody()

    """
    def __init__(self, name):
        super(RigidBody, self).__init__(name)
        self.parent = None
        self.child = None
        self.inertia = None
        self.body = sympy_mechanics.RigidBody(self.name, self.center_of_mass,
                                              self.reference_frame, self.mass,
                                              self.inertia)


class Particle(Body):
    """
    Arguments
    =========
    name: String
        sets the name of the particle which is used
        to name several properties to the particle
    """
    def __init__(self, name):
        super(Particle, self).__init__(name)

    @property
    def body(self):
        return sympy_mechanics.Particle(self.name, self.center_of_mass,
                                        self.mass)

