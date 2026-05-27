import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

def get_path(filename):
    """Generates absolute pathing for your assets folder."""
    return os.path.join(BASE_PATH, filename)
