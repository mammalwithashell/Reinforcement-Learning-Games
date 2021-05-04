# Design Folder

The markup files for Kivy go in this folder.

Kivy uses these kv files in the same way that a browser uses html

<https://kivy.org/doc/stable/guide/lang.html>

<https://kivy.org/doc/stable/api-kivy.uix.gridlayout.html?highlight=grid%20layout#module-kivy.uix.gridlayout>

We make extensive use of the GridLayout object from kivy.gridlayout. This layout sizes and positions things differently than other kivy layouts. It automatically places children of this widget in its columns or rows. We used this to effectively recreate html's box model of placement
