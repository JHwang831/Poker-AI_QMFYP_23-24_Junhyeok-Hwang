import openai
import numpy as np
import random
from collections import Counter
import math

class Card:
    """Represents a playing card with a rank and a suit."""
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

class Node:
    """Represents a node in the Monte Carlo Tree Search."""
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0

    def add_child(self, child_state):
        child = Node(child_state, self)
        self.children.append(child)
        return child

    def update(self, result):
        self.visits += 1
        self.wins += result

    def fully_expanded(self):
        return len(self.children) == len(self.state.legal_moves())

    def best_child(self, exploration_weight=1.41):
        """Selects the best child using the UCB1 formula, accounting for exploration and exploitation."""
        if self.parent is None:
            # For the root node, ignore the exploration part of UCB1 as there's no parent.
            best = max(self.children, key=lambda x: x.wins / x.visits)
        else:
            # Regular UCB1 calculation for non-root nodes.
            best = max(self.children, key=lambda x: x.wins / x.visits + exploration_weight * math.sqrt(math.log(self.parent.visits) / x.visits))
        return best

class MCTS:
    """Monte Carlo Tree Search algorithm."""
    def __init__(self, exploration_weight=1.41):
        self.exploration_weight = exploration_weight

    def choose_move(self, state):
        root = Node(state)

        for _ in range(1000):  # Number of simulations
            node = root
            # Selection
            while node.fully_expanded() and not node.state.is_terminal():
                node = node.best_child()
            # Expansion
            if not node.fully_expanded():
                new_state = random.choice(list(set(node.state.legal_moves()) - set(child.state for child in node.children)))
                node = node.add_child(new_state)
            # Simulation
            outcome = self.simulate_random_game(node.state)
            # Backpropagation
            while node is not None:
                node.update(outcome)
                node = node.parent

        return root.best_child().state

    def simulate_random_game(self, state):
        """Simulates a random game based on current state."""
        current_state = state
        while not current_state.is_terminal():
            possible_moves = current_state.legal_moves()
            current_state = random.choice(possible_moves)
        return current_state.game_result()

class PokerGameState:
    """Represents the state of a poker game used by MCTS."""
    def __init__(self, hand, community_cards, pot, is_terminal=False, current_bet=0):
        self.hand = hand
        self.community_cards = community_cards
        self.pot = pot
        self.current_bet = current_bet
        self.is_terminal_state = is_terminal

    def legal_moves(self):
        """Generates legal moves from the current state, including folds, calls, and raises."""
        moves = []

        # Fold
        moves.append(PokerGameState(self.hand, self.community_cards, self.pot, True))

        if len(self.community_cards) < 5:
            # Call
            new_cards = [Deck().draw_card() for _ in range(5 - len(self.community_cards))]
            moves.append(PokerGameState(self.hand, self.community_cards + new_cards, self.pot + self.current_bet))

            # Raises
            for raise_amount in [10, 20, 50]:  # Example raise amounts
                moves.append(PokerGameState(self.hand, self.community_cards + new_cards, self.pot + self.current_bet + raise_amount))
        else:
            # No more cards to deal, the game will move to showdown after the bet
            moves.append(PokerGameState(self.hand, self.community_cards, self.pot + self.current_bet, True))

        return moves

    def is_terminal(self):
        """Checks if the game state is terminal."""
        return self.is_terminal_state or len(self.community_cards) == 5

    def game_result(self):
        """Evaluates the game result from the perspective of the AI."""
        ph = PokerHand(self.hand + self.community_cards)
        winning_hands = ["Straight Flush", "Four of a Kind", "Full House", "Flush"]
        if ph.rank in winning_hands:
            return 1  # AI wins
        return -1  # AI loses

class PokerAI:
    """A poker AI that uses ChatGPT API for decision-making."""
    def __init__(self, api_key):
        self.api_key = api_key

    def make_decision(self, hand, community_cards):
        state = PokerGameState(hand, community_cards, pot=0, current_bet=0)
        context = "You have: " + str(hand) + "\nCommunity cards: " + str(community_cards) + "\nWhat should you do?"
        response = self.get_chat_response(context)
        return self.process_response(response)

    def get_chat_response(self, context):
        openai.api_key = self.api_key
        response = openai.Completion.create(
            engine="davinci-codex",
            prompt=context,
            max_tokens=50,
            temperature=0.7,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return response.choices[0].text.strip()

    def process_response(self, response):
        # Example: Extract action and bet from the response
        # Implement your logic here based on the response from ChatGPT
        action = "call"
        bet = 10
        return action, bet

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

    if player_rank > ai_rank:
        return "Player wins!"
    elif ai_rank > player_rank:
        return "AI wins!"
    else:
        return "It's a tie!"

def play_game():
    """Manages the gameplay logic."""
    deck = Deck()
    community_cards = []
    rounds = ["Flop", "Turn", "River"]
    num_cards = [3, 1, 1]

    api_key = "your_openai_api_key"  # Replace this with your actual OpenAI API key
    ai = PokerAI(api_key)
    player_hand = [deck.draw_card(), deck.draw_card()]
    ai_hand = [deck.draw_card(), deck.draw_card()]

    print("\nStarting new game...")
    print("Your Hand:", player_hand)

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

if __name__ == "__main__":
    while True:
        play_game()
        if input("\nPlay again? (yes/no): ").lower() != 'yes':
            break
