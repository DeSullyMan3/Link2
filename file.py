import sys
from pathlib import Path

somepath = sys.argv[1]
my_file = Path(f"{somepath}SYSTEM.PRP")
if my_file.is_file():
    print(my_file)
