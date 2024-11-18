class InputMethod:
    def __init__(self, game):
        self.game = game

    def prompt_action(self):
        pass
    
    def choose_bet(self):
        pass

    def set_lost(self):
        pass

    def set_win(self):
        pass

    def set_draw(self):
        pass
    
    def game_end(self):
        pass

class TerminalInput(InputMethod):
    def __init__(self, game):
        super().__init__(game)

    def prompt_action(self):
        player_decision = ''
        
        if self.game.turn == 1:
            print('This game bet is:',self.game.this_bet)
        
        print('Dealer value:', self.game.get_dealer_value())
        print('Player value:', self.game.get_player_value())

        while True:
            player_decision = input('>> ').lower().strip()

            match player_decision:
                case 'hit':
                    return 0
                case 'stand':
                    return 1

            
            if player_decision in ['0','1']:
                return int(player_decision)
        
            if player_decision == 'show':
                print('Dealer:')
                for card in self.game.dealer_cards:
                    print(card['name'])
                
                print('Player:')
                for card in self.game.player_cards:
                    print(card['name'])
    def choose_bet(self):
        player_decision = ''


        while type(player_decision) != int:
            try:
                print('(Your currency: {})'.format(self.game.credits))
                player_decision = int(input('Place your bet: '))
                if player_decision < 1: player_decision = ''
                if player_decision > self.game.credits: player_decision = self.game.credits
            except:
                pass
        
        self.game.this_bet = player_decision

    def set_lost(self):
        print('Dealer value:', self.game.get_dealer_value())
        print('Player value:', self.game.get_player_value())
        print('You loose...')
        input()

    def set_win(self):
        print('Dealer value:', self.game.get_dealer_value())
        print('Player value:', self.game.get_player_value())
        print('You win...')
        input()

    def set_draw(self):
        print('Dealer value:', self.game.get_dealer_value())
        print('Player value:', self.game.get_player_value())
        print('Draw Game...')
        input()
    
    def game_end(self):
        print('-'* 40)
        print('The End')
        print('-'* 40)
        print(f'You played {self.game.this_round} games and started with {self.game.start_credits} credits.')
        print(f'You ended with {self.game.credits} credits')
        difference = self.game.credits - self.game.start_credits

        if difference < 0:
            print(f'You lost {-difference}, good luck next time.')
        elif difference > 0:
            print(f'You earn {difference}, good job!')
        else: #difference == 0
            print(f'Wow, a true draw.')

