__all__ = ['Ground', 'Linear', 'Massless']

from sympy.physics.mechanics import ReferenceFrame, Point
from sympy import oo


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
    def __init__(self):
        self.name = 'ground'
        self.reference_frame = ReferenceFrame(self.name + 'frame')
        self.origin = Point('O')
        self.origin.set_vel(self.reference_frame, 0)
        self._mass = oo


class RigidBody(object):
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
        self.name = name
        self._reference_frame = ReferenceFrame(self.name + 'frame')
        self.parent = None
        self._child = None

    @property
    def parent(self):
        return self.parent

    @parent.setter
    def parent(self, parent):
        self.parent = parent

    @property
    def child(self):
        return self.child

    @child.setter
    def child(self, child):
        self.child = child
