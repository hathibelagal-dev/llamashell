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
    if "|" in user_input:
        commands = [shlex.split(cmd.strip()) for cmd in user_input.split("|")]
    else:
        commands = [shlex.split(user_input)]
    
    parsed_commands = []
    for cmd in commands:
        input_file = output_file = append_file = None
        cmd_args = []
        i = 0
        while i < len(cmd):
            if cmd[i] == "<":
                if i + 1 < len(cmd):
                    input_file = cmd[i + 1]
                    i += 2
                else:
                    raise ValueError("Missing input file after '<'")
            elif cmd[i] == ">":
                if i + 1 < len(cmd):
                    output_file = cmd[i + 1]
                    i += 2
                else:
                    raise ValueError("Missing output file after '>'")
            elif cmd[i] == ">>":
                if i + 1 < len(cmd):
                    append_file = cmd[i + 1]
                    i += 2
                else:
                    raise ValueError("Missing output file after '>>'")
            else:
                cmd_args.append(cmd[i])
                i += 1
        parsed_commands.append({
            "args": cmd_args,
            "input_file": input_file,
            "output_file": output_file,
            "append_file": append_file
        })
    
    return parsed_commands

def execute_command(command, stdin=None):
    args = command["args"]
    input_file = command["input_file"]
    output_file = command["output_file"]
    append_file = command["append_file"]

    if args and args[0] in ["exit", "quit", "bye"]:
        return False
    elif args and args[0] == "cd":
        try:
            os.chdir(args[1] if len(args) > 1 else os.path.expanduser("~"))
        except Exception as e:
            print(f"{RED}cd: {e}{RESET}")
        return True

    stdin_file = stdin if stdin else (open(input_file, "r") if input_file else subprocess.PIPE)
    stdout_file = open(output_file, "w") if output_file else open(append_file, "a") if append_file else subprocess.PIPE

    try:
        process = subprocess.Popen(
            args,
            stdin=stdin_file,
            stdout=stdout_file,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()
        if stderr:
            print(f"{RED}{stderr}{RESET}", end="")
        if stdout and stdout_file == subprocess.PIPE:
            print(stdout, end="")
        return True
    except FileNotFoundError:
        print(f"{RED}{args[0]}: command not found{RESET}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{RED}Error: {e}{RESET}")
        return True
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
        return True
    finally:
        if input_file and stdin_file != subprocess.PIPE:
            stdin_file.close()
        if (output_file or append_file) and stdout_file != subprocess.PIPE:
            stdout_file.close()

def execute_pipeline(commands):
    processes = []
    last_stdout = None

    for i, cmd in enumerate(commands):
        stdin = last_stdout if i > 0 else None
        result = execute_command(cmd, stdin=stdin)
        if result is False:
            return False
        if last_stdout and last_stdout != subprocess.PIPE:
            last_stdout.close()
        last_stdout = subprocess.PIPE

    return True

def main_loop():
    show_welcome()
    while True:
        prompt = f"{BOLD}{CYAN}{os.getcwd()}> {RESET}"
        print(prompt, end="", flush=True)
        
        try:
            user_input = input().strip()
            if not user_input:
                continue

            commands = parse_input(user_input)
            if not execute_pipeline(commands):
                break
        except ValueError as e:
            print(f"{RED}Error: {e}{RESET}")
        except KeyboardInterrupt:
            print(f"{RED}^C{RESET}")
        except EOFError:
            break
        except Exception as e:
            print(f"{RED}Unexpected error: {e}{RESET}")

    print("Goodbye!")