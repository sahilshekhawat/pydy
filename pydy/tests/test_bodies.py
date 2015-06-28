#!/usr/bin/env python
# -*- coding: utf-8 -*-

# external libraries
from sympy import Symbol
from sympy.physics.vector import Point, Dyadic
from sympy.physics.mechanics import ReferenceFrame

# local
from ..bodies import Body, Ground
from ..force import Force

class TestBody():
    def setup(self):
        self.body = Body('body')

    def test_body_init(self):
        assert self.body.name == 'body'
        assert self.body.parent is None
        assert self.body.child is None
        assert isinstance(self.body.masscenter, Point)
        assert isinstance(self.body.frame, ReferenceFrame)
        assert isinstance(self.body.mass, Symbol)
        assert len(self.body.inertia) == 2
        assert isinstance(self.body.inertia[0], Dyadic)
        assert isinstance(self.body.inertia[1], Point)

    def test_body_properties_value(self):
        name = self.body.name
        assert self.body.masscenter == Point(name + '_MassCenter')
        assert self.body.frame == ReferenceFrame(name + '_ReferenceFrame')
        assert self.body.mass == Symbol(name + '_Mass')

    def test_body_add_force(self):
        assert isinstance(self.body.force_list, list())
        assert len(self.body.force_list) == 0

        self.body.add_force(Force.GRAVITY)
        assert len(self.body.force_list) == 1
        assert self.body.force_list[0] == Force.GRAVITY


class TestGround():
    def setup(self):
        self.ground = Ground('ground')

    def test_ground_init(self):
        assert hasattr(self.ground, 'origin')
        assert self.ground.origin == Point(self.ground.name + '_Origin')
        assert self.ground.parent is None
