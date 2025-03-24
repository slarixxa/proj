"""
main.py 
17.03.2025

load .env file and extract OPENAI_API_KEY
"""

import os 
from dotenv import load_dotenv,find_dotenv
from openai import OpenAI


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


#Parameters
QUESTIONS = "What is the capital of Spain?"
SYSTEM_PROMPT = "You are a helpful assistant that can answer questions in exactly two sentences. Answer in German"

MODEL = "gpt-4o-mini"

load_dotenv(find_dotenv(), override=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": QUESTIONS}
]

print(messages)
print("Done")

res = client.chat.completions.create(model=MODEL, messages=messages)
print(res)
print(res.choices[0].message.content)

print("Done")
