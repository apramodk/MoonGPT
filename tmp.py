import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

from openai import OpenAI
client = OpenAI()

img = client.images.generate(
    model="dall-e-2",
    prompt="A cute baby sea otter",
    n=1,
    size="256x256"
)

print(img.data[0].url)