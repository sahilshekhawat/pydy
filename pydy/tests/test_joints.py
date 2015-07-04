from sympy import Symbol, acos
from sympy.physics.vector import Point, dot, cross
from sympy.physics.mechanics import dynamicsymbols

from ..bodies import Body
from ..joints import Joint, PinJoint


class TestJoints():
    def setup(self):
        self.parent = Body('parent')
        self.child = Body('child')
        self.joint = Joint('joint', self.parent, self.parent.frame.x, self.child, 0)

    def test_joint_init(self):
        assert self.joint.name == 'joint'
        assert self.joint.child == self.child
        assert self.joint.parent == self.parent
        assert self.joint.parent_joint_vector == self.parent.frame.x
        assert self.joint.child_joint_vector == 0

    def test_joint_set_parent_child_rel(self):
        self.joint.set_parent_child_rel()
        assert self.child.parent == self.parent
        assert self.parent.child == self.child

    def test_joint_locate_joint_point(self):
        self.joint._locate_joint_point()
        assert hasattr(self.joint, 'joint_point')

        joint_point = self.parent.masscenter.locatenew(self.name + '_Point',
                                                       self.joint.parent_joint_vector)
        assert self.joint_point.name == joint_point

        child_masscenter = Point(self.child.name + '_MassCenter')
        child_masscenter.set_pos(joint_point, self.joint.child_joint_vector)
        assert self.child.masscenter == child_masscenter

    def test_joint_set_child_vel(self):
        # Note: this numeric and symbolic value implementation can be applied anywhere in joints
        # wherever symbol is used e.g. in set_joint_point_vel()

        # 1. numeric value
        self.joint.set_child_vel(10 * self.parent.frame.x)
        assert self.child.masscenter.vel(self.parent.frame) == 10 * self.parent.frame.x

        # 2. symbolic value
        v1 = dynamicsymbols('v1')
        self.joint.set_child_vel(v1 * self.parent.frame.x)
        assert self.child.masscenter.vel(self.parent.frame) == v1 * self.parent.frame.x

    def test_joint_set_joint_point_vel(self):
        v2 = dynamicsymbols('v2')
        self.joint.set_joint_point_vel(v2 * self.parent.frame.x)
        assert self.joint.joint_point.vel(self.parent.frame) == v2 * self.parennt.frame.x

    def test_joint_set_child_angular_velocity(self):
        v3 = dynamicsymbols('v3')
        self.joint.set_child_angular_vel(v3 * self.parent.frame.z)
        assert self.child.frame.ang_vel_in(self.parent.frame) == v3 * self.parent.frame.z

    def test_joint_orient_child(self):
        q1 = Symbol('q1')
        self.joint.orient_child('Axis', [q1, self.parent.frame.x])

        # TODO other similar frame.orient() tests can be done.
        # leaving more tests to discuss its necessity with others.


class TestPinJoint():
    def setup(self):
        self.parent = Body('parent')
        self.child = Body('child')
        self.pinjoint = PinJoint('pinjoint', self.parent, self.child)

    def test_pinjoint_init(self):
        # default values
        assert self.pinjoint.axis1 == self.parent.frame.x
        assert self.pinjoint.axis2 == self.child.frame.x
        assert self.pinjoint.parent_joint_point == self.parent.masscenter
        assert self.pinjoint.child_joint_point == self.child.masscenter
        assert self.pinjoint.parent_joint_vector == self.parent.frame.x
        assert self.pinjoint.child_joint_vector == self.child.frame.x

        assert self.parent_joint_point.vel(self.parent.frame) == 0
        assert self.child_joint_point.vel(self.child.frame) == 0

    def test_pinjoint_parameters(self):
        self.pinjoint = PinJoint('pinjoint', self.parent, self.child,
                                 (1, 0, 0), (0, 1, 0), axis1='x', axis2='y')
        assert self.pinjoint.axis1 == self.parent.frame.z
        assert self.pinjoint.axis2 == self.child.frame.y
        point1 = self.parent.masscenter.locatenew(self.parent.frame, self.parent.frame.z)
        point2 = self.child.masscenter.locatenew(self.child.frame, self.child.frame.y)
        assert self.pinjoint.parent_joint_point == point1
        assert self.pinjoint.child_joint_piont == point2
        assert self.pinjoint.parent_joint_vector == self.parent.frame.z
        assert self.pinjoint.child_joint_vector == self.chidl.frame.y

    def test_joint_joint_functions(self):

        # part 1 assining parent-child relationship
        self.pinjoint.set_parent_child_rel()
        assert self.child.parent == self.parent
        assert self.parent.child == self.child

        # part 2 locating joint point in bodies
        self.pinjoint._locate_joint_point()
        child_masscenter = self.child.masscenter
        parent_masscenter = self.parent.masscenter
        parent_joint_point = parent_masscenter.locatenew(self.name + '_Point', self.parent_joint_vector)
        child_joint_point = child_masscenter.locatenew(self.name + '_Point', self.child_joint_vector)
        assert self.pinjoint.parent_joint_vector == parent_joint_point
        assert self.pinjoint.child_joint_vector == child_joint_point

        # part 3 aligning axis1 and axis2
        self.join_frames()
        # sample implementation
        # self.child.frame.orient(self.parent.frame, 'Axis', [0, self.parent.frame.x])
        assert cross(self.pinjoint.axis1, self.pinjoint.axis2) == self.child.frame.z
        assert cross(self.pinjoint.axis2, self.pinjoint.axis1) == - self.parent.frame.z
        self.align_axes()
        axis1 = self.pinjoint.axis1
        axis2 = self.pinjoint.axis2
        # sample implementation
        # perpendicular_axis_in_parent = - cross(axis1, axis2)
        # angle_between_axes = acos(dot(self.pinjoint.axis2, self.pinjoint.axis1))
        # self.child.frame.orient(self.parent.frame, 'Axis',
        #                        [acos(dot(axis1, axis2)/(axis1.magnitude() * axis2.magnitude())),
        #                         cross(axis1, axis2)])
        assert acos(dot(axis1, axis2)/(axis1.magnitude() * axis2.magnitude())) == 0

        # part 4 adding angular velocity to child w.r.t parent
        assert self.child.frame.ang_vel_in(self.parent.frame) != 0

    def test_joint_apply_joint(self):
        # apply_joint() should do everything done above by calling specific funtions
        self.new_pinjoint = PinJoint('pinjoint', self.parent, self.child)
        self.new_pinjoint._apply_joint()
        # part 1
        assert self.child.parent == self.parent
        assert self.parent.child == self.child

        # part 2
        child_masscenter = self.child.masscenter
        parent_masscenter = self.parent.masscenter
        parent_joint_point = parent_masscenter.locatenew(self.name + '_Point', self.parent_joint_vector)
        child_joint_point = child_masscenter.locatenew(self.name + '_Point', self.child_joint_vector)
        assert self.pinjoint.parent_joint_vector == parent_joint_point
        assert self.pinjoint.child_joint_vector == child_joint_point

        # part 4
        axis1 = self.pinjoint.axis1
        axis2 = self.pinjoint.axis2
        assert acos(dot(axis1, axis2)/(axis1.magnitude() * axis2.magnitude())) == 0
