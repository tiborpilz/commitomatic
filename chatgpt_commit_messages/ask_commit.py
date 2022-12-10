from revChatGPT.revChatGPT import Chatbot

config = {
    "email": "tibor@pilz.berlin",
    "password": "Uselessly-Impatient-Living5-Barrier-Correct",
}

chatbot = Chatbot(config, conversation_id=None)

response = chatbot.get_chat_response("Hello World", output="text")
print(response)
