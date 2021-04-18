from collections.abc import MutableMapping


class EnvHash:
    def __init__(self, location, time):
        self.location = location
        self.time = time

    def __eq__(self, other):
        return self.location == other.location

    def __hash__(self):
        return (self.location.__hash__, int(self.time)).__hash__()  # may need to write a custom class for time units that are not integers


class Percepts(object):
    """
    try to make agents state hashable by environment properties:
        ie) location and time indexing:   _percept_history = {(loc_1, 1) : percept_1, . . . , (loc_n, n) : percept_n}
    """
    def __init__(self, max_time=-1, max_loc=None):
        self.max_time = max_time
        self.max_loc = max_loc
        self.env_keys = []
        self._percept_history = {}

    def __iter__(self):
        """
        need to find a way to unhash the hashed (loc, time) tuple when u want to do for k in Percepts: print(k[0], k[1])
        :return:
        """
        return iter(self.env_keys)

    def __getitem__(self, key):
        return self._percept_history[EnvHash(location=key[0], time=key[1])]

    def __setitem__(self, key, value):
        loc = key[0]
        time = key[1]
        self.env_keys.append((loc, time))
        self._percept_history[EnvHash(location=loc, time=time)] = value

    def __delitem__(self, key):
        loc = key[0]
        time = key[1]
        self.env_keys.append((loc, time))
        self.pop(EnvHash(location=loc, time=time))

    def pop(self, key):
        return

    def hash_get(self, h):
        return self._percept_history[h]

    def hash_add(self, percept, h):
        self._percept_history[h] = percept
