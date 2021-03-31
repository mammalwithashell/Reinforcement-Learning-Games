import random as rand

class LeagueEnvironment:
    def __init__(self, board_environment, parent):
        # saving kivy screen object and board environment
        self.kivy_obj = parent
        self.board = board_environment    

    '''
        description
            receiving and saving lists of league and board agents
        parameters
            player_names: list of names corresponding to league and board agents
            league_agents: list of league betting agents
            board_agents: list of board gameplay agents
    '''
    def set_players(self, player_names, league_agents, board_agents):
        self.player_names = player_names
        self.league_agents = league_agents
        self.board_agents = board_agents
        assert(len(player_names) == len(league_agents) == len(board_agents) )
        self.num_players = len(player_names)

    '''
        description
            randomly select 2 players and sets initial state for league play
    '''
    def reset_pair(self):
        # getting random index value in range of agent lists
        player_indices = list(range(self.num_players))
        self.Ai = rand.choice(player_indices)

        # getting agents corresponding to random index value
        self.board.set_players(self.board_agents[self.Ai])
        self.league_agents[self.Ai].reset_past()

        # setting or resetting board and saving who gets the first move
        self.first = self.board.reset()

        # setting initial conditions for betting
        self.A_wins = 0
        self.A_chips=100
        self.Player_wins = 0
        self.Player_chips=100
        self.ties = 0
        self.state_perspective = 'A' # the state in wins/ties/losses for which player
        self.chip_mul=1
        self.min_bid=5
        self.game_counter=1

    '''
        description
            function called by Agent class to get game state of LeagueEnvironment
    '''
    def get_state(self):
        return (self.A_chips,self.A_wins,self.ties,self.Player_chips,self.Player_wins,self.player_names[self.Ai],'learning strategy and tactics')

    # vestigial function
    '''def pair_games_played(self):
        return self.A_wins + self.ties + self.B_wins'''

    '''
        description
            returns list of actions available to the current player
        parameters
            first: will be true if current player goes first in this round of betting
    '''
    def available_actions(self, first):
        if first:
            return ['quit','single bet','double bet','triple bet']
        else:
            return ['quit','call']


    # context for the play_pair function set
    #   original play_pair function was split into three functions: one for placing bets, 
    #   one for processing bets, and one for postgame options
    '''
        description
            gets user betting input, and gets AI betting input if the AI goes first this round
        parameters
            first_run: on and only on the first match in a series of league play, this is True
    '''
    def play_pair(self, first_run):
        # resetting league env if 'first_run' is True
        if first_run:
            self.reset_pair()
            player_choice = ''

        # if user is first, getting user input
        if self.first:
            self.league_choice(True)
        # if AI is first, getting AI input then getting user input
        else:
            # adding this codeblock to stop AI from quitting on first round
            if first_run:
                AI_choice = "quit"
                while AI_choice == "quit":
                    AI_choice = self.league_agents[self.Ai].select_action(True)
            else:
                AI_choice = self.league_agents[self.Ai].select_action(True)
            # if AI didn't quit, getting user input here
            if AI_choice != "quit":
                self.league_choice(False, AI_choice)
            # if AI quit, skipping user input and triggering end of game
            else:
                self.play_pair_pt_1_5(None, AI_choice=AI_choice)

    '''
        description
            processes betting input and formats scoreboard info
        parameters
            player_choice: choice input by player. will contain data unless the AI
                just quit the game
            AI_choice: AI's betting choice. Will contain info if AI played first, else
                will be an empty string
    '''
    def play_pair_pt_1_5(self, player_choice, AI_choice=''):
        # getting AI's bet if AI_choice is an empty string
        if AI_choice == '':
            AI_choice = self.league_agents[self.Ai].select_action(False)
        # handling case where user or AI quit
        if AI_choice == 'quit' or player_choice == 'quit':
            message = f'''
                {'You' if player_choice == 'quit' else 'AI'} quit\n
                You had {self.Player_chips} chips\n
                AI had {self.A_chips} chips
            '''
            # calling 'series_end' in kivy screen object
            self.kivy_obj.series_end(message)
            return
        # handling case where user or AI made a bet and other player called
        elif AI_choice == 'single bet' or player_choice == 'single bet':
            self.chip_mul=1
        elif AI_choice == 'double bet' or player_choice == 'double bet':
            self.chip_mul=2
        elif AI_choice == 'triple bet' or player_choice == 'triple bet':
            self.chip_mul=3

        # formatting scoreboard data
        self.kivy_obj.user_data.text = f''' 
        User chips: {self.Player_chips}\n
        User bet: {player_choice}
        '''
        self.kivy_obj.ai_data.text = f''' 
        AI chips: {self.A_chips}\n
        AI bet: {AI_choice}
        '''

        return

    ''' 
        description
            final play_pair function; updates league series info at end of 
            match and creates end of game message
        parameters
            winner: winner of game
            tie: True if tie game
    '''
    def play_pair_pt_2(self, winner, tie=False):
        # other player gets to bet first next time
        self.first = not self.first

        # updating chip and win counts
        if tie == True:
            self.ties += 1
        elif winner == True:
            self.Player_wins += 1
            self.Player_chips += self.min_bid*self.chip_mul
            self.A_chips -= self.min_bid*self.chip_mul
        elif winner == False:
            self.A_wins += 1
            self.A_chips += self.min_bid*self.chip_mul
            self.Player_chips -= self.min_bid*self.chip_mul

        # if a player runs out of chips, end the league series
        if self.A_chips <= 0 or self.Player_chips <= 0:
            message = f'''
                {'AI' if self.A_chips <= 0 else 'You'} ran out of chips\n
                You had {self.Player_chips} chips\n
                AI had {self.A_chips} chips
            '''
            self.kivy_obj.series_end(message)

    '''
        description
            gets user betting input
        parameters
            first: True if user is first in betting process
            AI_choice: AI's move selection. Will be an empty string
                if user plays first
    '''
    def league_choice(self, first, AI_choice = ''):
        # getting actions available to user
        choice_list = self.available_actions(first)

        # creating message that will be displayed to user
        message = f"You currently have {self.Player_chips} chips and {self.Player_wins} {'wins' if self.Player_wins != 1 else 'win'}.\n"
        message += f"Your opponent has {self.A_wins} {'wins' if self.A_wins != 1 else 'win'}.\n"
        if AI_choice:
            message += f"Opponent chose {AI_choice}\n"
        message += '\nSelect your next move'

        # calling function in kivy screen object that will display popup to user and get their input
        self.kivy_obj.bet_options(choice_list, message, self.play_pair_pt_1_5, AI_choice)
        return


