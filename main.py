import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import random as rand
from os import system
from collections import defaultdict


class MyGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super(MyGridLayout, self).__init__(**kwargs)

        self.cols = 3
        self.rows = 5

        #add widgets
        self.backButton = Button(text='back button', font_size=20)
        self.add_widget(self.backButton)

        self.scores = Label(text='scores')
        self.add_widget(self.scores)

        self.quitButton = Button(text='quit button', font_size=20)
        self.add_widget(self.quitButton)

        self.square1 = Button(text="1", font_size=72)
        #add function to the button
        self.square1.bind(on_press=self.press1)
        self.add_widget(self.square1)

        self.square2 = Button(text="2", font_size=72)
        self.square2.bind(on_press=self.press2)
        self.add_widget(self.square2)

        self.square3 = Button(text="3", font_size=72)
        self.square3.bind(on_press=self.press3)
        self.add_widget(self.square3)

        self.square4 = Button(text="4", font_size=72)
        self.square4.bind(on_press=self.press4)
        self.add_widget(self.square4)
        
        self.square5 = Button(text="5", font_size=72)
        self.square5.bind(on_press=self.press5)
        self.add_widget(self.square5)

        self.square6 = Button(text="6", font_size=72)
        self.square6.bind(on_press=self.press6)
        self.add_widget(self.square6)

        self.square7 = Button(text="7", font_size=72)
        self.square7.bind(on_press=self.press7)
        self.add_widget(self.square7)
        
        self.square8 = Button(text="8", font_size=72)
        self.square8.bind(on_press=self.press8)
        self.add_widget(self.square8)

        self.square9 = Button(text="9", font_size=72)
        self.square9.bind(on_press=self.press9)
        self.add_widget(self.square9)

        self.blankspot = Label(text='')
        self.add_widget(self.blankspot)

        self.blankspot = Label(text='message box')
        self.add_widget(self.blankspot)

        self.blankspot = Label(text='')
        self.add_widget(self.blankspot)

        self.count = 1

    def alternate_turn(self):
        self.count = self.count + 1
        self.turn = self.count%2
    
    def press1(self, instance):
        self.alternate_turn()
        if self.turn == 0:
            self.square1.text = 'X'
        else:
            self.square1.text = 'O'
    def press2(self, instance):
        self.alternate_turn()
        if self.turn == 0:
            self.square2.text = 'X'
        else:
            self.square2.text = 'O'
    def press3(self, instance):
        self.alternate_turn()
        if self.turn == 0:
            self.square3.text = 'X'
        else:
            self.square3.text = 'O'
    def press4(self, instance):
        self.alternate_turn()
        if self.turn == 0:
            self.square4.text = 'X'
        else:
            self.square4.text = 'O'
    def press5(self, instance):
        self.alternate_turn()
        if self.turn == 0:
            self.square5.text = 'X'
        else:
            self.square5.text = 'O'
    def press6(self, instance):
        self.alternate_turn()
        if self.turn == 0:
            self.square6.text = 'X'
        else:
            self.square6.text = 'O'
    def press7(self, instance):
        self.alternate_turn()
        if self.turn == 0:
            self.square7.text = 'X'
        else:
            self.square7.text = 'O'
    def press8(self, instance):
        self.alternate_turn()
        if self.turn == 0:
            self.square8.text = 'X'
        else:
            self.square8.text = 'O'
    def press9(self, instance):
        self.alternate_turn()
        if self.turn == 0:
            self.square9.text = 'X'
        else:
            self.square9.text = 'O'
# ----------kivy--------------------------------------------------------------------------------------------------------------------------

 # ----------kivy--------------------------------------------------------------------------------------------------------------------------
class Tictactoe(App):
    def build(self):
        return MyGridLayout()

if __name__ == "__main__":
    Tictactoe().run()
# ----------kivy--------------------------------------------------------------------------------------------------------------------------

