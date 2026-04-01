from pathlib import Path
from openai import OpenAI

def load_openai_key(config_path="D:\\work\\llm_configs\\openai.txt") -> str:
    text = Path(config_path).read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError("Config file is empty.")

    # Supports:
    # 1) openkey=sk-...
    # 2) OPENAI_API_KEY=sk-...
    # 3) plain key only: sk-...
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            k, v = line.split("=", 1)
            if k.strip().lower() in ("openkey", "openai_api_key"):
                key = v.strip().strip('"').strip("'")
                if key:
                    return key
        else:
            return line  # first non-empty, non-comment line as raw key

    raise ValueError("No API key found. Add openkey=YOUR_KEY to config.")

api_key = load_openai_key("D:\\work\\llm_configs\\openai.txt")
client = OpenAI(api_key=api_key)
prompt = """
Write a bash script that takes a matrix represented as a string with 
format '[1,2],[3,4],[5,6]' and prints the transpose in the same format.
"""
with client.responses.create(
    model="gpt-5-nano",
    reasoning={"effort": "low"},
    tools=[{"type": "web_search"}],
    input=[
        {
            "role": "user",
            "content": prompt,
        }],
    stream=True,
) as stream:
    for event in stream:
        if event.type == "response.output_text.delta":
            print(event.delta, end="", flush=True)
        elif event.type == 'response.completed':
            print("\n")