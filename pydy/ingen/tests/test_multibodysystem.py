from ..multibodysystem import MultiBodySystem
from ..bodies import Ground


class TestMultiBodySystem():

    def setup(self):
        self.system = MultiBodySystem()

    def test_init(self):
        assert isinstance(self.system.ground, Ground)
