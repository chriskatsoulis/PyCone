import discord
from discord.ext import commands
import openai
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True

openai.api_key = ''     # insert OpenAI token

client = commands.Bot(command_prefix="=", intents=discord.Intents.all())

@client.event
async def on_ready():
    await client.tree.sync()
    print('We have logged in as {0.user}'.format(client))


class Difficulty:
    def __init__(self, string):
        self._string = string

    def get_string(self):
        return self._string


class SelectDifficultyMenu(discord.ui.View):

    options = [
        discord.SelectOption(label="Easy", value="1", description=None),
        discord.SelectOption(label="Medium", value="2", description=None),
        discord.SelectOption(label="Hard", value="3", description=None)
    ]

    @discord.ui.select(placeholder="Select Difficulty", options=options)
    async def menu_callback(self, interaction: discord.Interaction, select):
        select.disabled=True
        if select.values[0] == "1":
            difficulty = Difficulty("Easy")
            await interaction.response.send_message(content="Select topic!", view=SelectTopicMenu())

        elif select.values[0] == "2":
            difficulty = Difficulty("Medium")
            await interaction.response.send_message(content="Select topic!", view=SelectTopicMenu())

        elif select.values[0] == "3":
            difficulty = Difficulty("Hard")
            await interaction.response.send_message(content="Select topic!", view=SelectTopicMenu())


class SelectTopicMenu(discord.ui.View):

    options = [
        discord.SelectOption(label="Binary Search", value="1", description=None),
        discord.SelectOption(label="Combinatorics", value="2", description=None),
        discord.SelectOption(label="Linked List", value="3", description=None),
        discord.SelectOption(label="Recursion", value="4", description=None),
        discord.SelectOption(label="Sorting", value="5", description=None)
    ]

    @discord.ui.select(placeholder="Select Topic", options=options)
    async def menu_callback(self, interaction: discord.Interaction, select):
        select.disabled=True
        if select.values[0] == "1":
            user_message = """
            Please generate a Python problem of easy
            difficulty that involves binary search. Do not reveal the answer or in any 
            way show any sort of Python code. I want to try the problem on my own, so 
            don't spoil it!
            """
            channel = str(user_message.channel.name)
            username = str(user_message.author).split('#')[0]
            response = openai.Completion.create(
                engine='text-davinci-003',
                prompt=user_message,
                max_tokens=100,
                temperature=0.7,
                n=1,
                stop=None
            )
            chatgpt_response = response.choices[0].text.strip()
            print(chatgpt_response)
            await interaction.response.send_message(content=chatgpt_response)

        elif select.values[0] == "2":
            await interaction.response.send_message(content=None)

        elif select.values[0] == "3":
            await interaction.response.send_message(content=None)

        elif select.values[0] == "4":
            await interaction.response.send_message(content=None)

        elif select.values[0] == "5":
            await interaction.response.send_message(content=None)


@client.tree.command(name="practicequestion", description="Generate a Python practice question from ChatGPT!")
async def PracticeQueston(interaction: discord.Interaction):
    await interaction.response.send_message(content="Select difficulty!", view=SelectDifficultyMenu())

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with client:
        await load()
        await client.start(')       # insert Discord token

asyncio.run(main())
