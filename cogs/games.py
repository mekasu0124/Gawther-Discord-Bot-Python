from disnake.ext import commands
from disnake.ext.commands import Cog

import disnake
import asyncio
import random
import sqlite3 as sql


class GawtherGames(Cog):
    def __init__(self,bot):
        self.bot = bot

    
    @commands.slash_command(name="coin-flip",description="Test Your Luck With A Toss Of A Coin!",guild_ids=[779290532622893057])
    @commands.has_any_role(
        "Owner", "Gawther", "Head Administrator", "Head Developer",
        "Head Designer", "Head Support", "Administrator", "Moderator",
        "Support Staff", "Community Helper", "DND DM", "DND PL", "Developers",
        "Designers", "Nitro Member", "Programming", "Gaming", "Member"
    )
    async def coin_toss(self,inter,side:str,amt:float):
        await inter.response.send_message("Tossing The Coin Now. . .",ephemeral=True)
        rand_num = 1 # random.randint(0,1)

        embed = disnake.Embed(
            color = disnake.Colour.green(),
            timestamp = inter.created_at,
            title = f"{inter.guild.name}'s Coin Toss",
            description = "Please See Details Below."
        ).set_thumbnail(url=inter.guild.avatar)

        if side.lower() == "heads" and rand_num == 1:
            # you win
            # add to database
            # send embed
            embed.add_field(
                name = "You Won!",
                value = f"{inter.author.mention} Has Won {amt}Gb! Adding Your Earnings Now!",
                inline = False
            )

            await inter.edit_original_message(embed=embed)
            await asyncio.sleep(3)

            with sql.connect('main.db') as mdb:
                cur = mdb.cursor()

                srch = 'SELECT bal FROM members WHERE id=?'
                val = (inter.author.id,)

                curr_bal = cur.execute(srch,val).fetchall()[0]
                new_bal = curr_bal + amt

                srch2 = 'UPDATE members SET bal=? WHERE id=?'
                val2 = (new_bal,inter.author.id,)

                cur.execute(srch2,val2)

            embed.add_field(
                name = "Success!",
                value = f"You Balance Of {curr_bal}Gb Has Been Increased By {amt}Gb To {new_bal}Gb.",
                inline=False
            )

            await inter.edit_original_message(embed=embed)
        elif side.lower() == "heads" and rand_num == 0:
            # you lose
            # sub from database
            # send embed
            pass
        elif side.lower() == "tails" and rand_num == 1:
            # you win
            # add to database
            # send embed
            pass
        elif side.lower() == "tails" and rand_num == 0:
            await inter.edit_original_message(f"{inter.author.id} the command should look like `/coin-toss side: Heads amt: 152.75`")


def setup(bot):
    bot.add_cog(GawtherGames(bot))