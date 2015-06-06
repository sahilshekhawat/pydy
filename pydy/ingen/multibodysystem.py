from __future__ import print_function, division

__all__ = ['MultiBodySystem']

from bodies import Ground, Body
from utils import AssignName
from sympy import Symbol
from sympy.physics.mechanics import KanesMethod


class MultiBodySystem(object):
    """A wrapper around pydy.system

    It does not have any arguments. It just needs to be created once.

        >>> from pydy.ingen import MultiBodySystem
        >>> system = MultiBodySystem()

    Its function is to provide a common place for all the components to
    interact and when the system has been defined by the user, to
    generate EoMs.
    """
    def __init__(self):
        self._q_ind = []
        self._qd_ind = []
        self._u_ind = []
        self._kd = []
        self._force_list = []
        self._body_list = []
        self._sympy_bodies = []
        self.ground = Ground(self)
        self.assignName = AssignName()
        self.reference_frame = self.ground.reference_frame
        self.origin = self.ground.origin
        self.gravity = None
        self.gravitational_constant = None
        self.kanes = None

    def generate_body_tree(self):
        """
        Generates body list based on the parent-child relationship between bodies.
        """
        if self.ground:
            self._body_list.append(self.ground)
        next_child = self.ground.child
        while next_child:
            self._body_list.append(next_child.body)
            next_child = next_child.child

    def set_gravity(self, direction):
        """Sets gravity system wide.

        Attributes
        ==========
        direction: Vector
            sets the direction of the gravity
        """
        self.gravitational_constant = Symbol('g')
        self.gravity = self.gravitational_constant * direction

    def add_gravity_force(self, direction):
        """iterates over all bodies and adds gravity force for all of them
        to the force list
        """
        self.set_gravity(direction)
        for i in self._body_list:
            self._force_list.append((i.center_of_mass, i.mass * self.gravity))

    def get_eoms(self):
        for i in range(len(self._qd_ind)):
            self._kd.append(self._qd_ind[i] - self._u_ind[i])
        for i in self._body_list:
            self._sympy_bodies.append(i.body)
        self.kanes = KanesMethod(self.reference_frame, q_ind=self._q_ind,
                            u_ind=self._u_ind, kd_eqs=self._kd)
        self.kanes.kanes_equations(self._force_list, self._sympy_bodies)
