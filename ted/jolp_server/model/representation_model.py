import openai
from dotenv import load_dotenv
from bertopic import BERTopic
from bertopic.representation import OpenAI
import os

prompt = """
I have a topic that contains the following documents: 
[DOCUMENTS]
The topic is described by the following keywords: [KEYWORDS]

Based on the information above, It MUST be one word korean topic label in the following format:
topic: <topic label>
"""
        
load_dotenv()
OPEN_API_KEY = os.environ["gpt_api_key"]
openai.api_key = OPEN_API_KEY
representation_model = OpenAI(
    model="gpt-3.5-turbo", prompt=prompt, delay_in_seconds=10, chat=True
)