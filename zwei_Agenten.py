import os

from openai import OpenAI

client = OpenAI(

api_key=os.getenv("OPENAI_API_KEY")

)

questions = [
"What is the capital of France?",
"How many people live there?",
]

res = client.responses.create(
    model="gpt-4o-mini",
    input=questions[0]
)

print(res.output[0].content[0].text)

response_id = res.id

res = client.responses.create(
    model="gpt-4o-mini",
    instructions="Answer as briefly as possible",
    previous_response_id=response_id,
    input=questions[1]
)

print(res.output[0].content[0].text)

# import os


from openai import OpenAI



client = OpenAI(

api_key=os.getenv("OPENAI_API_KEY")

)


questions = [

"What is the capital of France?",

"How many people live there?",

]


res = client.responses.create(

    model="gpt-4o-mini",

    input=questions[0]

)


print(res.output[0].content[0].text)


response_id = res.id


res = client.responses.create(

    model="gpt-4o-mini",

    instructions="Answer as briefly as possible",

    previous_response_id=response_id,

    input=questions[1]

)


print(res.output[0].content[0].text)


 
# Johannes Köppern
# Johannes Köppern

# 19:35

# agent_0: Käufer

# - Mund: assisstant

# - Ohren: user   


# agent_1: Verkäufer

# - Mund: assisstant

# - Ohren: user


# Allgemeint: OpenAI-Agent sagt etwas als assisant und zum ihm wird von user gesprochen
