import sys
from pathlib import Path

somepath = sys.argv[1]
my_file = Path(f"{somepath}SYSTEM.PRP")
if Path(f"{somepath}SYSTEM.PRP").is_file():
    print(my_file)
