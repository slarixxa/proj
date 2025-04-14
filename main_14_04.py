"""
main.py 
14.04.2025

load file OPENAI_API_KEY
"""


import os 
from dotenv import load_dotenv,find_dotenv
from openai import OpenAI
from database import DatabaseThat


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


#Parameters
QUESTIONS = "What is the capital of Spain?"
SYSTEM_PROMPT = "You are a helpful assistant that can answer questions in exactly two sentences. Answer in German"

MODEL = "gpt-4o-mini"

load_dotenv(find_dotenv(), override=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
db = DatabaseThat("token_usage.db")
db.open_database()

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": QUESTIONS}
]

res = client.chat.completions.create(model=MODEL, messages=messages)
completions_tokens = res.usage.completion_tokens
prompt_tokens = res.usage.prompt_tokens
db.add_token_usage(completion_tokens=completions_tokens, prompt_tokens=prompt_tokens, model=MODEL, vendor="OpenAI")
print(res.choices[0].message.content)

messages.append({"role" : "assistant", "content" : res.choices[0].message.content})
messages.append({"role" : "user", "content" : "wie viele leben dort?"})
res = client.chat.completions.create(model=MODEL, messages=messages)
completions_tokens = res.usage.completion_tokens
prompt_tokens = res.usage.prompt_tokens
db.add_token_usage(completion_tokens=completions_tokens, prompt_tokens=prompt_tokens, model=MODEL, vendor="OpenAI")
print(res.choices[0].message.content)
print("Done")