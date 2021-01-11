class Sensor:
    def __init__(self, name=None, default=None):
        self.state = default
        self.name = name

    def sense(self, *args):
        # move current input out and bring new input in
        return


class VacuumSensor(Sensor):

    def sense(self, grid, grid_loc):
        # detect dir
        return



