class Action:
    """
        In the context of the brain-arm-bottle example:
             - The action is characterized by information within the electrical impulses sent to the arm over
                the duration of time the arm is grabbing the water bottle. Within this period of time, the act of
                'grabbing' can be further broken up into sub-actions, namely moving the arm, closing fingers to grip,
                and moving the arm back. In this way the action can be defined as a time-based sequence of 'directives'
                which will be interpreted by the arm.
    """
    def __init__(self):
        return

    def __repr__(self):
        return self.__class__.__name__

    def __eq__(self, other):
        return repr(self) == repr(other)


class Left(Action):
    def __init__(self, units):
        self.units = units
        return

    def __repr__(self):
        return "Left"


class Right(Action):
    def __init__(self, units):
        self.units = units
        return

    def __repr__(self):
        return "Right"


class Up(Action):
    def __init__(self, units):
        self.units = units
        return

    def __repr__(self):
        return "Up"


class Down(Action):
    def __init__(self, units):
        self.units = units
        return

    def __repr__(self):
        return "Down"
