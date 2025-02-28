import random
from flask import Flask, render_template

class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __str__(self):
        return f"{self.color} {self.value}"

class Deck:
    def __init__(self):
        self.cards = []
        colors = ["red", "blue", "green", "yellow"]
        values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip", "Reverse", "+2"]
        for color in colors:
            for value in values:
                self.cards.append(Card(color, value))
            #add action cards
            self.cards.append(Card(color,"Skip"))
            self.cards.append(Card(color,"Reverse"))
            self.cards.append(Card(color,"+2"))

        # Add wild cards
        for i in range(4):
            self.cards.append(Card("wild", "Wild"))
            self.cards.append(Card("wild", "+4"))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num_cards):
        dealt_cards = []
        for _ in range(num_cards):
            if self.cards:
                dealt_cards.append(self.cards.pop())
            else:
                break  # Handle empty deck
        return dealt_cards

class Game:
    def __init__(self, num_players=1):
        self.num_players = num_players
        self.deck = Deck()
        self.deck.shuffle()
        self.discard_pile = []
        self.players = []
        self.current_player = 0

        # Initialize players and deal cards
        for i in range(num_players):
            self.players.append(self.deck.deal(7))

        #Start discard pile
        self.discard_pile.append(self.deck.deal(1)[0])


    def play_card(self, card):
        if card in self.players[self.current_player]:
            self.players[self.current_player].remove(card)
            self.discard_pile.append(card)
            self.current_player = (self.current_player + 1) % self.num_players
            # Add logic to check for win condition, draw cards etc.

    def draw_card(self):
        if self.deck:
            card = self.deck.deal(1)[0]
            self.players[self.current_player].append(card)

app = Flask(__name__)

@app.route('/')
def home():
    game = Game()
    hand = game.players[0]
    top_discard = game.discard_pile[-1]
    cards = [str(card) for card in hand]
    top_discard_card = str(top_discard)
    return render_template('index.html', cards=cards, top_discard_card=top_discard_card)

if __name__ == '__main__':
    app.run(debug=True)