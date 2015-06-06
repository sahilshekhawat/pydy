from sympy.physics.mechanics import *
from sympy import Symbol

__all__ = ['PinJoint']


class PinJoint(object):
    """TODO
    """
    def __init__(self, parent, parent_vector, child, child_vector, axis=None):
        self._joint_parent = parent
        self._joint_parent_vector = parent_vector
        self._joint_child = child
        self._joint_child_vector = child_vector
        self._rotation_vector = axis
        self._pin_point = None
        self.add_joint()

    def set_parent_child_relationship(self):
        """Sets the parent child relationship by setting the values of the
        parent and child attributes in the body.
        """
        self._joint_parent.child = self._joint_child
        self._joint_child.parent = self._joint_parent

    def locate_pin_point(self):
        self._pin_point = self._joint_parent.center_of_mass.locatenew(
            self._joint_parent.name + 'ToPinJoint',
            self._joint_parent_vector)

    def locate_child_center_of_mass(self):
        print "#############",self._joint_parent.center_of_mass.name
        self._joint_child.center_of_mass = self._joint_parent.center_of_mass.locatenew(
            'PinJointTo' + self._joint_child.name,
            self._joint_child_vector)

    def set_child_point_velocity(self):
        print self._joint_child.center_of_mass.name, self._joint_parent.reference_frame.name
        print self._joint_parent.center_of_mass.name
        self._joint_child.center_of_mass.v2pt_theory(
            self._joint_parent.center_of_mass,
            self._joint_parent.reference_frame,
            self._joint_child.reference_frame)

    def add_joint(self):
        if self._rotation_vector is None:
            # By default, pin joint binds z axis of both the bodies.
            self._rotation_vector = self._joint_parent.reference_frame.z
        self.set_parent_child_relationship()
        next_q = self._joint_parent.system.assignName.get_next_q()
        next_qd = dynamicsymbols(next_q, 1)
        next_q = dynamicsymbols(next_q)
        self._joint_child.reference_frame.orient(
            self._joint_parent.reference_frame,
            'Axis',
            [next_q, self._rotation_vector])
        self._joint_parent.system._q_ind.append(next_q)
        self._joint_parent.system._qd_ind.append(next_qd)

        self.locate_pin_point()
        self.locate_child_center_of_mass()
        self.set_child_point_velocity()

        next_u = dynamicsymbols(self._joint_parent.system.assignName.get_next_u())
        self.set_child_angular_velocity(
            next_u * self._joint_parent.reference_frame.z)
        self._joint_parent.system._u_ind.append(next_u)

        self._joint_parent.system._body_list.append(self._joint_child)

    def set_child_angular_velocity(self, vector):
        """Sets Angular velocity of the city w.r.t
        the parent.
        Attributes
        ==========
        vector: Vector
            defines the direction of the joint.
        """
        self._joint_child.reference_frame.set_ang_vel(
            self._joint_parent.reference_frame,
            vector)
        # update the velocity of child
        self.set_child_point_velocity()

    def include_child_in_system(self):
        self._joint_child = self._joint_parent.system
        self._joint_parent.system.assignName.increment_body()