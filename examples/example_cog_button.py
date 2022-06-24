import disnake 
import os
import sys
import json

from disnake.ext import commands

if not os.path.isfile('config.json'):
    sys.exit("'config.json' Not Found!")
else:
    with open('./config.json','r',encoding='utf-8-sig') as f:
        data = json.load(f)

guild_id = data["bot_info"]["guild_id"]


class SupportFunctions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    class Confirm(disnake.ui.View):
        def __init__(self):
            super().__init__()
            self.value = None

        
        @disnake.ui.button(label="Confirm", style=disnake.ButtonStyle.green)
        async def confirm(self, button:disnake.ui.Button,inter:disnake.MessageInteraction):
            await inter.response.send_message("Confirming", ephemeral=True)
            self.value = True
            self.stop()

        @disnake.ui.button(label="Cancel", style=disnake.ButtonStyle.red)
        async def cancel(self, button:disnake.ui.Button,inter:disnake.MessageInteraction):
            await inter.response.send_message("Cancelling", ephemeral=True)
            self.value = False
            self.stop()


    @commands.slash_command(
        name="example_with_buttons",
        description="just an example to show me how to use buttons",
        guild_ids=[guild_id]
    )
    @commands.is_owner()
    async def ask(self,ctx):
        view = self.Confirm()
        await ctx.send("Do you want to continue?", view=view)
        await view.wait()

        if view.value is None:
            await ctx.send("Timed Out")
        elif view.value:
            await ctx.send("Confirmed")
        else:
            await ctx.send("Cancelled")



def setup(bot):
    bot.add_cog(SupportFunctions(bot))