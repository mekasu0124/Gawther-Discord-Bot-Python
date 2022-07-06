import disnake
import os
import json
import asyncio

from disnake.ext import commands
from createDb import create_db

with open('./config.json','r',encoding='utf-8-sig') as f:
    data = json.load(f)

token = data["token"]

intents = disnake.Intents.all()

bot = commands.Bot(command_prefix='<<',intents=intents,guild_ids=[779290532622893057],sync_commands_debug=True)

@bot.event
async def on_ready():
    for guild in bot.guilds:
        term_channel = disnake.utils.get(guild.text_channels, name="gawther_terminal")
        count = 0

        for filename in os.listdir('./cogs'):
            if filename.endswith('py'):
                bot.load_extension(f'cogs.{filename[:-3]}')
                count += 1

        msg = await term_channel.send(f'{bot.user} Logging In. . .')
        await asyncio.sleep(0.5)
        await msg.delete()
        await term_channel.send(f'{bot.user} Has Logged In!')
        return

# credit for this update command goes to
# gamingbuddhist#9599 - discord
@bot.command()
@commands.is_owner()
async def update(ctx):
    async def start():
        os.system("python ./bot.py")
        await confirm()
    await ctx.send("Gawther will reset now")
    await start()

async def confirm(ctx):
    await ctx.send("Restart Complete")


if __name__ == '__main__':
    create_db()
    bot.run(token)