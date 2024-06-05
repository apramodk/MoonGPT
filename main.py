import os
import discord
import nacl
from dotenv import load_dotenv
from discord.ext import commands
from openai import OpenAI
import time

load_dotenv()
botToken = os.getenv('bot_token')
bot = commands.Bot(command_prefix=">>", intents=discord.Intents.all())
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class ChatBot:
    def __init__(self):
        self.assistant = client.beta.assistants.create(
            name="Moon",
            instructions="your name is Moon, while you are helpful and provide answers to any questions, you answer them in a rude but funny manner.",
            model="gpt-3.5-turbo-0125"
        )
        self.thread = client.beta.threads.create()

    def get_status(self, run):
        status = client.beta.threads.runs.retrieve(
            thread_id=self.thread.id,
            run_id=run.id
        )
        # print(status)
        return status

    def send_response(self, msg):
        # adding user message to thread
        message = client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=msg,
        )

        # running the assistant with the user message
        run = client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
        )
        
        while True:
            tmp = self.get_status(run)
            if tmp.status == "completed":
                break

        # getting the response from the assistant
        ret = client.beta.threads.messages.list(thread_id=self.thread.id).data[0].content[0].text
        return ret.value

# def tts(msg):
    # response = client.audio.speech.create(
    # model="tts-1-hd",
    # voice="alloy",
    # input=msg
    # )
    # response.stream_to_file("output.mp3")
# async def drawThis(msg):
#     img = client.images.generate(
#     model="dall-e-2",
#     prompt=msg,
#     size="256x256",
#     quality="standard",
#     n=1,)
#     tmp = img.data[0].url
#     return tmp

async def pm(msg):
    time.sleep(4)
    return "worked " + msg

if __name__=="__main__":
    chatbot = ChatBot()

    # text only
    @bot.command()
    async def hello(ctx):
        await ctx.send(f"hello there, {ctx.author.mention}!")

    @bot.command()
    async def cb(ctx, *, arg):
        print(ctx.author)
        response = chatbot.send_response(arg)
        await ctx.send(response)
        
        # tts(response)
        # await ctx.send(file=discord.File(r'output.mp3'))
        # os.remove("output.mp3")

    @bot.command()
    async def roast(ctx, arg1, arg2=""):
        print(arg2)
        msg = "tease " + arg1 + ". Use the given name to reference them again. do not modify the name." + arg2
        response = chatbot.send_response(msg)
        await ctx.send(response)
        
        # tts(response)
        # await ctx.send(file=discord.File(r'output.mp3'))
        # os.remove("output.mp3")
    
    # @bot.command()
    # async def draw(ctx, *, arg):
    #     prmpt = str(arg)
    #     print(prmpt)
    #     await ctx.send("ok, give me a second to draw that")
    #     imgURL = await drawThis(prmpt)
    #     # print(imgURL)
    #     await ctx.send(imgURL)
    #     # await ctx.send(file=discord.File(r'imgURL'))

    # voice channel
    @bot.command()
    async def join(ctx):
        channel = ctx.author.voice.channel
        print(channel)
        await channel.connect()

    @bot.command()
    async def leave(ctx):
        await ctx.voice_client.disconnect()
    
    @bot.command()
    async def play(ctx, arg):
        # player = await vc.create_ytdl_player(arg)
        url = url(arg)
        player = await ctx.voice_client.create_ytdl_player(url)
        player.start()

    bot.run(botToken)
