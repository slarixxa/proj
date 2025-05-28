import os 
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
from database import DatabaseThat
import re

from pydantic import BaseModel
import instructor


# .env laden
load_dotenv(find_dotenv(), override=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")



# OpenAI Client
client = instructor.from_openai(OpenAI(api_key=OPENAI_API_KEY))
db = DatabaseThat("token_usage.db")
db.open_database()

# Modell & System-Prompts
MODEL = "gpt-4o-mini"
CONVERSATION_TURNS = 5
KICKOFF = "Wie kannst du dein Studium durchziehen?"

common_instructions = (
    "Gib deine Antwort ausschließlich in XML Format zurück, ohne zusätzliche Erklärungen oder Umbrüche: "
    "<inner_thoughts>...</inner_thoughts><utterance>...</utterance>. "
    "Schreibe genau drei vollständige Sätze innerhalb von <innerer> und drei Sätze in <aeuserer>. "
    "Verwende keine Zeilenumbrüche, keine zusätzlichen Satzzeichen außerhalb der Tags und keine Einleitung oder Erklärung."
)

system_prompt_0 = (
    "Du bist ein männlicher Student, der Elektrotechnik studiert. Du liebst dein Studium leidenschaftlich und hältst es für das einzige seriöse Fach. "
    "Du verachtest Mode, Kunst oder andere 'weichere' Studiengänge und findest sie unnütz, sagst das aber nicht laut. "
    "Trotzdem bist du heimlich verknallt in eine Studentin, die Modedesign studiert – du schwärmst insgeheim von ihrem Aussehen, bist aber wütend auf dich selbst dafür. "
    "Sprich in der äußeren Äußerung stets höflich, respektvoll oder sogar bewundernd, obwohl du innerlich etwas völlig anderes denkst. Sprich bitte leicht und in leichten Worten "
    + common_instructions
)
system_prompt_1 = (
    "Du bist eine weibliche Studentin, die Modedesign studiert. Du liebst Mode und hasst technische Studiengänge wie Elektrotechnik – du findest sie langweilig, hässlich und überflüssig. "
    "Du willst dich damit nicht beschäftigen, findest Leute, die sowas studieren, lächerlich. Dennoch versuchst du, nach außen hin freundlich oder ironisch nett zu wirken – auf eine spitze, aber nicht offen beleidigende Art. Sprich bitte leicht und in leichten Worten. "
    "In deinen inneren Gedanken lässt du aber deinem Frust und deinem Urteil komplett freien Lauf. "
    + common_instructions
)
# Nachrichteninitialisierung
messages_0 = [{"role": "system", "content": system_prompt_0}, {"role": "user", "content": KICKOFF}]
messages_1 = [{"role": "system", "content": system_prompt_1}]

# Funktion zur Extraktion strukturierter Antwort
def parse_xml_response(response_text: str):
    match = re.search(r"<inner_thoughts>(.*?)</inner_thoughts>\s*<utterance>(.*?)</utterance>", response_text, re.DOTALL)
    if match:
        return {
            "inner_thoughts": match.group(1).strip(),
            "utterance": match.group(2).strip()
        }
    return {
        "inner_thoughts": "⚠️ Keine inneren Gedanken erkannt.",
        "utterance": "⚠️ Keine Aussage erkannt."
    }


class ThoughtUtterance(BaseModel):
    inner_thoughts: str
    utterance: str

# Hauptschleife der Konversation
for i in range(CONVERSATION_TURNS):
    print(f"\n🔁 Runde {i + 1}")

    # === Agent 0 ===
    res_0 = client.chat.completions.create(model=MODEL, messages=messages_0, response_model=ThoughtUtterance) 
    result_0 = res_0

    print(f"\n🎓 Student (Idealist):")
    print(f"🧠 Innerer Gedanke: {result_0.inner_thoughts}")
    print(f"💬 Äußerung: {result_0.utterance}") 

    # Token zählen
    db.add_token_usage(
        completion_tokens=res_0.usage.completion_tokens,
        prompt_tokens=res_0.usage.prompt_tokens,
        model=MODEL,
        vendor="OpenAI"
    )

    # Nachrichten aktualisieren
    messages_0.append({"role": "assistant", "content": content_0})
    messages_1.append({"role": "user", "content": result_0["utterance"]})

    # === Agent 1 ===
    res_1 = client.chat.completions.create(model=MODEL, messages=messages_1)
    content_1 = res_1.choices[0].message.content
    result_1 = parse_xml_response(content_1)


    print(f"\n🧑‍🎓 Studentin (Pragmatikerin):")
    print(f"🧠 Innerer Gedanke: {result_1['inner_thoughts']}")
    print(f"💬 Äußerung: {result_1['utterance']}")

    # Token zählen
    db.add_token_usage(

        completion_tokens=res_1.usage.completion_tokens,
        prompt_tokens=res_1.usage.prompt_tokens,
        model=MODEL,
        vendor="OpenAI"
    )

    # Nachrichten aktualisieren
    messages_1.append({"role": "assistant", "content": content_1})
    messages_0.append({"role": "user", "content": result_1["utterance"]})

# Gesprächsverlauf ausgeben (optional)
print("\n📜 Verlauf Student:")
for m in messages_0:
    print(m)

print("\n📜 Verlauf Studentin:")
for m in messages_1:
    print(m)
