import random

class Card:
    """Defines a playing card with a rank and a suit."""
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    suits = ["Clubs", "Diamonds", "Hearts", "Spades"]

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    """Represents a deck of 52 playing cards."""
    def __init__(self):
        self.cards = [Card(rank, suit) for rank in Card.ranks for suit in Card.suits]
        random.shuffle(self.cards)

    def draw_card(self):
        """Draws a single card from the deck."""
        return self.cards.pop()

class PokerGame:
    """Simulates a simple two-player poker game with betting and the option to fold."""
    def __init__(self):
        self.deck = Deck()
        self.pot = 0

    def bet(self, player):
        """Simulates a betting round. Returns True if player continues, False if they fold."""
        choice = input(f"Player {player}, do you want to 'bet' or 'fold'? ")
        if choice.lower() == 'bet':
            amount = int(input("How much do you want to bet? "))
            self.pot += amount
            print(f"Player {player} bets {amount}. Total pot is now {self.pot}.")
            return True
        else:
            print(f"Player {player} folds.")
            return False

    def play(self):
        """Plays a round of poker."""
        player1_hand = [self.deck.draw_card(), self.deck.draw_card()]
        player2_hand = [self.deck.draw_card(), self.deck.draw_card()]

        print(f"Player 1's hand: {player1_hand}")
        print(f"Player 2's hand: {player2_hand}")

        # Player 1 betting
        if not self.bet(1):
            print("Player 2 wins!")
            return

        # Player 2 betting
        if not self.bet(2):
            print("Player 1 wins!")
            return

        # Determine winner based on highest card rank
        p1_max_rank = max(player1_hand, key=lambda card: Card.ranks.index(card.rank))
        p2_max_rank = max(player2_hand, key=lambda card: Card.ranks.index(card.rank))

        if Card.ranks.index(p1_max_rank.rank) > Card.ranks.index(p2_max_rank.rank):
            print("Player 1 wins the pot!")
        elif Card.ranks.index(p1_max_rank.rank) < Card.ranks.index(p2_max_rank.rank):
            print("Player 2 wins the pot!")
        else:
            print("It's a tie! Pot is split.")

# Create and play the game instance
game = PokerGame()
game.play()

