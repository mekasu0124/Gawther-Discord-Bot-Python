import disnake
import asyncio
import sqlite3 as sql

from disnake.ext import commands
from disnake.ext.commands import Cog
from Paginator import CreatePaginator
from datetime import datetime


class DatabaseFunctions(Cog):
    def __init__(self,bot):
        self.bot = bot

    # done
    @commands.slash_command(name="update_database",description="Updates Database To Insert Non-Existent Members",guild_ids=[779290532622893057])
    @commands.has_any_role("Owner","Head Developer")
    async def update_mems(self, inter):
        with sql.connect('main.db') as mdb:
            cur = mdb.cursor()

            for member in inter.guild.members:
                if not member.bot:
                    srch = 'INSERT INTO members(id,bal,\
                        exp,level,color,animal,food,edu_subj,\
                            artist_music,artist_art,season,holiday,\
                                warnings,mutes,bans,kicks,age,dob) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
                    val = (member.id, 0, 0, 0, "empty", "empty", "empty", "empty",
                           "empty", "empty", "empty", "empty", 0, 0, 0, 0, 0, "empty")
                    cur.execute(srch, val)

        await inter.response.send_message("Finished Updating Members & Database", ephemeral=True)

def setup(bot):
    bot.add_cog(DatabaseFunctions(bot))