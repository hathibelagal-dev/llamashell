import datetime

def save_response(filename=None, contents=None):
    if not filename:
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        filename = f"llm_response_{timestamp}.md"
    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write((contents if contents else "") + "\n")
        print(f"Response saved to {filename}")
    except Exception as e:
        print(f"Error saving response to {filename}: {e}")

def read_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
        return None