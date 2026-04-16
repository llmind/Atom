import base64
from openai import OpenAI
# Set OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "http://192.168.71.16:14318/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

#prompt = """
#Write a bash script that takes a matrix represented as a string with
#format '[1,2],[3,4],[5,6]' and prints the transpose in the same format.
#"""
prompt = """
识别题干，输出latex代码
"""
base64_image = encode_image("testOCR.png")

response = client.chat.completions.create(
    model="/media/hdd/data01/llm/gemma-4-31B-IT",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_image}"}
                },
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        }
    ],
)
print(response)
