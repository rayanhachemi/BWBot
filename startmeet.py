import json
from datetime import datetime

from discord import app_commands
from discord.ext import commands

import settings


class StartMeet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="startmeet", with_app_command=True, description="Begin the meet")
    # @commands.has_permissions(administrator=True)
    async def startmeet(self, ctx):
        if ctx.author.name in settings.admins:
            with open(r"meeting_data.json", 'r') as meeting_file:
                meeting_data = json.load(meeting_file)
            meet_info = {
                'date': meeting_data['date'],
                'titre': meeting_data['titre'],
                'heure_debut': meeting_data['heure_debut'],
                'notes': [],
                'organisateur': meeting_data['organisateur'],
                'id': '',
            }
            settings.voice_channel_data = {'meet': meet_info, 'presents': []}
            if ctx.author.voice is not None:
                voice_channel = ctx.author.voice.channel
                if len(voice_channel.members) > 0:
                    for member in voice_channel.members:
                        member_name = member.name
                        settings.voice_channel_data['presents'].append({
                            'nom': '',
                            'prenom': '',
                            'email': '',
                            'nom_discord': member_name,
                            'entrees': [datetime.now(settings.algeria_tz).strftime('%H:%M:%S')],
                            'sorties': [],
                            'duree': [],
                        })
                if settings.record_voice_updates:
                    await ctx.send('Recording is already in progress.')
                    return
                settings.voice_channel_data['meet']['id'] = ctx.author.voice.channel.id
                settings.record_voice_updates = True
                await ctx.send('Beginning of the meeting.')
            else:
                await ctx.send('You need to be in a voice channel to start the meeting.')

        else:
            await ctx.send(f"To run this command you must be an administrator")


async def setup(bot):
    await bot.add_cog(StartMeet(bot))
