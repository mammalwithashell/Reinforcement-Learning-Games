import os, sys

def get_path(original_path):
    if not hasattr(sys, '_MEIPASS'):
        return original_path
    executable_path = os.path.join(sys._MEIPASS)
    return os.path.join(executable_path, original_path)