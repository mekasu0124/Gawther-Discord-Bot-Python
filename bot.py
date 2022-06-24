import disnake
import os
import json

from disnake.ext import commands
from createDb import create_db

with open('./config.json','r',encoding='utf-8-sig') as f:
    data = json.load(f)

token = data["token"]

intents = disnake.Intents.all()

bot = commands.Bot(
    command_prefix='<<',
    intents=intents,
    guild_ids=[779290532622893057],
    sync_commands_debug=True
)

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.id == 779290532622893057:
            for channel in guild.text_channels:
                if channel.name == "gawther_terminal":
                    await channel.send('Gawther Is Online, HAHA!')

for filename in os.listdir('./cogs'):
    if filename.endswith('py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(filename, 'loaded')

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