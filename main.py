import asyncio
import os
from datetime import datetime
import discord
import json

from discord.ext import commands

import settings


class MyBot(commands.Bot):

    def __init__(self):
        intents = discord.Intents.all()
        intents.message_content = True

        super().__init__(
            command_prefix='$',
            intents=discord.Intents.all()
        )

        self.initial_extensions = [
            "report",
            "createmeet",
            "startmeet",
            "addnote",
            "stopmeet",
            "announce"
        ]

    async def setup_hook(self):
        for ext in self.initial_extensions:
            await self.load_extension(ext)

        ich = await self.tree.sync()
        print(len(ich))


bot = MyBot()


@bot.event
async def on_ready():
    print(f'Bot connecté en tant que {bot.user.name}')


with open("config.json", "r") as config_file:
    config = json.load(config_file)


@bot.event
async def on_voice_state_update(member, before, after):
    meeting_channel_id = settings.voice_channel_data.get('meet').get('id')
    if meeting_channel_id is not None and settings.record_voice_updates:
        if before.channel is None and after.channel is not None and after.channel.id == meeting_channel_id:
            join_time = datetime.now(settings.algeria_tz)
            member_name = member.name

            for present_member in settings.voice_channel_data['presents']:
                if present_member['nom_discord'] == member_name:
                    present_member['entrees'].append(join_time.strftime('%H:%M:%S'))
                    break
            else:
                settings.voice_channel_data['presents'].append({
                    'nom': '',
                    'prenom': '',
                    'email': '',
                    'nom_discord': member_name,
                    'entrees': [join_time.strftime('%H:%M:%S')],
                    'sorties': [],
                    'duree': [],
                })

        elif before.channel is not None and after.channel is None and before.channel.id == meeting_channel_id:
            member_name = member.name

            for present_member in settings.voice_channel_data['presents']:
                if present_member['nom_discord'] == member_name:
                    leave_time = datetime.now(settings.algeria_tz)
                    last_entry_time = datetime.strptime(present_member['entrees'][-1], '%H:%M:%S')
                    leave_time = leave_time.replace(tzinfo=None)  # Rendre leave_time offset-naïf
                    duration = (leave_time - last_entry_time).seconds / 60
                    present_member['sorties'].append(leave_time.strftime('%H:%M:%S'))
                    present_member['duree'].append(duration)
                    break

    # try:


from dotenv import load_dotenv

load_dotenv()

# Accédez au token en utilisant os.environ
TOKEN = os.environ.get("DISCORD_TOKEN")

try:
    bot.run(TOKEN)
except:
    os.system('python main.py')
    os.system('kill 1')
