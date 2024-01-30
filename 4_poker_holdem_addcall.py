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

class PokerHand:
    """Represents a poker hand and can determine its rank."""
    def __init__(self, cards):
        self.cards = cards

    def evaluate_hand(self):
        # For simplicity, this method will just return the highest card rank for now.
        # In a full poker game, this would evaluate the hand rank (e.g., pair, flush, etc.)
        return max(self.cards, key=lambda card: Card.ranks.index(card.rank))

class PokerGame:
    """Simulates a Texas Hold'em poker game for two players."""
    def __init__(self):
        self.deck = Deck()
        self.pot = 0
        self.community_cards = []
        self.current_bet = 0

    def betting_action(self, player, action, amount=0):
        """Handles a player's betting action (call, raise, fold)."""
        if action == 'raise':
            self.pot += amount
            self.current_bet = amount
            print(f"Player {player} raises to {amount}. Total pot is now {self.pot}.")
        elif action == 'call':
            self.pot += self.current_bet
            print(f"Player {player} calls. Total pot is now {self.pot}.")
        elif action == 'fold':
            print(f"Player {player} folds.")
            return False
        return True

    def bet(self, player):
        """Simulates a betting round."""
        action = input(f"Player {player}, choose 'call', 'raise', or 'fold': ").lower()
        if action == 'raise':
            amount = int(input("How much do you want to raise? "))
            return self.betting_action(player, action, amount)
        elif action == 'call':
            return self.betting_action(player, action)
        elif action == 'fold':
            return self.betting_action(player, action)
        return False

    def deal_community_cards(self, number):
        """Deals a specified number of community cards."""
        for _ in range(number):
            self.community_cards.append(self.deck.draw_card())
        print(f"Community Cards: {self.community_cards}")

    def play(self):
        """Plays a round of Texas Hold'em poker."""
        player1_hand = [self.deck.draw_card(), self.deck.draw_card()]
        player2_hand = [self.deck.draw_card(), self.deck.draw_card()]

        print(f"Player 1's hand: {player1_hand}")
        print(f"Player 2's hand: {player2_hand}")

        # Pre-flop betting round
        if not self.bet(1) or not self.bet(2):
            return

        # Flop
        self.deal_community_cards(3)
        if not self.bet(1) or not self.bet(2):
            return

        # Turn
        self.deal_community_cards(1)
        if not self.bet(1) or not self.bet(2):
            return

        # River
        self.deal_community_cards(1)
        if not self.bet(1) or not self.bet(2):
            return

        # Determine winner based on best hand
        p1_best_hand = PokerHand(player1_hand + self.community_cards).evaluate_hand()
        p2_best_hand = PokerHand(player2_hand + self.community_cards).evaluate_hand()

        if Card.ranks.index(p1_best_hand.rank) > Card.ranks.index(p2_best_hand.rank):
            print("Player 1 wins the pot!")
        elif Card.ranks.index(p1_best_hand.rank) < Card.ranks.index(p2_best_hand.rank):
            print("Player 2 wins the pot!")
        else:
            print("It's a tie! Pot is split.")

# Create and play the game instance
game = PokerGame()
game.play()
