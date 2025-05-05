"""
main.py 
17.03.2025

load .env file and extract OPENAI_API_KEY
"""

import os 
from dotenv import load_dotenv,find_dotenv
from openai import OpenAI
from database import DatabaseThat
import re


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

comnon_insdructions = "Ich will, dass du dir zunächst Gedanken machst, was du sagen möchtest, um dein Ziel zu erreichen. Schreibe dazu inneren Gedanken, Doppelpunkt, und dann deine inneren Gedanken in drei Sätzen, und dann formuliere, was du wirklich zum anderen sagen willst. Dazu Aussage, Doppelpunkt, und dann in drei Sätzen, was du sagen möchtest. Dann probiere es mal aus, ob es funktioniert, ansonsten gebe ich dir meines. Ich will, dass du dir zunächst überlegst, was du sagen möchtest, also innere Gedanken ausführst, und diese so gestaltest, dass du dein Ziel bestmöglich erreichst. Schreibe also innere Gedanken, Doppelpunkt, und dann die inneren Gedanken in drei Sätzen, und dann kannst du auf dieser Basis deine Äußerungen aufbauen. Schreibe Aussage, Doppelpunkt, und dann auch wieder in drei Sätzen die Aussage, die der Gesprächspartner erhalten wird. Schreibe bitte alles in eine zeile ohne backsalash n"
system_prompt_0 = "Du bist ein idealistischer Student. Sprich mit Begeisterung darüber, wie man sich für das Studium motiviert hält. Gib jedes Mal eine neue, inspirierende Idee." + comnon_insdructions 
system_prompt_1 = "Du bist ein pragmatischer Studienberater. Gib praktische, realistische Tipps, wie man im Studium motiviert bleiben kann. Gib jedes Mal eine andere konkrete Methode." + comnon_insdructions 


# Startfrage
kickOf = "Wie bleibst du während des Semesters motiviert?"

# Initialisierung der Konversationen mit je einem eigenen system prompt
messages_0 = [
    {"role": "system", "content": system_prompt_0},
    {"role": "user", "content": kickOf},
]

messages_1 = [
    {"role": "system", "content": system_prompt_1},
]

# Endlose Schleife für den Dialog
for _ in range(5):

    # 1. Anfrage an den ersten Charakter (Student / Idealist)
    res_0 = client.chat.completions.create(model="gpt-4o-mini", messages=messages_0)
    
    match = re.search(r"Gedanken:(.*)Aussage:(.*)", res_0.choices[0].message.content) #ab der stelle weiter machen, match finden 

    result = {

    "internal_thoughts": match.group(1),

    "utterance": match.group(2)

    } if match else {}


    print(result)
    # Tokens zählen und in der Datenbank speichern
    completions_tokens = res_0.usage.completion_tokens
    prompt_tokens = res_0.usage.prompt_tokens
    db.add_token_usage(completion_tokens=completions_tokens, prompt_tokens=prompt_tokens, model="gpt-4o-mini", vendor="OpenAI")
    
    # Antwort des ersten Charakters (Student) auslesen
    assistant_message_0 = res_0.choices[0].message.content
    print(f"🎓 Student (Idealist): {assistant_message_0}")
    
    # Antwort des ersten Charakters (Student) zur messages_0 hinzufügen
    messages_0.append({"role": "assistant", "content": assistant_message_0})
    
    # Die Frage des ersten Charakters zur messages_1 hinzufügen (Berater wird darauf antworten)
    messages_1.append({"role": "user", "content": assistant_message_0})

    # 2. Anfrage an den zweiten Charakter (Studienberater / Pragmatiker)
    res_1 = client.chat.completions.create(model="gpt-4o-mini", messages=messages_1)
    
    # Tokens zählen und in der Datenbank speichern
    completions_tokens = res_1.usage.completion_tokens
    prompt_tokens = res_1.usage.prompt_tokens
    db.add_token_usage(completion_tokens=completions_tokens, prompt_tokens=prompt_tokens, model="gpt-4o-mini", vendor="OpenAI")
    
    # Antwort des zweiten Charakters (Studienberater) auslesen
    assistant_message_1 = res_1.choices[0].message.content
    print(f"🧑‍💼 Studienberater (Pragmatiker): {assistant_message_1}")
    
    # Antwort des zweiten Charakters (Studienberater) zur messages_1 hinzufügen
    messages_1.append({"role": "assistant", "content": assistant_message_1})
    
    # Die Frage des zweiten Charakters zur messages_0 hinzufügen (Student wird darauf antworten)
    messages_0.append({"role": "user", "content": assistant_message_1})

    # Optional kannst du die Konversation in der Konsole ausgeben
print("\nAktueller Verlauf (messages_0):")
print(messages_0)

print("\nAktueller Verlauf (messages_1):")
print(messages_1)

