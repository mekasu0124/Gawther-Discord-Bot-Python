import disnake
import asyncio
import sqlite3 as sql

from disnake.ext import commands
from disnake.ext.commands import Cog


class OnMemberJoin(Cog):
    def __init__(self,bot):
        self.bot = bot


    # when member first joins
    @commands.Cog.listener()
    async def on_member_join(self,member):
        guild = self.bot.get_guild(779290532622893057)

        rules_chan = disnake.utils.get(guild.text_channels,name="rules")
        intros_chan = disnake.utils.get(guild.text_channels,name="intros")
        role_sel_chan = disnake.utils.get(guild.text_channels,name="role_selection")
        how_to_supp = disnake.utils.get(guild.text_channels,name="how_to_get_support")



        welcome_embed = disnake.Embed(
            color = disnake.Colour.random(),
            timestamp = member.joined_at,
            title = 'Welcome To Gawther!',
            description = "Hi and Welcome! I'm Gawther, your friendly robot! Please see the details below."
        ).add_field(
            name = "Starting Information",
            value = "While you're waiting the 5 minutes to obtain the Member role and be able to chat with your friends in the server, please find the below information useful in your favor."
        ).add_field(
            name = "Useful Channels",
            value = f"{rules_chan.mention} - All In-Depth Rule Information. Start Here!\n{intros_chan.mention} - Introduce Yourself To The Community",
            inline=False
        ).add_field(
            name = "When Becoming A Member",
            value = f"When the timer finishes and you are moved into the members role, you'll only see the Support, General Lounge, and Information categories. This is because you have not told us your chosen walk(s) of life yet. To do this, please go to {role_sel_chan.mention} for further assistance."
        ).add_field(
            name = "Obtaining Support",
            value = f"Although you can see the Available Support Channels category, you cannot type in them. This is because you are not assigned to the role that matches the channel. To get support, please see {how_to_supp.mention} for further assistance."
        ).set_thumbnail(
            url=self.bot.user.avatar
        )

        await member.send(embed=welcome_embed)

        timer = 60*5 # 60 seconds time 5 for 5 minutes

        while timer != 0:
            await asyncio.sleep(1)
            timer -= 1

            if timer == (60*4):
                time_one = await member.send("You Have 4 Minutes Left")
            elif timer == (60*3):
                await time_one.delete()
                time_two = await member.send("You Have 3 Minutes Left")
            elif timer == (60*2):
                await time_two.delete()
                time_three = await member.send("You Have 2 Minutes Left")
            elif timer == 60:
                await time_three.delete()
                time_four = await member.send("You Have 1 Minute Left")
            elif timer < 60:
                await time_four.edit(f"You Have {timer}s Left")
        else:
            with sql.connect('main.db') as mdb:
                cur = mdb.cursor()

                srch = 'INSERT INTO members(id,exp,level,color,animal,food,edu_subj,artist_music,artist_art,season,holiday,warnings,mutes,bans,kicks,age,dob) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
                val = (member.id,0,0,None,None,None,None,None,None,None,None,0,0,0,0,0,None)

                cur.execute(srch, val)

            add_role = disnake.utils.get(guild.roles,name="Member")
            await member.add_roles(add_role)
            
            youre_a_member_embed = disnake.Embed(
                color = disnake.Colour.green(),
                timestamp = member.joined_at,
                title = "You're Officially A Member!",
                description = f"You've successfully been registered as a member to Gather! :) {member.mention} Please Have Fun! Relax! and Enjoy Yourself! and remember to follow the rules :P"
            ).set_thumbnail(
                url = self.bot.user.avatar
            )

            welc_chan = disnake.utils.get(guild.text_channels,name="welcome_members")
            await welc_chan.send(embed=youre_a_member_embed)


def setup(bot):
    bot.add_cog(OnMemberJoin(bot))