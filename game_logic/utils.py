import os, sys

def get_path(original_path):
    if hasattr(sys, '_MEIPASS'):
        executable_path = os.path.join(sys._MEIPASS)
        new_path = os.path.join(executable_path, original_path)
    else:
        new_path = original_path
    return new_path