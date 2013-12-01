import os


def repl_root(path):
    return path.replace('$ROOT', os.getcwd())
