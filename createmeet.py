import json
from datetime import datetime
from discord.ext import commands
import settings


class CreateMeet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="createmeet", with_app_command=True, description="Create a meet")
    async def create_meet(self, ctx, meet_title: str, start_time: str, end_time: str):
        if ctx.author.name in settings.admins:
            meet_info = {
                'date': datetime.now(settings.algeria_tz).strftime('%Y-%m-%d'),
                'titre': meet_title,
                'heure_debut': start_time,
                'heure_fin': end_time,
                'organisateur': ctx.author.name,
            }

            with open("meeting_data.json", "w") as file:
                json.dump(meet_info, file, indent=2, ensure_ascii=False)
                await ctx.send(f"Meeting '{meet_title}' créé avec succès.")
        else:
            await ctx.send(f"To run this command you must be an administrator")


async def setup(bot):
    await bot.add_cog(CreateMeet(bot))
