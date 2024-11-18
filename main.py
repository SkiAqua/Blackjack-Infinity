import input_methods
from random import choice
def get_all_cards():
    # Defining the suits and their icons
    suits = [
        {"name": "Hearts", "icon": "♥"},
        {"name": "Spades", "icon": "♠"},
        {"name": "Diamonds", "icon": "♦"},
        {"name": "Clubs", "icon": "♣"}
    ]

    # Defining the card values and names
    values = [
        {"name": "Ace", "value": 11},
        {"name": "2", "value": 2},
        {"name": "3", "value": 3},
        {"name": "4", "value": 4},
        {"name": "5", "value": 5},
        {"name": "6", "value": 6},
        {"name": "7", "value": 7},
        {"name": "8", "value": 8},
        {"name": "9", "value": 9},
        {"name": "10", "value": 10},
        {"name": "Jack", "value": 10},
        {"name": "Queen", "value": 10},
        {"name": "King", "value": 10}
    ]

    # Generate the full deck
    deck = []
    for suit in suits:
        for card in values:
            deck.append({
                "icon": suit["icon"],
                "name": card["name"],
                "suit": suit["name"],
                "value": card["value"]
            })

    return deck

class Game:
    HIT = 0
    STAND = 1
    DOUBLEDOWN = 2
    SPLIT = 3
    SURRENDER = 4

    def __init__(self,input, start_credit=0, max_rounds=1):
        self.input = input(self)
        self.start_credits = start_credit
        self.credits = start_credit
        self.minimun_bet = 1
        self.this_bet = 1

        self.game_reset()
        self.max_rounds = max_rounds
        self.this_round = 0

        while self.this_round <= self.max_rounds:
            self.this_round += 1
            self.run()
            if self.credits <= 0:
                break
        
        self.input.game_end()
    
    def run(self):
        #Game reset
        self.game_reset()
        #Player choose the bet
        self.input.choose_bet()
        #Player takes two cards
        self.give_random_card_to(self.player_cards)
        self.give_random_card_to(self.player_cards)

        #Dealer takes one card, and one dark card
        self.give_random_card_to(self.dealer_cards)

        self.dealer_darkcard = choice(self.available_cards)
        self.available_cards.remove(self.dealer_darkcard)

        if self.get_dealer_value() == 21:
            self.dealer_blackjack = True
        if self.get_player_value() == 21:
            self.blackjack = True
        
        while not self.busted and not self.dealer_busted and not self.blackjack and not self.dealer_blackjack:
            #O jogador recebe suas primeiras opções
            player_decision = self.input.prompt_action()



            match player_decision:
                case self.HIT:
                    self.give_random_card_to(self.player_cards)
                    self.turn += 1
                    if self.get_player_value() > 21:
                        self.busted = True
                
                case self.STAND:
                    self.dealer_cards.append(self.dealer_darkcard)
                    if self.get_dealer_value() < 17:
                        while True:
                            self.give_random_card_to(self.dealer_cards)
                            if self.get_dealer_value() > 16:
                                break
                        if self.get_dealer_value() > 21:
                            self.dealer_busted = True
                    break
        
        if self.busted:
            self.credits -= self.this_bet
            self.input.set_lost()

        elif self.dealer_busted:
            self.credits += self.this_bet
            self.input.set_win()
        
        elif self.blackjack and self.dealer_blackjack:
            self.input.set_draw()
        
        elif self.blackjack:
            self.credits += self.this_bet * 1.5
            self.input.set_win()
    
        else:
            if self.get_dealer_value() > self.get_player_value():
                self.credits -= self.this_bet
                self.input.set_lost()
            elif self.get_dealer_value() < self.get_player_value():
                self.credits += self.this_bet
                self.input.set_win()
            else: # dealer value == player value
                self.input.set_draw()

    def give_random_card_to(self, cardlist):
        card = choice(self.available_cards)
        self.available_cards.remove(card)
        cardlist.append(card)

    def get_dealer_value(self, return_ace=False):
        return self.calculate_value(self.dealer_cards)

    def get_player_value(self,return_ace=False):
        return self.calculate_value(self.player_cards)
    
    def get_ace_int(card_list):
        aces = 0
        for card in card_list:
            if card['name'] == 'Ace':
                aces += 1
        
        return aces
    def game_reset(self):
        self.turn = 1
        self.busted = False
        self.blackjack = False
        self.dealer_busted = False
        self.dealer_blackjack = False

        self.available_cards = get_all_cards()
        self.dealer_cards = []
        self.dealer_darkcard = None
        self.player_cards = []

    @staticmethod
    def calculate_value(card_list):
        total_value = 0
        ace_count = 0
        
        for card in card_list:
            if card['name'] == 'Ace':
                ace_count += 1
            else:
                total_value += card['value']
        
        while ace_count > 0:
            if total_value + 11 > 21:
                total_value += 1
            else:
                total_value += 11
            ace_count -= 1
        
        return total_value



if __name__ == "__main__":
    Game(input_methods.NeuralNetworkInput, 500,2000)