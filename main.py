import random

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

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    deck = Deck()
    deck.shuffle()
    hand = deck.deal(7)
    cards = [str(card) for card in hand]
    return render_template('index.html', cards=cards)

if __name__ == '__main__':
    app.run(debug=True)