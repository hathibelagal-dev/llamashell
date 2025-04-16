import os
import subprocess
import shlex
from . import __VERSION__

BOLD = "\033[1m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"
WHITE = "\033[37m"
CYAN = "\033[36m"
RED = "\033[31m"

def show_welcome():
    print(f"{BOLD}{YELLOW}Welcome to LLaMa Shell v{__VERSION__}{RESET}")

def parse_input(user_input):
    return shlex.split(user_input)

def execute_command(args):
    if args[0] == "exit" or args[0] == "quit" or args[0] == "bye":
        return False
    elif args[0] == "cd":
        try:
            os.chdir(args[1] if len(args) > 1 else os.path.expanduser("~"))
        except Exception as e:
            print(f"cd: {e}")
        return True

    try:
        subprocess.run(args, check=True)
    except subprocess.CalledProcessError as e:
        print(f"{RED}Error: {e}{RESET}")
    except FileNotFoundError:
        print(f"{RED}{args[0]}: command not found{RESET}")
    return True

def main_loop():
    show_welcome()
    while True:
        prompt = f"{BOLD}{CYAN}{os.getcwd()}> {RESET}"
        print(prompt, end="", flush=True)
        
        user_input = input().strip()
        if not user_input:
            continue

        args = parse_input(user_input)
        if not execute_command(args):
            break

    print("Goodbye!")