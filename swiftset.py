import os
from core.nmap import *
from core.csrf import *
import sys
import argparse
import json


def clear_screen():
    if os.name == "nt":
        try:
            os.system("cls")
        except Exception as e:
            print(f"Error clearing screen --> \n{e}")
    else:
        try:
            os.system("clear")
        except Exception as e:
            print(f"Error clearing screen --> \n{e}")

def install_modules():
    try:
        os.system("python -m pip install -r requirements.txt --no-deps --ignore-installed")
    except Exception as e:
        print(f"Error installing modules --> \n{e}")

def banner():
    print("""
      ____       _ _____    ____    __ 
     / __/    __(_) _/ /_  / __/__ / /_
    _\ \| |/|/ / / _/ __/ _\ \/ -_) __/
   /___/|__,__/_/_/ \__/ /___/\__/\__/                                 
""")

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help = "URL / Domain you want to scan")
    parser.add_argument("--version", help = "View the version of Swift Set", action = "store_true")
    parser.add_argument("--verbose", help = "Set the verbosity of the scan [1-5] Default:2")
    parser.add_argument("--view_scans", help = "View all scans currently installed", action = "store_true")
    parser.add_argument("--view_core", help = "View all core scans currently installed", action = "store_true")
    parser.add_argument("--headers", help = "Specify headers file for all requests")
    parser.add_argument("--cookies", help = "Specify cookies file for all requests")
    parser.add_argument("--all_scans", help = "Run all available scans", action = "store_true")
    parser.add_argument("--core_scans", help = "Run all available core scans", action = "store_true")
    parser.add_argument("--specific_scans", help = "Run some specific scans (comma seperated)")


    return parser.parse_args()

def main():
    install_modules()
    clear_screen()
    banner()
    version = "beta-dev"
    args = parse()

    if args.version:
        print(f"CURRENT VERSION --> {version}")

    if args.view_core:
        cwd = os.getcwd()
        core_directory = os.path.join(cwd , "core")
        for item in os.listdir(core_directory):
            full_path = os.path.join(core_directory , item)
            if os.path.isfile(full_path):
                file_name = item.split(".")[0]
                extension = item.split(".")[1]
                valid_core_modules = ["crsf" , "ssrf" , "xss" , "sqli" , "secrets" , "crawler" , "fuzz" , "idor" , "nmap" , "subdomain_search"]
                core_info_file = os.path.join(core_directory , "core_info.json")
                f = open(core_info_file , "r")
                core_info = f.read()
                f.close()
                core_info = json.loads(core_info)
                
                if extension == "py" and file_name in valid_core_modules:
                    print(f"CORE MODULE : {file_name} | {core_info[file_name]["description"]}")

    if args.core_scans:
        if args.url:
            print(f"STARTING ALL CORE SCANS ON {args.url}")
            print(initialize_csrf([args.url]))
        else:
            print("No url/domain found. Please enter one with the arg --url / -u")

        
if __name__ == "__main__":
    with open("core/pdf/results.txt", "w") as f:
        f.write("#Swiftset - Pentesting made easy\n##Swift-Sec\n\n")
        f.close()
    main()