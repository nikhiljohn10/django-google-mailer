from sys import path as pathlist
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
pathlist.append(str(BASE_DIR))

from gmailer import __version__
print(__version__)
