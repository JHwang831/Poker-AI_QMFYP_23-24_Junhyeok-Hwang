import random
from collections import Counter
import math
import numpy as np

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

class PokerQAgent:
    """A poker AI that uses Q-learning for decision-making."""
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.2):
        self.q_table = {}  # Q-values table
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate

    def get_state(self, hand, community_cards):
        """Define how to represent the state."""
        return (PokerHand(hand + community_cards).evaluate_hand(), len(community_cards))

    def get_possible_actions(self, state):
        """Simple action space."""
        return ['fold', 'call', 'raise']

    def best_action(self, state):
        """Choose the best action based on Q-table or explore new actions."""
        actions = self.get_possible_actions(state)
        if random.random() < self.epsilon:  # Exploration
            return random.choice(actions)
        q_values = [self.q_table.get((state, a), 0) for a in actions]
        return actions[np.argmax(q_values)]

    def update_q_table(self, state, action, reward, next_state):
        """Update Q-values based on the outcome."""
        best_next_action = self.best_action(next_state)
        current_q = self.q_table.get((state, action), 0)
        next_q = self.q_table.get((next_state, best_next_action), 0)
        new_q = current_q + self.alpha * (reward + self.gamma * next_q - current_q)
        self.q_table[(state, action)] = new_q

    def save_q_table(self, filepath):
        """Save the Q-table to a file."""
        np.save(filepath, self.q_table)

    def load_q_table(self, filepath):
        """Load the Q-table from a file."""
        self.q_table = np.load(filepath, allow_pickle=True).item()

def determine_winner(player_hand, ai_hand, community_cards):
    """Determines the winner based on poker hand rankings."""
    player_poker_hand = PokerHand(player_hand + community_cards)
    ai_poker_hand = PokerHand(ai_hand + community_cards)
    player_rank = player_poker_hand.evaluate_hand()
    ai_rank = ai_poker_hand.evaluate_hand()

    if player_rank > ai_rank:
        return "Player wins!", 1  # AI loses
    elif ai_rank > player_rank:
        return "AI wins!", -1  # AI wins
    else:
        return "It's a tie!", 0  # Neutral outcome

def play_game():
    """Manages the gameplay logic."""
    deck = Deck()
    community_cards = []
    rounds = ["Flop", "Turn", "River"]
    num_cards = [3, 1, 1]

    ai = PokerQAgent()
    player_hand = [deck.draw_card(), deck.draw_card()]
    ai_hand = [deck.draw_card(), deck.draw_card()]

    print("\nStarting new game...")
    print("Your Hand:", player_hand)

    for round_name, cards in zip(rounds, num_cards):
        for _ in range(cards):
            community_cards.append(deck.draw_card())
        print(f"\n{round_name}: {community_cards}")

        # AI decision
        state = ai.get_state(ai_hand, community_cards)
        action = ai.best_action(state)
        print(f"AI decides to {action}")

        if action == "fold":
            print("AI folds.")
            return "Player wins!", 1  # Immediate win for the player

    winner, reward = determine_winner(player_hand, ai_hand, community_cards)
    print("\nFinal Community Cards:", community_cards)
    print("Your Hand:", player_hand)
    print("AI Hand:", ai_hand)
    print(winner)
    return winner, reward

if __name__ == "__main__":
    # Play multiple games and learn from them
    ai = PokerQAgent()
    for i in range(1000):
        play_game()
        # Update the Q-table based on outcomes here (not shown, depends on game mechanics)
    ai.save_q_table('poker_q_table.npy')
