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

    def isValidName(self, name):
        for player in self.players:
            if player.name == name:
                return False
        return True

    class Card:
        def __init__(self):
            self.possibleColours = []
            self.assignRandomPossibleColours()
            self.assignRandomColour()

        def assignRandomPossibleColours(self):
            self.possibleColours = convertColourListToNames(random.sample(range(1, NUMOFCOLOURS+1), NUMOFPOSSIBLECOLOURS))

        def assignRandomColour(self):
            self.colour = self.possibleColours[random.randint(1,NUMOFPOSSIBLECOLOURS)-1]

    class Player:
        def __init__(self, game, brain, name):
            self.game = game
            if game.isValidName(name):
                self.name = name
            else:
                raise ValueError(f"Duplicate names are not allowed: \'{name}\'")
            self.tank = []
            self.scorePile = []
            self.brain = brain
        
        def getMatchingColours(self, colour):
            assert validateColour(colour)
            matchingCards = []
            for card in self.tank:
                if colour == card.colour:
                    matchingCards.append(card)
            return matchingCards

        def takeTurn(self):
            target = self.brain.run()
            self.action(target)

        def action(self, target):
            if target.name == self.name:
                self.stealAction()
            else:
                self.scoreAction()

        def stealAction(self, target):
            card = self.game.drawCard()
            if target.getMatchingColours(card.colour):
                target.tank.append(card)
                target.moveColours(card.colour, self.tank)
            else:
                target.tank.append(card)

        def scoreAction(self):
            card = self.game.drawCard()
            if self.getMatchingColours(card.colour):
                self.tank.append(card)
                self.moveColours(card.colour, self.scorePile)
            else:
                self.tank.append(card)
        
        def moveColours(self, colour, target:list):
            for card in self.getMatchingColours(colour):
                self.tank.remove(card)
                target.append(card)

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

