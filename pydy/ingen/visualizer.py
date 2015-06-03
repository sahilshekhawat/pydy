__all__ = []


class Visualizer(object):
    """
    Creates visualization of the system

    Attributes
    =========
    system: instance of MultiBodySystem
        Just pass an instance of MultiBodySystem and it will visualize
        it using pydy.viz

    Example
    =======

        >>> from pydy.ingen import MultiBodySystem, RigidBody
        >>> system = MultiBodySystem()
        >>> body = RigidBody()
        >>> viz = Visualizer(system)

    It will automatically start a server and open up the visualization.
    """
    def __init__(self, system):
        self._system = system
