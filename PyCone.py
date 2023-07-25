import discord
from discord.ext import commands
import openai
import os
import asyncio


intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="=", intents=discord.Intents.all())

# insert OpenAI token
api_key = 'OPENAI_TOKEN'
openai.api_key = api_key


@client.event
async def on_ready():
    await client.tree.sync()
    print('We have logged in as {0.user}'.format(client))


def get_chatgpt_response(prompt):
    """A function that sends ChatGPT a prompt and returns the response."""
    try:
        problem = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=150,
            stop=None,
        )
        return problem["choices"][0]["text"].strip()
    except Exception as e:
        print("Error:", e)
        return None


# Here we save the difficulty selected by the user and the practice
# problem generated by ChatGPT.
difficulty = []
practice_problem = []


class SelectDifficultyMenu(discord.ui.View):
    """A class that represents the difficulty drop-down menu."""
    options = [
        discord.SelectOption(label="Easy", value="1", description=None),
        discord.SelectOption(label="Medium", value="2", description=None),
        discord.SelectOption(label="Hard", value="3", description=None)
    ]

    @discord.ui.select(placeholder="Difficulty", options=options)
    async def menu_callback(self, interaction: discord.Interaction.response, select):
        """A function that prompts the user to select a difficulty. Once a difficulty is chosen
        by the user, the difficulty is stored in the difficulty list and then the SelectTopicMenu
        class is called."""
        select.disabled = True
        difficulty.append(select.values[0])
        await interaction.response.send_message(content="Select topic!", view=SelectTopicMenu())


class SelectTopicMenu(discord.ui.View):
    """A class that represents the topic drop-down menu."""
    options = [
        discord.SelectOption(label="Arrays", value="1", description=None),
        discord.SelectOption(label="Backtracking", value="2", description=None),
        discord.SelectOption(label="Binary Search", value="3", description=None),
        discord.SelectOption(label="Breadth-First Search", value="4", description=None),
        discord.SelectOption(label="Depth-First Search", value="5", description=None),
        discord.SelectOption(label="Divide and Conquer", value="6", description=None),
        discord.SelectOption(label="Dynamic Programming", value="7", description=None),
        discord.SelectOption(label="Graph", value="8", description=None),
        discord.SelectOption(label="Greedy", value="9", description=None),
        discord.SelectOption(label="Hash Table", value="10", description=None),
        discord.SelectOption(label="Heap Queue", value="11", description=None),
        discord.SelectOption(label="Linked List", value="12", description=None),
        discord.SelectOption(label="Matrix", value="13", description=None),
        discord.SelectOption(label="Memoization", value="14", description=None),
        discord.SelectOption(label="Monotonic Stack", value="15", description=None),
        discord.SelectOption(label="Priority Queue", value="16", description=None),
        discord.SelectOption(label="Recursion", value="17", description=None),
        discord.SelectOption(label="Sliding Window", value="18", description=None),
        discord.SelectOption(label="Sorting", value="19", description=None),
        discord.SelectOption(label="Stacks", value="20", description=None),
        discord.SelectOption(label="Strings", value="21", description=None),
        discord.SelectOption(label="Trees", value="22", description=None),
        discord.SelectOption(label="Trie", value="23", description=None),
        discord.SelectOption(label="Two Pointers", value="24", description=None),
        discord.SelectOption(label="Union Find", value="25", description=None)
    ]

    @discord.ui.select(placeholder="Topic", options=options)
    async def menu_callback(self, interaction: discord.Interaction.response, select):
        """A function that prompts the user to select a topic. Once a topic is chosen by the user,
        the Discord bot sends ChatGPT a prompt, receives the response, stores the response in the
        practice_problem list, and then calls the SelectTopicMenu class."""
        select.disabled = True
        user_prompt_1 = f"Please generate a random Python coding problem of {difficulty[-1]} " \
                        f"difficulty that involves {select.values[0]}. The problem should " \
                        f"be similar to a LeetCode problem in terms of the problem that is " \
                        f"presented and the answer should require coding in Python. In " \
                        f"the problem prompt, please provide an example input and output, " \
                        f"and parameters. Also specify modules that are required. Do not " \
                        f"reveal the answer or in any way show any sort of Python code. I " \
                        f"want to try the problem on my own, so don't spoil it!"
        responsegpt = get_chatgpt_response(user_prompt_1)
        practice_problem.append(responsegpt)
        await interaction.response.send_message(content=responsegpt, view=ReceiveAnswer())


class ReceiveAnswer(discord.ui.View):
    """A class that represents the answer drop-down menu."""
    option = [discord.SelectOption(label="Show me the answer!", value="1", description=None)]

    @discord.ui.select(placeholder="Answer", options=option)
    async def menu_callback(self, interaction: discord.Interaction.response, select):
        """A function that prompts the user to select the answer. Once "Show me the answer!" is
        chosen by the user, the Discord bot sends ChatGPT a prompt, receives the response, and
        displays the response to the user."""
        select.disabled = True
        previous_problem = practice_problem[-1]
        user_prompt_2 = f"What is the answer to the following Python problem (please provide " \
                        f"the code)?: {previous_problem}"
        answergpt = get_chatgpt_response(user_prompt_2)
        await interaction.response.send_message(content=answergpt)


@client.tree.command(name="practicequestion", description="Generate a Python practice problem from ChatGPT!")
async def practice_question(interaction: discord.Interaction.response):
    """A function that creates a Discord bot command that prompts the user to receive a Python
    practice problem and answer."""
    await interaction.response.send_message(content="Select difficulty!", view=SelectDifficultyMenu())


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with client:
        await load()
        # insert Discord bot token
        await client.start('DISCORD_BOT_TOKEN')

asyncio.run(main())
