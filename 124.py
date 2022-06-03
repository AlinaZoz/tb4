class GameRPS:
    values = ["1", "2", "3", "4", "5", "6"]

    def __init__(self):
        self.computerChoice = self.__class__.getRandomChoice()

    def newGame(self):
        self.computerChoice = self.__class__.getRandomChoice()

    @classmethod
    def getRandomChoice(cls):
        lenValues = len(cls.values)
        import random
        rndInd = random.randint(0, lenValues - 1)
        return cls.values[rndInd]

    def playerChoice(self, player1Choice):
        winner = None

        code = player1Choice[0] + self.computerChoice[0]
        if player1Choice == self.computerChoice:
            winner = "Погиб!"

        else:
            winner = "Живой!"

        return f"{player1Choice} vs {self.computerChoice} = " + winner