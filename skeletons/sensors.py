class Sensor:
    def __init__(self, name, default=None):
        self.state = default
        self.name = name

    def sense(self):
        # move current input out and bring new input in
        return
