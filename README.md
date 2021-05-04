# Reinforcement Learning Games

![Title Screen](https://github.com/mammalwithashell/WJNKCW/blob/main/screenshots/title_screen.png)

![Connect 4](https://github.com/mammalwithashell/WJNKCW/blob/main/screenshots/connect4.png)

![Betting League](https://github.com/mammalwithashell/WJNKCW/blob/main/screenshots/League_Betting.png)

Senior Capstone Course
Team WJNKCW

Project Structure:

The design folder has the markup files that outline the user interface

The game_logic folder houses the logic for the games and the python scripts that are responsible for the reinforcement learning game

## Getting Started

* Set up a python virtual environment
* activate the environment

```bash

 python -m venv <env_name>

```

* clone the repository

```bash

git clone https://github.com/mammalwithashell/WJNKCW.git
```

* install the requirements

```bash
pip install requirements.txt
```

* run the project

```bash
python main.py
```

## Building the project for Windows

* Install PyInstaller

```bash
pip install pyinstaller
```

* Install from reinforcement.spec

```bash
pyinstaller reinforcement.spec
```