import solara
import solara.lab as lab

from app.components import (
    show_chat,
)


from langchain_core.prompts import ChatPromptTemplate 
from langchain_ollama.llms import OllamaLLM

template = """Question: {question} 
 
Answer: Let's think step by step."""

promt = ChatPromptTemplate.from_template(template)

model = OllamaLLM(model='llama3')




message = solara.reactive('')
list_messages_user = solara.reactive([])
list_messages_chatbox = solara.reactive([])

def send_message(mess: str):
    message.set(mess)
    list_messages_user.set(list_messages_user.get() + [mess])
    # print(message.value, list_messages_user.value)


@solara.component
def home_page():
    with solara.Div(
        style={
            'height': '100vh',
        }
    ) as container:
        solara.Text('Build Chatbot Ollama Model With 8 Sync Dev', style={'font-size': '2rem', 'margin-bottom': '20px'})
        with solara.Div(
            style={
                'height': '60%',
                'border-bottom': '1px solid #ccc',
                'border-radius': '5px',
                'shadow': '0 0 10px rgba(0, 0, 0, 0.1)',
                'overflow-y': 'auto',
            }
        ) as showchat:
            show_chat(
                mess_reactive=message,
                config_model={
                    'model': model,
                    'prompt': promt,
                },
            )
        with solara.Div(
            style={
                'padding': '10px',
            }
        ) as chat_box:
            lab.ChatInput(send_callback=send_message)