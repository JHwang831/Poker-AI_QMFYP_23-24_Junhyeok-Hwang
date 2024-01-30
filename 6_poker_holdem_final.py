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
    def __init__(self):
        self.deck = Deck()
        self.pot = 0
        self.community_cards = []
        self.player_hands = {1: [], 2: []}
        self.player_bets = {1: 0, 2: 0}
        self.current_player = 1
        self.blinds = (10, 20) # Small and big blinds

    def start_new_round(self):
        """Starts a new round of Texas Hold'em."""
        self.community_cards.clear()
        self.player_hands[1] = [self.deck.draw_card(), self.deck.draw_card()]
        self.player_hands[2] = [self.deck.draw_card(), self.deck.draw_card()]
        self.player_bets = {1: self.blinds[0], 2: self.blinds[1]}
        self.pot = sum(self.blinds)
        self.current_player = 1

    def display_game_state(self):
        """Displays the current state of the game."""
        print(f"\nPlayer 1's hand: {self.player_hands[1]}")
        print(f"Player 2's hand: {self.player_hands[2]}")
        print(f"Community Cards: {self.community_cards}")
        print(f"Current Pot: {self.pot}")
        print(f"Player Bets: {self.player_bets}\n")

    def betting_round(self):
        """Handles a round of betting."""
        while True:
            self.display_game_state()
            action = input(f"Player {self.current_player}, choose 'call', 'raise', or 'fold': ").lower()
            if action == 'call':
                self.handle_call()
            elif action == 'raise':
                raise_amount = int(input("Enter raise amount: "))
                self.handle_raise(raise_amount)
            elif action == 'fold':
                self.handle_fold()
                break

            if self.player_bets[1] == self.player_bets[2]:
                break

            self.current_player = 3 - self.current_player

    def handle_call(self):
        """Handles a call action."""
        bet_amount = max(self.player_bets.values()) - self.player_bets[self.current_player]
        self.pot += bet_amount
        self.player_bets[self.current_player] += bet_amount

    def handle_raise(self, amount):
        """Handles a raise action."""
        self.pot += amount
        self.player_bets[self.current_player] += amount

    def handle_fold(self):
        """Handles a fold action."""
        winner = 3 - self.current_player
        print(f"Player {self.current_player} folds. Player {winner} wins the pot!")
        self.pot = 0

    def deal_community_cards(self, number):
        """Deals a specified number of community cards."""
        for _ in range(number):
            self.community_cards.append(self.deck.draw_card())

    def play(self):
        """Plays a round of Texas Hold'em poker."""
        self.start_new_round()
        self.betting_round()  # Pre-flop betting

        # Flop, Turn, River
        for round_name, cards_to_deal in [("Flop", 3), ("Turn", 1), ("River", 1)]:
            self.deal_community_cards(cards_to_deal)
            self.betting_round()

        # Determine the winner
        winner = self.determine_winner(self.player_hands[1], self.player_hands[2])
        print(f"Winner: Player {winner} wins the pot!")
        
    def run_game(self):
        """Runs the entire game."""
        while True:
            self.play()
            if input("Play another round? (yes/no): ").lower() != 'yes':
                break
            
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
            return 1
        elif hand_strength[p2_hand_rank[0]] > hand_strength[p1_hand_rank[0]]:
            return 2
        else:
            return "It's a tie! Pot is split."

# Create and play the game instance
game = PokerGame()
game.run_game()
