import random as rand
from os import system

class LeagueEnvironment:
    def __init__(self, board_environment, parent):
        self.kivy_obj = parent
        self.board = board_environment    

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
        self.A_wins = 0
        self.A_chips=100
        self.Player_wins = 0
        self.Player_chips=100
        self.ties = 0
        self.state_perspective = 'A' # the state in wins/ties/losses for which player
        self.chip_mul=1
        self.min_bid=5
        self.game_counter=1

    def get_state(self):  ### how to tell who is calling get_state?
        return (self.A_chips,self.A_wins,self.ties,self.Player_chips,self.Player_wins,self.player_names[self.Ai],'learning strategy and tactics')

    def pair_games_played(self):
        return self.A_wins + self.ties + self.B_wins

    def available_actions(self, first):
        if first:
            return ['quit','single bet','double bet','triple bet']
        else:
            return ['quit','call']

    # split original play_pair function into three functions:
    # one for placing bets, one for processing bets, and one for postgame options
    #def play_pair(self):
        
    def play_pair(self, first_run):
        # only resetting league env on first run
        if first_run:
            system('clear')
            self.reset_pair()

            player_choice = ''

        # we will implement this loop somewhere else
        #while(True):

        if self.first:
            player_choice = self.league_choice(True)
            # adding this codeblock to stop AI from quitting on first round
        else:
            if first_run:
                AI_choice = "quit"
                while AI_choice == "quit":
                    AI_choice = self.league_agents[self.Ai].select_action(True)
            else:
                AI_choice = self.league_agents[self.Ai].select_action(True)
            if AI_choice != "quit":
                player_choice = self.league_choice(False, AI_choice)
            else:
                self.play_pair_pt_1_5(None, AI_choice=AI_choice)

    def play_pair_pt_1_5(self, player_choice, AI_choice=''):
        if AI_choice == '':
            AI_choice = self.league_agents[self.Ai].select_action(False)
            print("Opponent chose", AI_choice)
        if AI_choice == 'quit' or player_choice == 'quit':
            message = f'''
                {'You' if player_choice == 'quit' else 'AI'} quit\n
                You had {self.Player_chips} chips\n
                AI had {self.A_chips} chips
            '''
            self.kivy_obj.series_end(message)
            return
            #break
        elif AI_choice == 'single bet' or player_choice == 'single bet':
            self.chip_mul=1
        elif AI_choice == 'double bet' or player_choice == 'double bet':
            self.chip_mul=2
        elif AI_choice == 'triple bet' or player_choice == 'triple bet':
            self.chip_mul=3

        self.kivy_obj.user_data.text = f''' 
        User chips: {self.Player_chips}\n
        User bet: {player_choice}
        '''
        self.kivy_obj.ai_data.text = f''' 
        AI chips: {self.A_chips}\n
        AI bet: {AI_choice}
        '''

        return True

    def play_pair_pt_2(self, winner, tie=False):
        # winner is set in parameter rather than by calling "play_game here"
        self.first = not self.first

        if tie == True:
            self.ties += 1
        elif winner == True:
            print("Player wins!")
            self.Player_wins += 1
            self.Player_chips += self.min_bid*self.chip_mul
            self.A_chips -= self.min_bid*self.chip_mul
        elif winner == False:
            print("Ai wins!")
            self.A_wins += 1
            self.A_chips += self.min_bid*self.chip_mul
            self.Player_chips -= self.min_bid*self.chip_mul

        if self.A_chips <= 0 or self.Player_chips <= 0:
            # game should end here, but it is not yet implemented
            message = f'''
                {'AI' if self.A_chips <= 0 else 'You'} ran out of chips\n
                You had {self.Player_chips} chips\n
                AI had {self.A_chips} chips
            '''
            self.kivy_obj.series_end(message)
            #break
        # initially, the while loop starting in "play_pair" ended here

        # these replay options will be handled elsewhere
        '''if player_choice == 'quit' or self.Player_chips <= 0:
            print("Player is no longer playing")

        else:
            print("Play again? 1 for yes, 0 for no")
            again = -1
            while again < 0 or again > 1:
                again = int(input())
            if again == 1:
                self.play_pair()
            return'''


    def league_choice(self, first, AI_choice = ''):
        choice_list = self.available_actions(first)
        i = 0
        p_input = -1
        message = f"You currently have {self.Player_chips} chips and {self.Player_wins} {'wins' if self.Player_wins != 1 else 'win'}.\n"
        message += f"Your opponent has {self.A_wins} {'wins' if self.A_wins != 1 else 'win'}.\n"
        if AI_choice:
            message += f"Opponent chose {AI_choice}\n"
        message += '\nSelect your next move'
        bet_choice = self.kivy_obj.bet_options(choice_list, message, self.play_pair_pt_1_5, AI_choice)
        return choice_list[p_input]

        '''
        print("You currently have", self.Player_chips, "chips and", self.Player_wins, "wins.")
        if AI_choice:
            print("Opponent chose", AI_choice)
        print('Select a choice from the list:')
        for choice in choice_list:
            print(i, choice)
            i += 1
        while p_input < 0 or p_input > len(choice_list):
            p_input = int(input())
        return choice_list[p_input]
        '''


