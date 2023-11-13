import openai

openai.api_key = "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"
messages = []
content = "사과, 배, 참외, 피자 이 단어들의 공통점을 한 단어로 말해줘!"
# content = input("User: ")
messages.append({"role": "user", "content": content})

completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

# chat_respoonse가 리스폰스임.
chat_response = completion.choices[0].message.content
print(f"ChatGPT: {chat_response}")
messages.append({"role": "assistant", "content": chat_response})
