import os
import json
import time
from groq import Groq

client = Groq(
    api_key=os.environ.get("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"),
)

def get_response(prompt):
    time_sent = int(time.time())
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="gemma-7b-it",
    )
    time_recvd = int(time.time())
    message = chat_completion.choices[0].message.content
    
    return {
        "Prompt": prompt,
        "Message": message,
        "TimeSent": time_sent,
        "TimeRecvd": time_recvd,
        "Source": "Gemma-7b"
    }


with open("input.txt", "r") as file:
    prompts = file.readlines()


results = []


for prompt in prompts:
    result = get_response(prompt)
    results.append(result)


with open("output.json", "w") as f:
    json.dump(results, f, indent=4)

