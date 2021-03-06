class Action(object):
    """
        In the context of the brain-arm-bottle example:
             - The action is characterized by information within the electrical impulses sent to the arm over
                the duration of time the arm is grabbing the water bottle. Within this period of time, the act of
                'grabbing' can be further broken up into sub-actions, namely moving the arm, closing fingers to grip,
                and moving the arm back. In this way the action can be defined as a time-based sequence of 'directives'
                which will be interpreted by the arm.
    """

    def __repr__(self):
        return "'" + type(self).__name__ + "'"

    def __eq__(self, other):
        return repr(self) == other

    def __init__(self, name=None):
        self.name = name


class Left(Action):
    name = 'Left'

    def __str__(self):
        return 'Left'

    def __repr__(self):
        return str(self)

    def __init__(self, units=1):
        self.units = units

    def __copy__(self):
        return Left()


class Right(Action):
    name = 'Right'

    def __str__(self):
        return 'Right'

    def __repr__(self):
        return str(self)

    def __init__(self, units=1):
        self.units = units

    def __copy__(self):
        return Right()


class Up(Action):
    name = 'Up'

    def __str__(self):
        return 'Up'

    def __repr__(self):
        return str(self)

    def __init__(self, units=1):
        self.units = units

    def __copy__(self):
        return Up()


class Down(Action):
    name = 'Down'

    def __str__(self):
        return 'Down'

    def __repr__(self):
        return str(self)

    def __init__(self, units=1):
        self.units = units

    def __copy__(self):
        return Down()


class Suck(Action):
    name = 'Suck'

    def __str__(self):
        return 'Suck'

    def __repr__(self):
        return str(self)

    def __init__(self):
        pass

    def __copy__(self):
        return Suck()


class Bet(Action):
    name = 'Bet'

    def __str__(self):
        return 'Bet'

    def __repr__(self):
        return str(self)

    def __init__(self):
        pass

    def __copy__(self):
        return Bet()


class Call(Action):
    name = 'Call'

    def __str__(self):
        return 'Call'

    def __repr__(self):
        return str(self)

    def __init__(self):
        pass

    def __copy__(self):
        return Call()


class Fold(Action):
    name = 'Fold'

    def __str__(self):
        return 'Fold'

    def __repr__(self):
        return str(self)

    def __init__(self):
        pass

    def __copy__(self):
        return Fold()


class Raise(Action):
    name = 'Raise'

    def __str__(self):
        return 'Raise'

    def __repr__(self):
        return str(self)

    def __init__(self):
        pass

    def __copy__(self):
        return Raise()


class Rebuy(Action):
    name = 'Rebuy'

    def __str__(self):
        return 'Rebuy'

    def __repr__(self):
        return str(self)

    def __init__(self):
        pass

    def __copy__(self):
        return Rebuy()


class Addon(Action):
    name = 'Addon'

    def __str__(self):
        return 'Addon'

    def __repr__(self):
        return str(self)

    def __init__(self):
        pass

    def __copy__(self):
        return Addon()






