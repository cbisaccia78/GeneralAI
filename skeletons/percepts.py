from skeletons.things import Thing


class Percept:
    def __init__(self, sensors):
        self.observations = [{'name': sensor.name, 'state': sensor.state} for sensor in sensors]
