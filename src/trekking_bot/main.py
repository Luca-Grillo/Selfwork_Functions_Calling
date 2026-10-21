import json
import chainlit as cl
from dotenv import load_dotenv
from openai import OpenAI

from trekking_bot.tools import TOOLS, run_tool

load_dotenv()
client = OpenAI()

MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = (
    "Sei l'assistente di 'Sentieri Aperti', un'agenzia di escursioni guidate. "
    "Rispondi in italiano, in modo breve."
    "Controlla che la data sia oltre il giorno attuale"
    "Usa i tool per info, partenze e prenotazioni: non inventare dati."
    "Per prenotare chiedi all'utente i dati mancanti (escursione, data, nome)."
)


def get_response(messages: list) -> str:
    while True:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
        )
        message = response.choices[0].message

        if not message.tool_calls:
            messages.append({"role": "assistant", "content": message.content})
            return message.content

        messages.append(message)


        for call in message.tool_calls:
            arguments = json.loads(call.function.arguments)
            print(f"[tool] {call.function.name} {arguments}")
            result = run_tool(call.function.name, arguments)
            messages.append(
                {"role": "tool", "tool_call_id": call.id, "content": result}
            )

@cl.on_chat_start
async def start():
    cl.user_session.set(
        "messages", [{"role": "system", "content": SYSTEM_PROMPT}]
    )
    await cl.Message(
        content="Ciao! Posso darti info sulle escursioni, le prossime partenze e prenotare una guida."
    ).send()


@cl.on_message
async def on_message(message: cl.Message):
    messages = cl.user_session.get("messages")
    messages.append({"role": "user", "content": message.content})

    reply = await cl.make_async(get_response)(messages)

    await cl.Message(content=reply).send()


if __name__ == "__main__":
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    while True:
        user_input = input("Tu: ")
        if user_input.lower() in ("esci", "exit"):
            break
        messages.append({"role": "user", "content": user_input})
        print("Bot:", get_response(messages))