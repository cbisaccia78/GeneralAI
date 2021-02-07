class State:
    """
    a state should be relevant to a problem, as to not blow up the memory of the program by including
    extraneous information. for example, if the state is instantiated with a DriveToLocation problem,
    it will include info relevant to driving, but it wont include the current stock price of google.
    In this way the state is a subset or subclass of the current environment.
    """
    def __init__(self, problem):
        return
