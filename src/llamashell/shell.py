import os
import subprocess
import shlex
import sys
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.styles import Style
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
        if not cmd:
            continue
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
        if cmd_args:
            parsed_commands.append({
                "args": cmd_args,
                "input_file": input_file,
                "output_file": output_file,
                "append_file": append_file
            })
    
    return parsed_commands

def execute_command(command, stdin=None, stdout=subprocess.PIPE):
    args = command["args"]
    input_file = command["input_file"]
    output_file = command["output_file"]
    append_file = command["append_file"]

    if not args:
        return True

    if args[0] in ["exit", "quit", "bye"]:
        return False
    elif args[0] == "cd":
        try:
            target = args[1] if len(args) > 1 else os.path.expanduser("~")
            if not target:
                print(f"{RED}cd: missing directory{RESET}")
                return True
            os.chdir(target)
            return True
        except Exception as e:
            print(f"{RED}cd: {e}{RESET}")
            return True

    interactive_commands = ["vi", "vim", "ps", "top", "less", "nano", "more", "python", "python3"]
    if args[0] in interactive_commands:
        if input_file or output_file or append_file or stdin:
            print(f"{RED}Interactive commands cannot use redirection or pipes{RESET}")
            return True
        try:
            subprocess.run(args, check=True)
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

    stdin_file = stdin if stdin else (open(input_file, "r") if input_file else None)
    stdout_file = open(output_file, "w") if output_file else open(append_file, "a") if append_file else stdout

    try:
        process = subprocess.Popen(
            args,
            stdin=stdin_file,
            stdout=stdout_file,
            stderr=subprocess.PIPE,
            text=True
        )
        return process
    except FileNotFoundError:
        print(f"{RED}{args[0]}: command not found{RESET}")
        return None
    except subprocess.CalledProcessError as e:
        print(f"{RED}Error: {e}{RESET}")
        return None
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
        return None
    finally:
        if input_file and stdin_file:
            stdin_file.close()
        if (output_file or append_file) and stdout_file != subprocess.PIPE:
            stdout_file.close()

def execute_pipeline(commands):
    if not commands:
        return True

    processes = []
    last_process = None

    for i, cmd in enumerate(commands):
        stdin = last_process.stdout if last_process else None
        stdout = subprocess.PIPE if i < len(commands) - 1 else None
        result = execute_command(cmd, stdin=stdin, stdout=stdout)
        if result is False:
            return False
        elif result is True:
            continue
        elif result is None:
            for p in processes:
                if p.stdout:
                    p.stdout.close()
            return True
        processes.append(result)
        last_process = result

    if processes:
        stdout, stderr = processes[-1].communicate()
        if stdout:
            print(stdout, end="")
        if stderr:
            print(f"{RED}{stderr}{RESET}", end="")

        for p in processes:
            if p.stdout:
                p.stdout.close()

    return True

def main_loop():
    show_welcome()
    style = Style.from_dict({
        'prompt': 'bold #00cccc'
    })
    session = PromptSession(
        history=InMemoryHistory(),
        style=style,
        message=lambda: [('class:prompt', f'{os.getcwd()}> ')]
    )

    while True:
        try:
            user_input = session.prompt().strip()
            if not user_input:
                continue

            commands = parse_input(user_input)
            if not commands:
                continue
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