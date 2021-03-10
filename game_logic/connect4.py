from kivy.uix.screenmanager import ScreenManager, Screen

class Connect4Screen(Screen):
    def load_settings(self, diff, match):
        pass
    
    def menu(self):
        self.manager.current = "title"