import os
os.environ["NO_PROXY"] = "localhost,127.0.0.1,192.168.*"

from openai import OpenAI
# Set OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "http://192.168.71.16:14268/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

prompt = """
钢铁是怎样炼成的是一部著名的小说，请给我生成此书的概要，包括主要任务和故事情节，大约500字左右
"""
with client.responses.create(
    model="/media/hdd/data01/llm/gemma-4-26B-A4B-IT",
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
