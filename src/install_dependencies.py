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
