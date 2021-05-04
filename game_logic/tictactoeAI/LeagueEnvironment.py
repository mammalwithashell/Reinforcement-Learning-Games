import random as rand
from os import system
from collections import defaultdict

class LeagueEnvironment:
    def __init__(self, board_env, kivy_obj):
        self.kivy_obj = kivy_obj
        self.board = board_env    

    def set_players(self, player_names, league_agents, board_agents):
        self.player_names = player_names
        self.league_agents = league_agents
        self.board_agents = board_agents
        assert(len(player_names) == len(league_agents) == len(board_agents) )
        self.num_players = len(player_names)

    def reset_pair(self):
        # randomly select 2 players
        player_indices = list(range(self.num_players))
        self.Ai = rand.choice(player_indices)
        self.board.set_players(self.board_agents[self.Ai])
        self.first = self.board.reset()
        self.league_agents[self.Ai].reset_past()
        self.A_wins = 0;
        self.A_chips=100;
        self.Player_wins = 0;
        self.Player_chips=100;
        self.ties = 0;
        self.state_perspective = 'A' # the state in wins/ties/losses for which player
        self.chip_mul=1
        self.min_bid=5
        self.game_counter=1

    def get_state(self):  
        return (self.A_chips,self.A_wins,self.ties,self.Player_chips,self.Player_wins,self.player_names[self.Ai],'learning strategy and tactics')

    def pair_games_played(self):
        return self.A_wins + self.ties + self.B_wins

    def available_actions(self, first):
        if first:
            return ['quit','single bet','double bet','triple bet']
        else:
            return ['quit','call']

    def play_pair(self):
        system('clear')
        self.reset_pair()

        player_choice = ''

        while(True):

            if self.first:
                player_choice = self.league_choice(True)
                AI_choice = self.league_agents[self.Ai].select_action(False)
                print("Opponent chose", AI_choice)
            else:
                AI_choice = self.league_agents[self.Ai].select_action(True)
                player_choice = self.league_choice(False, AI_choice)

            if AI_choice == 'quit' or player_choice == 'quit':
                break
            elif AI_choice == 'single bet' or player_choice == 'single bet':
                self.chip_mul=1
            elif AI_choice == 'double bet' or player_choice == 'double bet':
                self.chip_mul=2
            elif AI_choice == 'triple bet' or player_choice == 'triple bet':
                self.chip_mul=3

            winner = self.board.play_game_turn(self.square_number)
            self.first = not self.first

            if winner == True:
                print("Player wins!")
                self.Player_wins += 1
                self.Player_chips += self.min_bid*self.chip_mul
                self.A_chips -= self.min_bid*self.chip_mul
            elif winner == False:
                print("Ai wins!")
                self.A_wins += 1
                self.A_chips += self.min_bid*self.chip_mul
                self.Player_chips -= self.min_bid*self.chip_mul
            else:
                self.ties += 1

            if self.A_chips <= 0 or self.Player_chips <= 0:
                break

        if player_choice == 'quit' or self.Player_chips <= 0:
            print("Player is no longer playing")

        else:
            print("Play again? 1 for yes, 0 for no")
            again = -1
            while again < 0 or again > 1:
                again = int(input())
            if again == 1:
                self.play_pair()
            return


    def league_choice(self, first, AI_choice = ''):
        choice_list = self.available_actions(first)
        p_input = -1
        print("You currently have", self.Player_chips, "chips and", self.Player_wins, "wins.")
        if AI_choice:
            print("Opponent chose", AI_choice)
        print('Select Bet 1, Bet 2, or Bet 3:')
        for i, choice in enumerate(choice_list):
            print(i, choice)
        while p_input < 0 or p_input > len(choice_list):
            p_input = self.kivy_obj.player_bet_amount
        return choice_list[p_input]
