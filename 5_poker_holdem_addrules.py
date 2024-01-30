import random
from collections import Counter

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
        self.cards = sorted(cards, key=lambda card: Card.ranks.index(card.rank), reverse=True)
        self.rank = self.evaluate_hand()

    def evaluate_hand(self):
        # Evaluates and returns the rank of the hand
        if self.is_straight_flush():
            return ("Straight Flush", self.cards[0].rank)
        elif self.is_four_of_a_kind():
            return ("Four of a Kind", self.cards[0].rank)
        elif self.is_full_house():
            return ("Full House", self.cards[0].rank)
        elif self.is_flush():
            return ("Flush", self.cards[0].rank)
        elif self.is_straight():
            return ("Straight", self.cards[0].rank)
        elif self.is_three_of_a_kind():
            return ("Three of a Kind", self.cards[0].rank)
        elif self.is_two_pair():
            return ("Two Pair", self.cards[0].rank)
        elif self.is_one_pair():
            return ("One Pair", self.cards[0].rank)
        else:
            return ("High Card", self.cards[0].rank)

    def is_straight_flush(self):
        return self.is_straight() and self.is_flush()

    def is_four_of_a_kind(self):
        ranks = [card.rank for card in self.cards]
        return 4 in Counter(ranks).values()

    def is_full_house(self):
        ranks = [card.rank for card in self.cards]
        rank_counts = Counter(ranks).values()
        return 3 in rank_counts and 2 in rank_counts

    def is_flush(self):
        suits = [card.suit for card in self.cards]
        return len(set(suits)) == 1

    def is_straight(self):
        ranks = [Card.ranks.index(card.rank) for card in self.cards]
        ranks.sort()
        if ranks == list(range(ranks[0], ranks[0] + 5)):
            return True
        # Check for Ace-low straight (Ace, 2, 3, 4, 5)
        if ranks == [0, 1, 2, 3, 12]:
            return True
        return False

    def is_three_of_a_kind(self):
        ranks = [card.rank for card in self.cards]
        return 3 in Counter(ranks).values()

    def is_two_pair(self):
        ranks = [card.rank for card in self.cards]
        return list(Counter(ranks).values()).count(2) == 2

    def is_one_pair(self):
        ranks = [card.rank for card in self.cards]
        return 2 in Counter(ranks).values()
    
class PokerGame:
    """Simulates a Texas Hold'em poker game for two players."""
    def __init__(self):
        self.deck = Deck()
        self.pot = 0
        self.community_cards = []
        self.player_bets = {1: 0, 2: 0}
        self.last_raiser = None

    def betting_action(self, player, action, amount=0):
        """Handles a player's betting action (call, raise, fold)."""
        if action == 'raise':
            self.pot += amount - self.player_bets[player]
            self.player_bets[player] = amount
            print(f"Player {player} raises to {amount}. Total pot is now {self.pot}.")
            self.last_raiser = player
        elif action == 'call':
            call_amount = max(0, self.player_bets[self.last_raiser] - self.player_bets[player])
            self.pot += call_amount
            self.player_bets[player] += call_amount
            print(f"Player {player} calls. Total pot is now {self.pot}.")
        elif action == 'fold':
            print(f"Player {player} folds.")
            return False
        return True

    def bet_round(self):
        """Conducts a betting round."""
        active_player = 1
        while True:
            action_taken = self.bet(active_player)
            if not action_taken:
                return False  # End round if player folds

            if self.player_bets[1] == self.player_bets[2]:
                break

            active_player = 3 - active_player  # Switch to the other player

        # Reset for the next round
        self.player_bets = {1: 0, 2: 0}
        self.last_raiser = None
        return True

    def bet(self, player):
        """Simulates a betting round for a single player."""
        action = input(f"Player {player}, choose 'call', 'raise', or 'fold': ").lower()
        amount = 0
        if action == 'raise':
            amount = int(input("How much do you want to raise? "))
        return self.betting_action(player, action, amount)

    def deal_community_cards(self, number):
        """Deals a specified number of community cards."""
        for _ in range(number):
            self.community_cards.append(self.deck.draw_card())
        print(f"Community Cards: {self.community_cards}")

    def play(self):
        """Plays a round of Texas Hold'em poker."""
        print("Welcome to Texas Hold'em!")
        print("If you do not want to raise, please enter 'raise' and enter an amount of 0.")

        player1_hand = [self.deck.draw_card(), self.deck.draw_card()]
        player2_hand = [self.deck.draw_card(), self.deck.draw_card()]

        print(f"Player 1's hand: {player1_hand}")
        print(f"Player 2's hand: {player2_hand}")

        # Betting rounds
        for round_name in ["Pre-flop", "Flop", "Turn", "River"]:
            print(f"{round_name} round:")
            while True:
                if self.player_bets[1] == self.player_bets[2]:
                    if not self.bet(1) or not self.bet(2):
                        break
                else:
                    if not self.bet(1) or not self.bet(2):
                        break

            if round_name != "Pre-flop":
                self.deal_community_cards(3 if round_name == "Flop" else 1)
                print(f"Community Cards: {self.community_cards}")

        # Determine winner
        winner = self.determine_winner(player1_hand, player2_hand)
        print(winner)

    def determine_winner(self, player1_hand, player2_hand):
        """Determines the winner of the game."""
        p1_hand_rank = PokerHand(player1_hand + self.community_cards).rank
        p2_hand_rank = PokerHand(player2_hand + self.community_cards).rank

        # Compare hand ranks based on predefined hand strengths
        hand_strength = {
            "Straight Flush": 8, "Four of a Kind": 7, "Full House": 6, 
            "Flush": 5, "Straight": 4, "Three of a Kind": 3, 
            "Two Pair": 2, "One Pair": 1, "High Card": 0
        }

        if hand_strength[p1_hand_rank[0]] > hand_strength[p2_hand_rank[0]]:
            return "Player 1 wins the pot!"
        elif hand_strength[p2_hand_rank[0]] > hand_strength[p1_hand_rank[0]]:
            return "Player 2 wins the pot!"
        else:
            return "It's a tie! Pot is split."

# Create and play the game instance
game = PokerGame()
game.play()
