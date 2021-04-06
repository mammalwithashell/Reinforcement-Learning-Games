from kivy.uix.screenmanager import Screen

class TicTacToeScreen(Screen):
    def load_settings(self, diff, match):

        self.difficulty_setting = diff
        self.match = match
        
        if self.match == "Single Match":
            pass
        else:
            self.first_league_run = True
            league = LeagueEnvironment(self.board_env, self)

            player_names = []
            board_agents = []
            league_agents = []

            player_names.append('learning strategy and tactics')
            board_agents.append(Agent(self.board_env, select_difficulty(True), 'max'))
            league_agents.append(Agent(league, 'game_logic/tictactoeAI/qtables/league.txt', 'max'))

            player_names.append('learning tactics only')
            board_agents.append(Agent(self.board_env, select_difficulty(True), 'max'))
            league_agents.append(Agent(league, 'game_logic/tictactoeAI/qtables/league.txt', 'random'))

            player_names.append('learning strategy only')
            board_agents.append(Agent(self.board_env, select_difficulty(True), 'random'))
            league_agents.append(Agent(league, 'game_logic/tictactoeAI/qtables/league.txt', 'max'))

            player_names.append('no learning')
            board_agents.append(Agent(self.board_env, select_difficulty(True), 'random'))
            league_agents.append(Agent(league, 'game_logic/tictactoeAI/qtables/league.txt', 'random'))

            league.set_players(player_names, league_agents, board_agents)


#----------------------------------------------------------------------------------------------------------
    def press_main(self):
        quit()
    def press_exit(self):
        quit()
    
    def press1(self):
        self.square_number = 1
        if (self.square_number not in self.buttonlist):
            self.alternate_turn()
            if self.turn == 0:
                self.square1.text = 'X'
                self.square1.color = [0, 1, 0, 1]
                #https://www.december.com/html/spec/colorrgbadec.html
                self.buttonlist.append(1)
            else:
                self.square1.text = 'O'
                self.square1.color = [0, 1, 1, 1]
                self.buttonlist.append(1)
    
    def press2(self):
        self.square_number = 2
        if (self.square_number not in self.buttonlist):
            self.alternate_turn()
            if self.turn == 0:
                self.square2.text = 'X'
                self.square2.color = [0, 1, 0, 1]
                self.buttonlist.append(2)
            else:
                self.square2.text = 'O'
                self.square2.color = [0, 1, 1, 1]
                self.buttonlist.append(2)
    
    def press3(self):
        self.square_number = 3
        if (self.square_number not in self.buttonlist):
            self.alternate_turn()
            if self.turn == 0:
                self.square3.text = 'X'
                self.square3.color = [0, 1, 0, 1]
            else:
                self.square3.text = 'O'
                self.square3.color = [0, 1, 1, 1]

            self.buttonlist.append(3)
    
    def press4(self):
        self.square_number = 4
        if (self.square_number not in self.buttonlist):
            self.alternate_turn()
            if self.turn == 0:
                self.square4.text = 'X'
                self.square4.color = [0, 1, 0, 1]
            else:
                self.square4.text = 'O'
                self.square4.color = [0, 1, 1, 1]

            self.buttonlist.append(4)
    
    def press5(self):
        self.square_number = 5
        if (self.square_number not in self.buttonlist):
            self.alternate_turn()
            if self.turn == 0:
                self.square5.text = 'X'
                self.square5.color = [0, 1, 0, 1]
                self.buttonlist.append(5)
            else:
                self.square5.text = 'O'
                self.square5.color = [0, 1, 1, 1]
                self.buttonlist.append(5)

    def press6(self):
        self.square_number = 6
        if (self.square_number not in self.buttonlist):
            self.alternate_turn()
            if self.turn == 0:
                self.square6.text = 'X'
                self.square6.color = [0, 1, 0, 1]
                self.buttonlist.append(6)
            else:
                self.square6.text = 'O'
                self.square6.color = [0, 1, 1, 1]
                self.buttonlist.append(6)
    
    def press7(self):
        self.square_number = 7
        if (self.square_number not in self.buttonlist):
            self.alternate_turn()
            if self.turn == 0:
                self.square7.text = 'X'
                self.square7.color = [0, 1, 0, 1]
                self.buttonlist.append(7)
            else:
                self.square7.text = 'O'
                self.square7.color = [0, 1, 1, 1]
                self.buttonlist.append(7)
    
    def press8(self):
        self.square_number = 8
        if (self.square_number not in self.buttonlist):
            self.alternate_turn()
            if self.turn == 0:
                self.square8.text = 'X'
                self.square8.color = [0, 1, 0, 1]
                self.buttonlist.append(8)
            else:
                self.square8.text = 'O'
                self.square8.color = [0, 1, 1, 1]
                self.buttonlist.append(8)
    
    def press9(self):
        self.square_number = 9
        if (self.square_number not in self.buttonlist):
            self.alternate_turn()
            if self.turn == 0:
                self.square9.text = 'X'
                self.square9.color = [0, 1, 0, 1]
                self.buttonlist.append(9)
            else:
                self.square9.text = 'O'
                self.square9.color = [0, 1, 1, 1]
                self.buttonlist.append(9)
    
    def secondlast(self):
        pass
    
    def menu(self):
        self.manager.current = "title"