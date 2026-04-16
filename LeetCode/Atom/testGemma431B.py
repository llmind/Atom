from openai import OpenAI
# Set OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "http://192.168.71.16:14318/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

#prompt = """
#Write a bash script that takes a matrix represented as a string with
#format '[1,2],[3,4],[5,6]' and prints the transpose in the same format.
#"""
prompt = """
告诉我三角形的角平分线有哪些性质
"""
with client.responses.create(
    model="/media/hdd/data01/llm/gemma-4-31B-IT",
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
