import openai
import os
from dotenv import load_dotenv

load_dotenv()
OPEN_API_KEY = os.environ["gpt_api_key"]
openai.api_key = OPEN_API_KEY
messages = []
content = "사과, 배, 참외, 피자 이 단어들의 공통점을 한 단어로 말해줘!"
# content = input("User: ")
messages.append({"role": "user", "content": content})

completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

# chat_respoonse가 리스폰스임.
chat_response = completion.choices[0].message.content
print(f"ChatGPT: {chat_response}")
messages.append({"role": "assistant", "content": chat_response})
