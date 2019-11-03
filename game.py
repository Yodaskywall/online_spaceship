class Game:
    def __init__(self):
        self.bullets = []
        self.spaceships = [None, None]
        self.connected = (False, False)

    def isready(self):
        return self.connected[0] and self.connected[1]