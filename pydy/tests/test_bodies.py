#!/usr/bin/env python
# -*- coding: utf-8 -*-

# external libraries
from sympy import Symbol
from sympy.physics.vector import Point, Dyadic
from sympy.physics.mechanics import ReferenceFrame, Particle, RigidBody

# local
from ..bodies import Body, Ground
from ..force import Force

class TestBody():
    def setup(self):
        self.body = Body('Body')

    def test_body_init(self):
        # by default a rigidbody is created.
        assert self.body.name == 'Body'
        assert self.body.parent is None
        assert self.body.child is None
        assert isinstance(self.body.masscenter, Point)
        assert isinstance(self.body.frame,    ReferenceFrame)
        assert isinstance(self.body.mass, Symbol)
        assert len(self.body.inertia) == 2
        assert isinstance(self.body.inertia[0], Dyadic)
        assert isinstance(self.body.inertia[1], Point)
        assert isinstance(self.body.body, RigidBody)

    def test_body_properties_value(self):
        name = self.body.name
        assert self.body.masscenter == Point(name + ' MassCenter')
        assert self.body.frame == ReferenceFrame(name + ' ReferenceFrame')
        assert self.body.mass == Symbol(name + ' Mass')

    def test_body_particle(self):
        point = Point('point')
        mass = Symbol('mass')
        self.particle_body = Body(masscenter=point, mass=mass)
        assert isinstance(self.particle_body.body, Particle)
        assert self.particle_body.masscenter == point
        assert self.particle_body.mass == mass

    def test_body_particle_add_force(self):
        vector = Symbol('a') * self.particle_body.frame.x
        self.particle_body.add_force(vector)
        assert self.particle_body.force_list == [(self.particle_body.masscenter, vector)]

    def test_body_add_force(self):
        assert isinstance(self.body.force_list, list())
        assert len(self.body.force_list) == 0

        point = self.body.masscenter.locatenew('force_point', Symbol('l')*self.body.frame.x)
        force_tuple = (point, Symbol('Fa')*self.body.frame.z)
        self.body.add_force(force_tuple)
        assert len(self.body.force_list) == 1
        assert self.body.force_list[0] == [force_tuple]


class TestGround():
    def setup(self):
        self.ground = Ground('ground')

    def test_ground_init(self):
        assert hasattr(self.ground, 'origin')
        assert self.ground.origin == Point(self.ground.name + ' Origin')
        assert self.ground.parent is None
