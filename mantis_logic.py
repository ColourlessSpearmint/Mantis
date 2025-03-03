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
        self.players = [self.Player()]
        self.deck = [self.Card()]
        self.topCard = self.Card()
        self.goal = 10
        self.turns = 0

        for i in range(DECKSIZE):
            self.deck.append(self.Card())

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
        def __init__(self, name="Player"):
            self.name = name
            self.tank = []
            self.score = []

    def addPlayer(self, playerName):
        newPlayer = self.Player(playerName)
        for i in range(STARTINGTANKSIZE):
            newPlayer.tank.append(self.drawCard())
        self.players.append(newPlayer)

    def drawCard(self):
        """Returns and pops (REMOVES) the top card from the deck."""
        return self.deck.pop()
        

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
