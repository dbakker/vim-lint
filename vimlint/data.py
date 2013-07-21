import os

_ROOT = os.path.abspath(os.path.dirname(__file__))


def get(path):
    return os.path.join(_ROOT, 'data', path)


def lines(path):
    with open(get(path)) as f:
        return f.readlines()
