from discord.ext import commands

import settings


class AddNote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="addnote", with_app_command=True, description="Add a note to the meet")
    async def add_note(self, ctx, *, note):
        if ctx.author.name in settings.admins:
            if settings.voice_channel_data.get('meet'):
                settings.voice_channel_data['meet']['notes'].append(note)
                await ctx.send(f"A note was added to the meet's agenda.",delete_after=1)
            else:
                await ctx.send("A meet has not been started yet.")
        else:
            await ctx.send(f"To run this command you must be an administrator")


async def setup(bot):
    await bot.add_cog(AddNote(bot))
