class Game:
    def __init__(self, gameId):
        self.bullets = []
        self.id = gameId
        self.spaceships = [None, None]
        self.connected = [False, False]
        self.lost = [False, False]

    def isready(self):
        return self.connected[0] and self.connected[1]

    def finished(self):
        return self.lost[0] or self.lost[1]
