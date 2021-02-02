class Directive:
    """
        Following the brain-arm-bottle example, a particular directive is the voltage
        of the electrical impulse at the entry to the arm at a given unit of time.
    """
    def __init__(self):
        return


class Action:
    """
        To consider the definition of an action, the following example will be helpful:
            Imagine a system containing a brain, a body, and a water bottle.
             - The brain, for our purposes, is the implementation of the agent function. ie) it takes a percept sequence
                 (memory) and maps it to a given action (electrical/chemical impulse sent to the body)
             - The body is a collection of actuators, but this action only requires the arm actuator to be completed
             - The action is characterized by information within the electrical impulses sent to the arm sent over
                the duration of time the arm is grabbing the water bottle. Within this period of time, the act of
                'grabbing' can be further
                broken up into sub-actions, namely moving the arm, closing fingers to grip, and moving arm back. In
                this way the action can be defined as a time-based sequence of 'directives' which will be interpreted
                by the arm. The arm actuator is what 'brings to life' those directives within the environment.
                At a basic level then, the action should be a dict of {t1: d1, t2: d2, ..., tk: dk}
                where the ti's are time units and the di's are directives


    """
    def __init__(self):
        return

