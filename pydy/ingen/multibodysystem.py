from __future__ import print_function, division

__all__ = ['MultiBodySystem']

from bodies import Ground


class MultiBodySystem(object):
    """A wrapper around pydy.system

    It does not have any arguments. It just needs to be created once.

        >>> from pydy.ingen import MultiBodySystem
        >>> system = MultiBodySystem()

    Its function is to provide a common place for all the components to
    interact.
    """
    def __init__(self):
        self.q_ind = []
        self.u_ind = []
        self.kd = []
        self.force_list = []
        self.body_list = []
        self.ground = Ground()

    @property
    def q_ind(self):
        return self.q_ind

    @q_ind.setter
    def q_ind(self, q):
        self.q_ind.append(q)

    @property
    def u_ind(self):
        return self.u_ind

    @u_ind.setter
    def u_ind(self, u):
        self.u_ind.append(u)

    @property
    def kd(self):
        return self.kd

    @kd.setter
    def kd(self, equation):
        self.kd.append(equation)

    @property
    def force_list(self):
        return self.force_list

    @force_list.setter
    def force_list(self, force):
        self.force_list.append(force)

    @property
    def body_list(self):
        return self.body_list

    @body_list.setter
    def body_list(self, body):
        self.body_list.append(body)
