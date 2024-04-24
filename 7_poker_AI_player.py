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
    """Evaluates poker hands and determines their rank."""
    def __init__(self, cards):
        self.cards = sorted(cards, key=lambda card: Card.ranks.index(card.rank), reverse=True)
        self.rank = self.evaluate_hand()

    def evaluate_hand(self):
        if self.is_straight_flush():
            return "Straight Flush"
        elif self.is_four_of_a_kind():
            return "Four of a Kind"
        elif self.is_full_house():
            return "Full House"
        elif self.is_flush():
            return "Flush"
        elif self.is_straight():
            return "Straight"
        elif self.is_three_of_a_kind():
            return "Three of a Kind"
        elif self.is_two_pair():
            return "Two Pair"
        elif self.is_one_pair():
            return "One Pair"
        else:
            return "High Card"

    def is_straight_flush(self):
        return self.is_straight() and self.is_flush()

    def is_four_of_a_kind(self):
        return 4 in Counter(card.rank for card in self.cards).values()

    def is_full_house(self):
        ranks = Counter(card.rank for card in self.cards)
        return 3 in ranks.values() and 2 in ranks.values()

    def is_flush(self):
        return len(set(card.suit for card in self.cards)) == 1

    def is_straight(self):
        indices = sorted(Card.ranks.index(card.rank) for card in self.cards)
        return indices == list(range(min(indices), min(indices) + 5)) or indices == [0, 1, 2, 3, 12]  # Ace low straight

    def is_three_of_a_kind(self):
        return 3 in Counter(card.rank for card in self.cards).values()

    def is_two_pair(self):
        ranks = Counter(card.rank for card in self.cards)
        return list(ranks.values()).count(2) == 2

    def is_one_pair(self):
        return 2 in Counter(card.rank for card in self.cards).values()

class PokerAI:
    """A simple poker AI that decides actions based on hand strength."""
    def __init__(self):
        self.hand_strengths = {
            "Straight Flush": 8, "Four of a Kind": 7, "Full House": 6,
            "Flush": 5, "Straight": 4, "Three of a Kind": 3,
            "Two Pair": 2, "One Pair": 1, "High Card": 0
        }

    def make_decision(self, hand, community_cards):
        """Determines AI's action based on the combined hand strength."""
        full_hand = hand + community_cards
        poker_hand = PokerHand(full_hand)
        hand_rank = poker_hand.evaluate_hand()
        hand_strength = self.hand_strengths[hand_rank]

        if hand_strength > 4:
            return "raise", 50  # Strong hands
        elif hand_strength > 2:
            return "call", 0  # Medium hands
        else:
            return "fold", 0  # Weak hands

def player_action():
    """Allows the player to choose an action."""
    while True:
        action = input("Choose 'call', 'raise', or 'fold': ").lower()
        if action in ['call', 'raise', 'fold']:
            if action == 'raise':
                amount = int(input("Enter raise amount: "))
                return action, amount
            return action, 0
        print("Invalid action, please choose again.")

def determine_winner(player_hand, ai_hand, community_cards):
    """Determines the winner based on poker hand rankings."""
    player_poker_hand = PokerHand(player_hand + community_cards)
    ai_poker_hand = PokerHand(ai_hand + community_cards)
    player_rank = player_poker_hand.evaluate_hand()
    ai_rank = ai_poker_hand.evaluate_hand()
    player_strength = player_poker_hand.hand_strengths[player_rank]
    ai_strength = ai_poker_hand.hand_strengths[ai_rank]

    if player_strength > ai_strength:
        return "Player wins!"
    elif ai_strength > player_strength:
        return "AI wins!"
    else:
        return "It's a tie!"

def play_game():
    deck = Deck()
    community_cards = []
    rounds = ["Flop", "Turn", "River"]
    num_cards = [3, 1, 1]

    ai = PokerAI()
    player_hand = [deck.draw_card(), deck.draw_card()]
    ai_hand = [deck.draw_card(), deck.draw_card()]

    print("\nStarting new game...")
    print("Your Hand:", player_hand)

    # Pre-flop
    player_decision, player_bet = player_action()
    ai_decision, ai_bet = ai.make_decision(ai_hand, community_cards)
    print(f"You decided to {player_decision} with a bet of {player_bet}")
    print(f"AI decides to {ai_decision} with a bet of {ai_bet}")

    if player_decision == "fold" or ai_decision == "fold":
        winner = "AI wins!" if player_decision == "fold" else "Player wins!"
        print(winner)
        return

    for round_name, cards in zip(rounds, num_cards):
        for _ in range(cards):
            community_cards.append(deck.draw_card())
        print(f"\n{round_name}: {community_cards}")

        player_decision, player_bet = player_action()
        ai_decision, ai_bet = ai.make_decision(ai_hand, community_cards)
        print(f"You decided to {player_decision} with a bet of {player_bet}")
        print(f"AI decides to {ai_decision} with a bet of {ai_bet}")

        if player_decision == "fold" or ai_decision == "fold":
            winner = "AI wins!" if player_decision == "fold" else "Player wins!"
            print(winner)
            return

    winner = determine_winner(player_hand, ai_hand, community_cards)
    print("\nFinal Community Cards:", community_cards)
    print("Your Hand:", player_hand)
    print("AI Hand:", ai_hand)
    print(winner)

while True:
    play_game()
    if input("\nPlay again? (yes/no): ").lower() != 'yes':
        break
