from discord.ext import commands
from discord import app_commands

import discord
from discord import ui


class ReportIssue(ui.Modal, title='Report an issue'):
    user_name = ui.TextInput(label='Your Discord name ', required=True, max_length=100, style=discord.TextStyle.short,
                             placeholder="eg. JohnDoe#0000")
    description = ui.TextInput(label='The issue', required=True, max_length=2000, style=discord.TextStyle.paragraph,
                               placeholder="eg. I can't access the vocal lounge")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"{interaction.user.name} Thank you for submitting your report, the moderation team will see it momentarily!",
            ephemeral=True)
        channel = discord.utils.get(interaction.guild.channels, name="report")
        await channel.send(
            f"Report Submitted by {interaction.user.mention} \n Name : {self.user_name} \n Reported for : {self.description}")


class Report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="report", description="Report an issue")
    # @commands.has_permissions(administrator=True)
    async def report(self, interaction: discord.Interaction):
        await interaction.response.send_modal(ReportIssue())


async def setup(bot):
    await bot.add_cog(Report(bot))
