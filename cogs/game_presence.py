from disnake.ext import commands, tasks
from disnake.ext.commands import Cog

import disnake
import random
import asyncio


class TaskCommands(Cog):
    def __init__(self,bot):
        self.bot = bot

        self.game_pres.start()


    @tasks.loop(seconds=90)
    async def game_pres(self):
        await self.bot.wait_until_ready()

        presences = [
            "Let's Play /coin-toss!",
            "Need Help? /support",
            "Applications Open!"
        ]

        while True:
            await self.bot.change_presence(activity=disnake.Game(random.choice(presences)))
            await asyncio.sleep(90)


def setup(bot):
    bot.add_cog(TaskCommands(bot))