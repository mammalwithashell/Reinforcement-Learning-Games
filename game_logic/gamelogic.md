# Game Logic

This folder has the screens for each game. The logic that makes the games work is in this folder

Kivy widgets in the python code communicate with .kv files primarily with a widget's id property in the .kv file or through Property objects (StringProperty, NumericProperty, ListProperty, etc) from kivy's kivy.properties library.

A widget with an id in the .kv file will be added to the root widget's ids dictionary
A widget that is given a Property object can reference and manipulate that object in the .kv file

<https://kivy.org/doc/stable/api-kivy.uix.widget.html?highlight=ids#kivy.uix.widget.Widget.ids>

<https://kivy.org/doc/stable/api-kivy.properties.html?highlight=properties#module-kivy.properties>
