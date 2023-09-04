import discord
from discord.ext import commands
from discord import ui, app_commands


class AnnounceModel(ui.Modal, title='Report an issue'):
    objet = ui.TextInput(label='Objet', required=True, max_length=100, style=discord.TextStyle.short,
                         placeholder="eg. Suite du partage de tâches pour l'AG")
    heure = ui.TextInput(label="Heure", required=True, max_length=100, style=discord.TextStyle.short,
                         placeholder="eg. 20:00")
    lieux = ui.TextInput(label="Lieux", required=True, max_length=100, style=discord.TextStyle.short,
                         placeholder="eg. meeting-room")
    concernes = ui.TextInput(label="Concernés", required=True, max_length=2000, style=discord.TextStyle.paragraph,
                             placeholder="eg. meeting-room")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("hey")

    def __init__(self):
        super().__init__()


class Announce(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="announce", description="Announce a meet")
    async def announce(self, interaction: discord.Interaction):
        await interaction.response.send_modal(AnnounceModel())


async def setup(bot):
    await bot.add_cog(Announce(bot))
