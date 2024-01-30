# Implementing a simple poker game
# In this game, two players each receive two cards, and the player with the higher card wins.

import random

class Card:
    """Card class, defining card ranks and suits"""
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    suits = ["Clubs", "Diamonds", "Hearts", "Spades"]

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    """Deck class, includes functionality to create and shuffle 52 cards"""
    def __init__(self):
        self.cards = [Card(rank, suit) for rank in Card.ranks for suit in Card.suits]
        random.shuffle(self.cards)

    def draw_card(self):
        """Draw a single card from the deck"""
        return self.cards.pop()

class PokerGame:
    """Poker game class, two players play the game"""
    def __init__(self):
        self.deck = Deck()

    def play(self):
        # Distribute two cards to each of the two players
        player1_hand = [self.deck.draw_card(), self.deck.draw_card()]
        player2_hand = [self.deck.draw_card(), self.deck.draw_card()]

        print(f"Player 1's hand: {player1_hand}")
        print(f"Player 2's hand: {player2_hand}")

        # Simple logic to determine the winner: Compare only by rank
        p1_max_rank = max(player1_hand, key=lambda card: Card.ranks.index(card.rank))
        p2_max_rank = max(player2_hand, key=lambda card: Card.ranks.index(card.rank))

        if Card.ranks.index(p1_max_rank.rank) > Card.ranks.index(p2_max_rank.rank):
            print("Player 1 wins!")
        elif Card.ranks.index(p1_max_rank.rank) < Card.ranks.index(p2_max_rank.rank):
            print("Player 2 wins!")
        else:
            print("It's a tie!")

# Create and play the game instance
game = PokerGame()
game.play()
