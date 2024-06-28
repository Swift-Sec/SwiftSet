import os
from core.nmap import *
import sys
import argparse

def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

clear_screen()
print(
    """
   ____       _ _____    ____    __ 
  / __/    __(_) _/ /_  / __/__ / /_
 _\ \| |/|/ / / _/ __/ _\ \/ -_) __/
/___/|__,__/_/_/ \__/ /___/\__/\__/ 
                                    
    """
)

parser = argparse.ArgumentParser()
parser.add_argument('--url', help='URL / Domain you ant to scan')
parser.add_argument('--version', help='View the version of Swift Set')
parser.add_argument('--view_scans', help='View all scans currently installed')
parser.add_argument('--view_core', help='View all core scans currently installed')
parser.add_argument('--headers', help='Specify headers file for all requests')
parser.add_argument('--cookies', help='Specify cookies file for all requests')
parser.add_argument('--all_scans', help='Run all available scans')
parser.add_argument('--core_scans', help='Run all available core scans')
parser.add_argument('--specific_scans', help='Run some specific scans (comma seperated)')


args = parser.parse_args()

