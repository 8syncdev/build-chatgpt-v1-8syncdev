import solara
from solara.tasks import use_task, Task
import solara.lab as lab
from langchain_ollama.llms import OllamaLLM
from asgiref.sync import sync_to_async


manager = solara.reactive([])

@solara.component
def get_ai_chat(chain: OllamaLLM, current_mess: str):
    print('current_mess', current_mess)
    if current_mess == '':
        manager.set(manager.get() + [{
            'user': current_mess,
            'ai': 'Please enter a message',
        }])
        return lab.ChatMessage(children=[solara.Markdown(md_text='Please enter a message')], user=False)
        
    ai_mess = chain.invoke(current_mess)
    manager.set(manager.get() + [{
        'user': current_mess,
        'ai': '...' if ai_mess == '' else ai_mess,
    }])
    return lab.ChatMessage(children=[
        solara.Markdown(md_text=ai_mess),
    ], user=False)

# async def async_get_ai_chat(chain: OllamaLLM, current_mess: str):
#     return await sync_to_async(get_ai_chat)(chain, current_mess)

def get_old_mess():
    old_mess = []
    for mess in manager.get():
        user_chat = lab.ChatMessage(
            children=[
                solara.Markdown(md_text=mess['user']),
            ],
            user=True,
        )
        ai_chat = lab.ChatMessage(
            children=[
                solara.Markdown(md_text=mess['ai']),
            ],
            user=False,
        ) if mess['ai'] != '' else solara.Div()
        old_mess.extend([user_chat, ai_chat])
    return old_mess

@solara.component
def show_chat(
    mess_reactive: solara.Reactive,
    config_model: dict,
    list_messages_user_reactive: solara.Reactive = None,
    list_messages_chatbox_reactive: solara.Reactive = None,
):
    chain = config_model['prompt'] | config_model['model']
    get_ai_chat_response: Task = use_task(
        lambda: get_ai_chat(chain=chain, current_mess=mess_reactive.value),
        dependencies=[mess_reactive.value]
    )

    if get_ai_chat_response.finished:
        old_mess = get_old_mess()[:-1]
        return lab.ChatBox(children=[
            *old_mess,
            get_ai_chat_response.result.value,
        ])
    else:
        old_mess = get_old_mess()
        return lab.ChatBox(children=[
            *old_mess,
            lab.ChatMessage(children=[mess_reactive.value], user=True),
            solara.ProgressLinear(value=get_ai_chat_response.progress),
        ])


            
        

        


