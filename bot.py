
import os
import discord
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("DISCORD_GUILD_ID", "0"))
TARGET_USER_ID = int(os.getenv("TARGET_USER_ID", "0"))
YOUR_USER_ID = int(os.getenv("YOUR_USER_ID", "0"))

intents = discord.Intents.default()
intents.voice_states = True
intents.members = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    print("Monitoring voice channels...")


@client.event
async def on_voice_state_update(member, before, after):
    # Ignore activity outside your configured server
    if member.guild.id != GUILD_ID:
        return

    # Only react when the target joins or switches voice channels
    if after.channel is None or after.channel == before.channel:
        return

    # Only act on the specified user
    if member.id != TARGET_USER_ID:
        return

    # Check whether you are in that same voice channel
    your_member = member.guild.get_member(YOUR_USER_ID)
    if your_member is None or your_member.voice is None:
        return

    if your_member.voice.channel != after.channel:
        return

    # Disconnect the target user
    try:
        await member.move_to(
            None,
            reason="Target user joined the monitored voice channel"
        )
        print(f"Disconnected {member.display_name}")

    except discord.Forbidden:
        print("Missing permission to move members.")

    except discord.HTTPException as error:
        print(f"Discord API error: {error}")


if not TOKEN:
    raise ValueError("Missing DISCORD_TOKEN in .env")

client.run(TOKEN)
