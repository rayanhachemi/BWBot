import json
from datetime import datetime

import discord
from discord.ext import commands

import settings


def save_data():
    with open("voice_data.json", "w") as file:
        json.dump(settings.voice_channel_data, file, indent=2)


def format_duration(minutes):
    hours = int(minutes / 60)
    reminder = minutes % 60
    minutes = int(reminder)
    seconds = int((reminder - minutes) * 60)
    return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)


class StopMeet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="stopmeet", with_app_command=True, description="Stop the meet")
    # @commands.has_permissions(administrator=True)
    async def stopmeet(self, ctx):
        if ctx.author.name in settings.admins:
            settings.record_voice_updates = False
            # await ctx.channel.set_permissions(ctx.guild.default_role, connect=True)

            meeting_end_time = datetime.now(settings.algeria_tz)

            for present_member in settings.voice_channel_data['presents']:
                if present_member['entrees']:
                    if not present_member['sorties']:
                        present_member['sorties'].append(meeting_end_time.strftime('%H:%M:%S'))
                    elif len(present_member['entrees']) > len(present_member['sorties']):
                        for _ in range(len(present_member['entrees']) - len(present_member['sorties'])):
                            present_member['sorties'].append(meeting_end_time.strftime('%H:%M:%S'))
                    duration = 0
                    for entry, exit_time in zip(present_member['entrees'], present_member['sorties']):
                        entry_time = datetime.strptime(entry, '%H:%M:%S').replace(tzinfo=settings.algeria_tz)
                        exit_time = datetime.strptime(exit_time, '%H:%M:%S').replace(tzinfo=settings.algeria_tz)
                        duration += (exit_time - entry_time).seconds / 60

                    present_member['duree'] = format_duration(duration)

            absent_members = []
            with open("membres.json", "r") as membres_file:
                membres_data = json.load(membres_file)

            for present_member in settings.voice_channel_data['presents']:
                member_name = present_member['nom_discord']
                for membre in membres_data:
                    if membre['nom_discord'] == member_name:
                        present_member['nom'] = membre['nom']
                        present_member['prenom'] = membre['prenom']
                        present_member['email'] = membre['email']
                        break

            list_presents = [present_member['nom_discord'] for present_member in
                             settings.voice_channel_data['presents']]
            for membre in membres_data:
                if membre['nom_discord'] not in list_presents:
                    absent_members.append({
                        'nom_discord': membre['nom_discord'],
                    })
            settings.voice_channel_data["absents"] = absent_members
            for absent_member in settings.voice_channel_data['absents']:
                member_name = absent_member['nom_discord']
                for membre in membres_data:
                    if membre['nom_discord'] == member_name:
                        absent_member['nom'] = membre['nom']
                        absent_member['prenom'] = membre['prenom']
                        absent_member['email'] = membre['email']
                        break
            save_data()
            await ctx.send("End of the meeting.")
            with open("voice_data.json", 'rb') as meeting_file:
                await ctx.author.send(content=f"{ctx.author.mention} Here is the meeting file",
                                      file=discord.File(meeting_file, 'voice_data.json'))
        else:
            await ctx.send(f"To run this command you must be an administrator")


async def setup(bot):
    await bot.add_cog(StopMeet(bot))
