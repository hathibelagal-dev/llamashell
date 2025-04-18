# llamashell
 **llamashell** is a powerful shell that's powered by a locally running LLM. We have tested it with Llama 3.2, Qwen 2.5, and Gemma 3.

## Features

- **Interactive Shell**: Execute standard shell commands like `cd`, `ls`, and more, with support for pipes (`|`), input redirection (`<`), and output redirection (`>` or `>>`).
- **LLM Integration**: Interact with an LLM (default: `meta-llama/Llama-3.2-1B-Instruct`) for assistance using the `--` prefix (e.g., `-- write me an inspirational quote`).
- **Command History**: Persistent command history stored in `~/.llamashell_history`.
- **Chat Log Management**: Save and view LLM conversation logs with commands like `--save-chat-logs` and `--view-chat-logs`.
- **File Operations**: Read files into the LLM context with `--read <filename>` and save individual LLM responses with `--save <filename>`.
- **Auto-Completion**: Basic command and file auto-completion for a smoother user experience.
- **Cross-Platform**: Supports GPU acceleration (CUDA/MPS) and CPU fallback for broad compatibility.

## Installation

```bash
pip3 install llamashell
```

### Prerequisites
- Python 3.11+
- Linux or MacOS

## Usage

```bash
llamashell
```

You can provide any instruct LLM you can find on hugging face. For example:

```bash
llamashell --model "Qwen/Qwen2.5-0.5B-Instruct"
```

or

```bash
llamashell --model "google/gemma-3-1b-it"
```

### Special Commands

- `-- <message>`: Send a message to the LLM.
- `--save-chat-logs`: Save the entire LLM conversation to a file.
- `--save [filename]`: Save the last LLM response to a file.
- `--view-chat-logs`: Display the LLM conversation history.
- `--read <filename>`: Read a file and add its contents to the LLM context.
- `--clear`: Reset the LLM chat session.
- `history`: Show the shell command history.
- `exit`, `quit`, `bye`: Exit the shell.
