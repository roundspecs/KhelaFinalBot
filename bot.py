import discord
import responses


async def send_message(message, user_message):
    try:
        response = await responses.get_response(message, user_message)
        if response == None:
            return
        await message.reply(response)
    except Exception as e:
        print(e)

def run_bot():
    TOKEN: str
    with open('token.txt') as f:
        TOKEN = f.read()
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
    
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        user_message = str(message.content)
        await send_message(message=message, user_message=user_message)
    client.run(TOKEN)