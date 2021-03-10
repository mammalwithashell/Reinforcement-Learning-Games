from kivy.uix.screenmanager import Screen

class TicTacToeScreen(Screen):
    def load_settings(self, diff, match):
        pass
    
    def menu(self):
        self.manager.current = "title"