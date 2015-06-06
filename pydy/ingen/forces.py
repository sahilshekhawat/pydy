from sympy import Symbol


class GravityForce(object):
    """
    Creates a gravity force

    Attributes
    ==========
    direction: Vector
        Defines the direction of the gravity force
    """
    def __init__(self, direction):
        self.direction = direction
        self.gravitational_constant = Symbol('g')
