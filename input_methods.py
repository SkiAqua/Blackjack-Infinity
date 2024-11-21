import numpy as np
import random
import os

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
        self.monte_carlo_assistance = input('Use AI assistance y/n: ')
        self.monte_carlo_assistance = True if self.monte_carlo_assistance[0] == 'y' else False

        if self.monte_carlo_assistance and not os.path.isfile('MonteCarloData'):
            raise Exception('Monte Carlo não foi treinado')
        if self.monte_carlo_assistance:
            self.load_monte_carlo()

    def prompt_action(self):
        player_decision = ''
        
        if self.game.turn == 1:
            print('This game bet is:',self.game.this_bet)
        
        print('Dealer value:', self.game.get_dealer_value())
        print('Player value:', self.game.get_player_value())

        while True:
            if self.monte_carlo_assistance:
                round_size = len(self.game.history)
                related_games = []

                hit_wins = 0
                stand_wins = 0
                total_wins = 0
                for g in self.monte_carlo_data:
                    if len(g) >= round_size:
                        if g[:round_size] == [x['name'] for x in self.game.history]:
                            related_games.append(g)
                            if g[round_size] == 'hit' and g[-1] == '1':
                                hit_wins += 1
                                total_wins += 1
                            elif g[round_size] == 'stand' and g[-1] == '1':
                                stand_wins += 1
                                total_wins += 1
                if hit_wins == stand_wins:
                    print(('(50/50)'))
                else:
                    hit_per = hit_wins / total_wins * 100
                    stand_per = stand_wins / total_wins * 100

                    best_name = 'hit' if hit_wins > stand_wins else 'stand'
                    worst_name = 'hit' if best_name == 'stand' else 'stand'
                    best_per = hit_per if hit_wins > stand_wins else stand_per
                    worst_per = hit_per if best_per == stand_per else stand_per

                    print(f'({best_per:.2f}% {best_name})')
                    print(f'({worst_per:.2f}% {worst_name})')
            
            player_decision = input('>> ').lower().strip()

            if player_decision == 'hit':
                return 0
            elif player_decision == 'stand':
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
        input()

    def load_monte_carlo(self):
        self.monte_carlo_data = MonteCarloTraining(self.game).read_file()
        
    
class MonteCarloTraining(InputMethod):
    def __init__(self, game, data_file_name='MonteCarloData'):
        super().__init__(game)
        self.data_file_name = data_file_name
        self.data = []

        #Inicializando os dados do arquivo
        if not os.path.isfile(data_file_name):
            with open(data_file_name, 'w') as f:
                pass
        
        self.read_file()
    
    def prompt_action(self):
        return random.randint(0,1)
    
    def choose_bet(self):
        return 0
    
    def set_win(self):
        self.end_round(1)
    
    def set_lost(self):
        self.end_round(0)
    
    def set_draw(self):
        self.end_round(2)

    def end_round(self, round_result: int):
        self.data.append([x['name'] for x in self.game.history] + [str(round_result)])
    
    def game_end(self):
        self.save_file()
        print('Game ended...')

    def read_file(self):
        with open(self.data_file_name) as f:
            data = f.readlines()
        
        # Filtrar linhas vazias e processar corretamente
        processed_data = [x.strip().split(',') for x in data if x.strip()]
        
        # Adicionar os dados processados diretamente
        self.data.extend(processed_data)
        return self.data

    def save_file(self, chunk_size=1000):
        with open(self.data_file_name, 'w') as f:
            buffer = []

            for i, value in enumerate(self.data):
                # Adiciona a linha ao buffer
                buffer.append(','.join(value))
                
                # Escreve no arquivo quando o buffer atinge o tamanho do chunk
                if (i + 1) % chunk_size == 0:
                    f.write('\n'.join(buffer) + '\n')
                    buffer = []

            # Escreve o restante do buffer
            if buffer:
                f.write('\n'.join(buffer) + '\n')