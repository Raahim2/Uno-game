import random
from flask import Flask, request, jsonify

class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __str__(self):
        return f"{self.color} {self.value}"

    def to_dict(self):
        return {"color": self.color, "value": self.value}

class Deck:
    def __init__(self):
        self.cards = []
        colors = ["red", "blue", "green", "yellow"]
        values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip", "Reverse", "+2"]
        for color in colors:
            for value in values:
                self.cards.append(Card(color, value))
            self.cards.append(Card(color,"Skip"))
            self.cards.append(Card(color,"Reverse"))
            self.cards.append(Card(color,"+2"))

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
                break
        return dealt_cards

class Game:
    def __init__(self, game_id):
        self.game_id = game_id
        self.deck = Deck()
        self.deck.shuffle()
        self.discard_pile = []
        self.players = []
        self.current_player = 0
        self.num_players = 0

    def add_player(self, player_id):
        self.players.append({"id": player_id, "hand": self.deck.deal(7)})
        self.num_players +=1
        if self.num_players == 1:
            self.discard_pile.append(self.deck.deal(1)[0])

    def play_card(self, player_id, card):
        player = self.get_player(player_id)
        if player and card in player["hand"]:
            player["hand"].remove(card)
            self.discard_pile.append(card)
            self.current_player = (self.current_player + 1) % self.num_players
            return True
        return False

    def draw_card(self, player_id):
        player = self.get_player(player_id)
        if player and self.deck.cards:
            card = self.deck.deal(1)[0]
            player["hand"].append(card)
            return True
        return False

    def get_player(self, player_id):
        for player in self.players:
            if player["id"] == player_id:
                return player
        return None

    def get_top_discard(self):
        if self.discard_pile:
            return self.discard_pile[-1]
        return None

games = {}
app = Flask(__name__)

@app.route('/create_game', methods=['POST'])
def create_game():
    game_id = len(games) + 1
    games[game_id] = Game(game_id)
    return jsonify({"game_id": game_id})

@app.route('/join_game/<int:game_id>', methods=['POST'])
def join_game(game_id):
    player_id = request.json.get('player_id')
    if game_id in games:
        games[game_id].add_player(player_id)
        return jsonify({"message": "Joined game"})
    return jsonify({"error": "Game not found"}), 404

@app.route('/play_card/<int:game_id>', methods=['POST'])
def play_card(game_id):
    player_id = request.json.get('player_id')
    card = request.json.get('card')
    if game_id in games:
        success = games[game_id].play_card(player_id, card)
        return jsonify({"success": success})
    return jsonify({"error": "Game not found"}), 404

@app.route('/draw_card/<int:game_id>', methods=['POST'])
def draw_card(game_id):
    player_id = request.json.get('player_id')
    if game_id in games:
        success = games[game_id].draw_card(player_id)
        return jsonify({"success": success})
    return jsonify({"error": "Game not found"}), 404

@app.route('/game_state/<int:game_id>', methods=['GET'])
def game_state(game_id):
    if game_id in games:
        game = games[game_id]
        player = game.get_player(request.args.get('player_id'))
        if player:
            top_discard = game.get_top_discard().to_dict() if game.get_top_discard() else None
            return jsonify({"hand": [card.to_dict() for card in player["hand"]], "top_discard": top_discard})
        return jsonify({"error": "Player not found in game"}), 404
    return jsonify({"error": "Game not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)