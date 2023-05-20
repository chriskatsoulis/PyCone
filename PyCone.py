# PyCone.py

import discord

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('Hi'):
        await message.channel.send('Hello!')


client.run('MTEwODY5MTcxNjA2MTUyODI0Nw.GnB-Wc.fyONROu38QXsrx-YE_iF0RSgWid9E9KIZjw8FA')
