from skeletons.properties import Shape, Size


class Thing:
    def __init__(self, name=None):
        self.name = name
        return


class Physical(Thing):
    def __init__(self, name=None, shape: Shape = None, size: Size = None):
        super(Physical, self).__init__(name)
        self.shape = shape
        self.size = size
        return


class Virtual(Thing):
    def __init__(self, name=None):
        super(Virtual, self).__init__(name)
        return


class D0Physical(Physical):
    def __init__(self, name=None, shape: Shape = None, size: Size = None):
        self.dim = 0
        return


class D1Physical(Physical):
    def __init__(self, name=None, shape: D1Shape = None, size: D1Size = None):
        self.dim = 1
        return


class D2Physical(Physical):
    def __init__(self, name=None, shape: D2Shape = None, size: D2Size = None):
        self.dim = 2
        return


class D3Physical(Physical):
    def __init__(self, name=None, shape: D3Shape = None, size: D3Size = None):
        self.dim = 3
        return


class PhysicalDirective(Physical):
    """
        Following the brain-arm-bottle example, a physical directive is the voltage
        of the electrical impulse at the entry to the arm at a given unit of time.
    """
    def __init__(self, name=None):
        return


class VirtualDirective(Virtual):
    """
        Needs expanding.
    """
    def __init__(self, name=None):
        return
