import discord
import asyncio

TOKEN = 'TOKEN'  # Token
MESSAGE = 'Hello, how are you?'  # Message
REPEAT_COUNT = 3  # Messages to send

intents = discord.Intents.default()
intents.dm_messages = True
intents.guilds = True
intents.members = True

client = discord.Client(intents=intents)

async def get_or_create_dm_channel(member):
    dm_channel = member.dm_channel
    if dm_channel is None:
        dm_channel = await member.create_dm()
    return dm_channel

async def send_message(member, message, repeat_count):
    dm_channel = await get_or_create_dm_channel(member)
    for _ in range(repeat_count):
        try:
            await dm_channel.send(message)
            await asyncio.sleep(1)
        except discord.Forbidden:
            print(f'Cannot DM {member.name}: User has DMs disabled or other restriction.')
            break
        except Exception as e:
            print(f'Error: Failed to send message to {member.name}. Error: {e}')
            break

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} ({client.user.id})')

    for guild in client.guilds:
        print(f'Sending message to all members in guild {guild.name}...')
        for member in guild.members:
            if member != client.user and not member.bot:
                await send_message(member, MESSAGE, REPEAT_COUNT)
        print(f'Successfully sent messages in guild {guild.name}.')

    print('Successfully sent messages to all guilds.')
    await client.close()

client.run(TOKEN)
