import random

COLOURDICT = {
    "red": {"index": 1, "name": "red", "emoji": "🟥"},
    "orange": {"index": 2, "name": "orange", "emoji": "🟧"},
    "yellow": {"index": 3, "name": "yellow", "emoji": "🟨"},
    "green": {"index": 4, "name": "green", "emoji": "🟩"},
    "blue": {"index": 5, "name": "blue", "emoji": "🟦"},
    "purple": {"index": 6, "name": "purple", "emoji": "🟪"},
    "pink": {"index": 7, "name": "pink", "emoji": "🌸"},
}
NUMOFCOLOURS = len(COLOURDICT)
NUMOFPOSSIBLECOLOURS = 3
DECKSIZE = 105
STARTINGTANKSIZE = 4

class Mantis:
    def __init__(self):
        self.players = []
        self.deck = []
        self.goal = 10
        self.turns = 0

        for i in range(DECKSIZE):
            self.deck.append(self.Card())

        self.topCard = self.deck[-1]

    def drawCard(self):
        """Returns and pops (REMOVES) the top card from the deck."""
        self.topCard = self.deck[-1]
        return self.deck.pop()

    class Card:
        def __init__(self, colour="", possibleColours=[]):
            self.possibleColours = []
            self.colour = ""
            if possibleColours:
                for possibleColour in possibleColours:
                    assert validateColour(possibleColour)
                self.possibleColours = possibleColours
            else:
                self.assignRandomPossibleColours()
                if colour and colour not in self.possibleColours:
                    self.possibleColours[0] = colour

            if colour:
                assert validateColour(colour)
                self.colour = colour
            else:
                self.assignRandomColour()

        def assignRandomPossibleColours(self):
            self.possibleColours = convertColourListToNames(random.sample(range(1, NUMOFCOLOURS+1), NUMOFPOSSIBLECOLOURS))

        def assignRandomColour(self):
            self.colour = self.possibleColours[random.randint(1,NUMOFPOSSIBLECOLOURS)-1]

    class Player:
        def __init__(self, mantis, name="Player"):
            self.game = mantis
            for player in self.game.players:
                assert player.name != name
            self.name = name
            self.tank = []
            self.score = []
            for i in range(STARTINGTANKSIZE):
                self.tank.append(self.game.drawCard())
            self.brain = self.Brain(self)

        def action(self, target):
            topCard = self.game.drawCard()
            if self.name == target.name:
                for card in self.tank:
                    if card.colour == topCard.colour:
                        self.tank.append(topCard)
                        self.scoreColour(topCard.colour)
                        return
                self.tank.append(topCard)
                return
            else:
                for card in target.tank:
                    if card.colour == topCard.colour:
                        target.tank.append(topCard)
                        self.stealColour(target, topCard.colour)
                        return
                target.tank.append(topCard)
                return
        
        def stealColour(self, target, colour):
            assert validateColour(colour)
            for card in target.tank:
                if card.colour == colour:
                    self.tank.append(card)
                    target.tank.remove(card)

        def scoreColour(self, colour):
            assert validateColour(colour)
            for card in self.tank:
                if card.colour == colour:
                    self.score.append(card)
                    self.tank.remove(card)

        class Brain:
            def __init__(self, player):
                self.player = player


def convertColourIndexToName(colourIndex: int) -> str:
    for colour in COLOURDICT.values():
        if colour["index"] == colourIndex:
            return colour["name"]
    raise LookupError(f"Invalid colourIndex: \'{colourIndex}\'") 

def convertColourListToNames(colourIndexList: list) -> list:
    colourNameList = []
    for colourindex in colourIndexList:
        colourNameList.append(convertColourIndexToName(colourindex))
    return colourNameList

def validateColour(colour=""):
    return colour.lower() in COLOURDICT

if __name__ == "__main__":
    game = Mantis()
    game.players.append(game.Player(game, "Player1"))
    game.players.append(game.Player(game, "Player2"))
    game.players.append(game.Player(game, "Player3"))

    print(game.topCard.possibleColours)
    for card in game.players[0].tank:
        print(card.possibleColours)
    print()
    for card in game.players[1].tank:
        print(card.possibleColours)

    game.players[0].action(game.players[1])

    print()
    print(game.topCard.possibleColours)
    for card in game.players[0].tank:
        print(card.possibleColours)
    print()
    for card in game.players[1].tank:
        print(card.possibleColours)
