"""
main.py 
17.03.2025

load .env file and extract OPENAI_API_KEY
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

print(messages)
print("Done")

res = client.chat.completions.create(model=MODEL, messages=messages)
print(res)
print(res.choices[0].message.content)
print(f"Input Token: {res.usage.prompt_tokens}, Output Token: {res.usage.completion_tokens}")

completions_tokens = res.usage.completion_tokens
prompt_tokens = res.usage.prompt_tokens

db.add_token_usage(completion_tokens=completions_tokens, prompt_tokens=prompt_tokens, model=MODEL, vendor="OpenAI")

print(messages.append({"role" : "system", "content" : res.choices[0].message.content}))
print(messages.append({"role": "user", "content" : "and of germany?"}))


messages.append({"role": "assistant", "content": 
print(res.choices[0].message.content)})
print("Done")

# Der erste "Kickoff" Satz für das Gespräch
kickOf = "Sag hallo und frag wie es mir geht"

# Initialisierung der messages_0
messages_0 = [
    {"role": "system", "content": "antworte kurz und immer mit einer nachfrage, damit das gespräch"},
    {"role": "user", "content": kickOf},
]

# Initialisierung der messages_1
messages_1 = [
    {"role": "system", "content": "antworte kurz und immer mit einer nachfrage, damit das gespräch"},
]

# Endlose Schleife für den Dialog
for _ in range(5):
    # Anfrage an OpenAI (holen sich die Antwort)
    res = client.chat.completions.create(model="gpt-4o-mini", messages=messages_0)
    
    # Tokens zählen und in der Datenbank speichern
    completions_tokens = res.usage.completion_tokens
    prompt_tokens = res.usage.prompt_tokens
    db.add_token_usage(completion_tokens=completions_tokens, prompt_tokens=prompt_tokens, model="gpt-4o-mini", vendor="OpenAI")
    
    # Antwort des Assistenten auslesen
    assistant_message = res.choices[0].message.content
    print(f"Assistant: {assistant_message}")
    
    # Antwort des Assistenten zur messages_0 hinzufügen
    messages_0.append({"role": "assistant", "content": assistant_message})
    
   
    
    # Die Frage des Users zur messages_1 hinzufügen (für die Fortsetzung der Konversation)
    messages_1.append({"role": "user", "content": assistant_message})
    

    res = client.chat.completions.create(model="gpt-4o-mini", messages=messages_1)
    assistant_message = res.choices[0].message.content
    # Tokens zählen und in der Datenbank speichern
    completions_tokens = res.usage.completion_tokens
    prompt_tokens = res.usage.prompt_tokens
    db.add_token_usage(completion_tokens=completions_tokens, prompt_tokens=prompt_tokens, model="gpt-4o-mini", vendor="OpenAI")

    messages_1.append({"role": "assistant", "content": assistant_message})

    messages_0.append({"role": "user", "content": assistant_message})

    # Optional kannst du die Konversation in der Konsole ausgeben
    print("Aktueller Verlauf (messages_0):")
    print(messages_0)
    
    print("Aktueller Verlauf (messages_1):")
    print(messages_1)

