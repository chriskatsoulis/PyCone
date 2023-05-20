import discord
import openai

intents = discord.Intents.default()
intents.message_content = True

token = 'MTEwODY5MTcxNjA2MTUyODI0Nw.GYj7vK.qmVaEu4O-dKlkA059UduMXxbXZES0JsvyHNe1Q'
openai.api_key = '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'

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)

    print(username + " said " + user_message.lower() + " in " + channel)

    if message.channel.name == client.user:
        return

    if message.channel.name == 'development':
        response = openai.Completion.create(
                model="text-davinci-003",
                prompt=user_message,
                max_tokens=3000,
                temperature=0.7
            )

        output = response["choices"][0]["text"]

        print(output)
        await message.channel.send(output)

client.run(token)
