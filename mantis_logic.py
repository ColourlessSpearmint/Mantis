"""
Mantis Rules
https://www.explodingkittens.com/pages/how-to-play-mantis

## Game Overview
- Players aim to be the first to collect 10+ cards in their Score Pile
- 2-4 Players
- Game uses 60 cards (6 colour, 10 of each colour)
- Cards have two sides: white side (front) and peach side (back) with three different colours
- The colour on the front is always one of the three colours shown on the back
- The seven colours are: red, orange, yellow, green, blue, purple, pink

## Setup
- Shuffle the deck
- Deal 4 cards face up (white side) to each player's Tank (hand)
- Play proceeds clockwise

## Turn Structure
On your turn, choose ONE of these two actions:

1. **Try to Score**:
   - Take the top card from the Draw Pile
   - Flip it over in YOUR Tank
   - If the card colour matches any cards in your Tank:
     - Move ALL cards of that colour (including the new one) to your Score Pile
   - If no match:
     - Leave the card in your Tank

2. **Try to Steal**:
   - Take the top card from the Draw Pile
   - Flip it over in ANOTHER player's Tank
   - If the card colour matches any cards in their Tank:
     - Move ALL cards of that colour (including the new one) to YOUR Tank
   - If no match:
     - Leave the card in their Tank

## Winning
- First player with 10+ cards in their Score Pile wins
- If Draw Pile runs out, player with most cards in Score Pile wins
- If tied on Score Pile size, player with most cards in Tank wins
"""


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
DEFAULTGOAL = 10

class Mantis:
    def __init__(self):
        self.players = []
        self.deck = []
        self.goal = DEFAULTGOAL
        self.turns = 0

    def drawCard(self):
        """Returns and pops (REMOVES) the top card from the deck."""
        self.topCard = self.deck[-1]
        return self.deck.pop()

    def startGame(self):
        self.shuffleDeck()
        self.dealCards()

    def dealCards(self):
        for player in self.players:
            newTank = []
            for i in range(STARTINGTANKSIZE):
                newTank.append(self.drawCard())
            player.tank = newTank

    def shuffleDeck(self):
        newDeck = []
        for i in range(DECKSIZE):
            newDeck.append(self.Card())
        self.deck = newDeck
        self.topCard = self.deck[-1]

    def isValidName(self, name):
        for player in self.players:
            if player.name == name:
                return False
        return True


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
            if mantis.isValidName(name):
                self.name = name
            else:
                raise ValueError(f"Duplicate names are not allowed: \'{name}\'")
            self.tank = []
            self.score = []
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
