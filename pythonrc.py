import rlcompleter, readline
readline.parse_and_bind("tab: complete")
# readline.set_completer(rlcompleter.Completer(locals()).complete)

# Import general utilities
from rich import *
import platform
import sys
from os.path import expanduser
print("Python...", end=" ")
print(f"{sys.version}", end=" ")
print(f"on {platform.platform()}", end=" ")
print(f"by {expanduser('~')}", end=" ")
print(";-)")




