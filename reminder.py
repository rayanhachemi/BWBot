import asyncio
import json
from datetime import datetime, timedelta
import discord
from discord import Embed
from discord.ext import commands
import settings


class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="reminder")
    async def reminder(self,ctx, channel_name: str):
        with open("meeting_data.json", "r") as file:
            meeting_info = json.load(file)

        meet_title = meeting_info.get('titre')
        start_time = meeting_info.get('heure_debut')

        if not meet_title or not start_time:
            await ctx.send("No meeting has been created or the information is missing.")
            return

        voice_channel = discord.utils.get(ctx.guild.voice_channels, name=channel_name)

        if voice_channel:
            current_time = datetime.now(settings.algeria_tz).time()
            start_datetime = datetime.strptime(start_time, '%H:%M').time()
            current_datetime = datetime.combine(datetime.now(settings.algeria_tz).date(), current_time)
            start_datetime = datetime.combine(datetime.now(settings.algeria_tz).date(), start_datetime)
            print(current_datetime)
            print(start_datetime)
            if current_datetime < start_datetime:
                time_until_meet_start = start_datetime - current_datetime

                while time_until_meet_start.total_seconds() > 60:
                    await asyncio.sleep(1)
                    current_datetime += timedelta(seconds=1)
                    time_until_meet_start -= timedelta(seconds=1)
                    print(time_until_meet_start)
                else:
                    embed = Embed(
                        title=f"Meeting '{meet_title}'",
                        description=f"The meeting starts in 1 minutes. Get ready!"
                    )

                    bot_avatar_url = settings.bot.user.avatar
                    embed.set_thumbnail(url=bot_avatar_url)
                    await voice_channel.send("@everyone", embed=embed)
            else:
                await ctx.send(f"The meeting '{meet_title}' has already started.")
        else:
            await ctx.send(f"The voice channel '{channel_name}' was not found.")


