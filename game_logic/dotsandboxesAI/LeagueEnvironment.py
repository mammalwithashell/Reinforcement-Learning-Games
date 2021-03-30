import random as rand

class LeagueEnvironment:
    def __init__(self, board_environment, parent):
        # saving kivy screen object and board environment
        self.kivy_obj = parent
        self.board = board_environment

    def set_players(self, player_names, league_agents, board_agents):
        self.player_names = player_names
        self.league_agents = league_agents
        self.board_agents = board_agents
        assert(len(player_names) == len(league_agents) == len(board_agents) )
        self.num_players = len(player_names)

    def reset_pair(self):
        # getting random index value in range of agent lists
        player_indices = list(range(self.num_players))
        self.Ai = rand.choice(player_indices)

        # getting agents corresponding to random index value
        self.board.set_players(self.board_agents[self.Ai])
        self.league_agents[self.Ai].reset_past()

        # setting initial conditions for betting
        self.AI_wins = 0
        self.AI_lines = 100
        self.Player_wins = 0
        self.Player_lines = 100
        self.ties = 0
        self.state_perspective = 'A'
        self.line_mul = 1
        self.min_bid = 5
        self.game_counter = 1

        # Getting the Game States
    
    def get_state(self):
        return (self.AI_lines, self.AI_wins, self.ties, self.Player_lines, self.Player_wins, self.player_names[self.Ai], 'learning strategy and tactics')

    
    
