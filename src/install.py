from tools import link_launcher, link_process, PARENT_DIR

import subprocess
import sys
import os

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

dependencies = [
    "colr",
    "pyfiglet",
    "questionary",
]

for package in dependencies: install(package)
print("All dependencies have been installed successfully.")

# print("Creating JSON file...")
# if not os.path.exists(PARENT_DIR + "valedict_data.json"):
#     open(PARENT_DIR + "valedict_data.json", "w")

print("Creating shortcuts...")
link_launcher(True)
link_process()
print("Done.")

input()