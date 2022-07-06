import disnake 
import asyncio
import sqlite3 as sql

from disnake.ext import commands
from disnake.ext.commands import Cog 
from datetime import datetime, timedelta


class GeneralStaffCommands(Cog):
    def __init__(self,bot):
        self.bot = bot    
    
    @commands.slash_command(name="warn_member",description="Warn A Member",guild_ids=[779290532622893057])
    @commands.has_any_role(
        "Owner", "Head Administrator", "Head Support", "Head Designer", "Head Developer",
        "Administrator", "Moderator", "Support Staff", "Community Helper"
    )
    async def mem_warn(self,inter,member:disnake.Member,*,reason:str):
        embed = disnake.Embed(
            color = disnake.Colour.orange(),
            timestamp = inter.created_at,
            title = "{}'s Moderation System".format(self.bot.user.name),
            description = "Member: {}\nStaff Member: {}\nType: Warned".format(
                member.name, inter.author.name
            )
        ).add_field(
            name="Reason",
            value=reason,
            inline=False
        ).set_thumbnail(
            url = self.bot.user.avatar
        )
        
        with sql.connect('main.db') as mdb:
            cur = mdb.cursor()

            srch = 'SELECT warnings FROM members WHERE id=?'
            val = (member.id,)

            current_count = cur.execute(srch, val).fetchone()

            if current_count:
                new_count = current_count[0] + 1

                srch2 = 'UPDATE members SET warnings=? WHERE id=?'
                val2 = (new_count, member.id,)

                cur.execute(srch2, val2)
            else:
                new_count = 1

                srch2 = 'UPDATE members SET warnings=? WHERE id=?'
                val2 = (new_count, member.id,)

                cur.execute(srch2, val2)

        log_channel = disnake.utils.get(inter.guild.text_channels, name="warning_logs")

        await member.send(embed=embed)
        await log_channel.send(embed=embed)
        await inter.response.send_message("Successfully Warned {}".format(member.name), ephemeral=True)


    @commands.slash_command(name="mute_member",description="Mute A Member",guild_ids=[779290532622893057])
    @commands.has_any_role(
        "Owner", "Head Administrator", "Head Support", "Head Designer", "Head Developer",
        "Administrator", "Moderator", "Support Staff", "Community Helper"
    )
    async def mem_mute(self,inter,member:disnake.Member,time:int,*,reason:str):
        embed = disnake.Embed(
            color = disnake.Colour.yellow(),
            timestamp = inter.created_at,
            title = "{}'s Moderation System".format(self.bot.user.name),
            description = "Member: {}\nStaff Member: {}\nType: Muted\nTime To Serve: {}s\n".format(
                member.name, inter.author.name, str(time)
            )
        ).add_field(
            name="Reason",
            value=reason,
            inline=False
        ).set_footer(
            text = "To Appeal This Decision, Please Use The `/appealban` command."
        ).set_thumbnail(
            url = self.bot.user.avatar
        )

        member_current_roles = member.roles
        mute_role = disnake.utils.get(inter.guild.roles,name="Muted")
        log_channel = disnake.utils.get(inter.guild.text_channels,name="mute_logs")

        with sql.connect('main.db') as mdb:
            cur = mdb.cursor()

            srch = 'SELECT mutes FROM members WHERE id=?'
            val = (member.id,)

            current_count = cur.execute(srch, val).fetchone()

            if current_count:
                new_count = current_count[0] + 1

                srch2 = 'UPDATE members SET mutes=? WHERE id=?'
                val2 = (new_count, member.id,)

                cur.execute(srch2, val2)

                total_logs = cur.execute('SELECT * FROM mute_logs').fetchall()

                mute_id = len(total_logs) + 1

                start = datetime.now()
                end = datetime.now() + timedelta(seconds=time)

                srch3 = 'INSERT INTO mute_logs(id,mute_id,staff,start_time,end_time,reason) VALUES (?,?,?,?,?,?)'
                val3 = (member.id, mute_id, inter.author.id, start, end, reason)

                cur.execute(srch3, val3)

                for channel in inter.guild.voice_channels:
                    for mem in channel.members:
                        if mem.id == member.id:
                            await member.move_to(None)

                await member.edit(roles=[mute_role])
                await member.send(embed=embed)
                await log_channel.send(embed=embed)
                await inter.response.send_message("Successfully Muted {}".format(member.name), ephemeral=True)

                while time > 0:
                    await asyncio.sleep(1)
                    time -= 1
                else:
                    await member.edit(roles=member_current_roles)

                await member.send("Your Mute Has Been Lifted, {}".format(member.mention))
            else:
                new_count = 1

                srch2 = 'UPDATE members SET mutes=? WHERE id=?'
                val2 = (new_count, member.id,)

                cur.execute(srch2, val2)

                total_logs = cur.execute('SELECT * FROM mute_logs').fetchall()

                mute_id = len(total_logs) + 1

                start = datetime.now()
                end = datetime.now() + timedelta(seconds=time)

                srch3 = 'INSERT INTO mute_logs(id,mute_id,staff,start_time,end_time,reason) VALUES (?,?,?,?,?,?)'
                val3 = (member.id, mute_id, inter.author.id, start, end, reason)

                cur.execute(srch3, val3)

                for channel in inter.guild.voice_channels:
                    for mem in channel.members:
                        if mem.id == member.id:
                            await member.move_to(None)

                await member.send(embed=embed)
                await log_channel.send(embed=embed)
                await inter.response.send_message("Successfully Muted {}".format(member.name), ephemeral=True)
                await member.edit(roles=[mute_role])

                while time > 0:
                    await asyncio.sleep(1)
                    time -= 1
                else:
                    await member.edit(roles=member_current_roles)

                await member.send("Your Mute Has Been Lifted, {}".format(member.mention))

def setup(bot):
    bot.add_cog(GeneralStaffCommands(bot))