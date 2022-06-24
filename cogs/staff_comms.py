import disnake
import asyncio
import json
import sqlite3 as sql

from disnake.ext import commands
from disnake.ext.commands import Cog
from datetime import datetime, timedelta


class TierFourCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    # Support Staff, Community Helper commands
    
    @commands.slash_command(name="warn_member",description="Warn A Member")
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


    @commands.slash_command(name="mute_member",description="Mute A Member")
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


    @commands.slash_command(name="kick_member",description="Kick A Member")
    @commands.has_any_role(
        "Owner", "Head Administrator", "Head Support", "Head Designer", "Head Developer",
        "Administrator", "Moderator"
    )
    async def mem_kick(self,inter,member:disnake.Member,time:int,*,reason:str):
        embed = disnake.Embed(
            color = disnake.Colour.purple(),
            timestamp = inter.created_at,
            title = "{}'s Moderation System".format(self.bot.user.name),
            description = "Member: {}\nStaff Member: {}\nType: Kicked\nTime To Serve: {}".format(
                member.name, inter.author.name, str(time)
            )
        ).add_field(
            name="Reason",
            value=reason,
            inline=False
        ).set_footer(
            text = "To Appeal This Decision, Please Use The '/appealban' command."
        ).set_thumbnail(
            url = self.bot.user.avatar
        )

        member_current_roles = member.roles
        kick_role = disnake.utils.get(inter.guild.roles,name="Kicked")
        log_channel = disnake.utils.get(inter.guild.text_channels, name="kick_logs")

        with sql.connect('main.db') as mdb:
            cur = mdb.cursor()

            srch = 'SELECT kicks FROM members WHERE id=?'
            val = (member.id,)

            current_count = cur.execute(srch, val).fetchone()

            if current_count:
                new_count = current_count[0] + 1

                srch2 = 'UPDATE members SET kicks=? WHERE id=?'
                val2 = (new_count, member.id,)

                cur.execute(srch2, val2)

                total_logs = cur.execute('SELECT * FROM kick_logs').fetchall()

                kick_id = len(total_logs) + 1

                start = datetime.now()
                end = datetime.now() + timedelta(seconds=time)

                srch3 = 'INSERT INTO kick_logs(id,kick_id,staff,start_time,end_time,reason) VALUES (?,?,?,?,?,?)'
                val3 = (member.id, kick_id, inter.author.id, start, end, reason)

                cur.execute(srch3, val3)

                for channel in self.bot.get_guild(guild_id).voice_channels:
                    for mem in channel.members:
                        if mem.id == member.id:
                            await member.move_to(None)

                await member.send(embed=embed)
                await log_channel.send(embed=embed)
                await inter.response.send_message("Successfully Kicked {}".format(member.name), ephemeral=True)
                await member.edit(roles=[kick_role])

                while time > 0:
                    await asyncio.sleep(1)
                    time -= 1
                else:
                    await member.edit(roles=member_current_roles)

                await member.send("Your Kick Has Been Lifted, {}".format(member.mention))
            else:
                new_count = 1

                srch2 = 'UPDATE members SET kicks=? WHERE id=?'
                val2 = (new_count, member.id,)

                cur.execute(srch2, val2)

                total_logs = cur.execute('SELECT * FROM kick_logs').fetchall()

                kick_id = len(total_logs) + 1

                start = datetime.now()
                end = datetime.now() + timedelta(seconds=time)

                srch3 = 'INSERT INTO kick_logs(id,kick_id,staff,start_time,end_time,reason) VALUES (?,?,?,?,?,?)'
                val3 = (member.id, kick_id, inter.author.id, start, end, reason)

                cur.execute(srch3, val3)

                for channel in self.bot.get_guild(guild_id).voice_channels:
                    for mem in channel.members:
                        if mem.id == member.id:
                            await member.move_to(None)

                await member.send(embed=embed)
                await log_channel.send(embed=embed)
                await inter.response.send_message("Successfully Kicked {}".format(member.name), ephemeral=True)
                await member.edit(roles=[kick_role])

                while time > 0:
                    await asyncio.sleep(1)
                    time -= 1
                else:
                    await member.edit(roles=member_current_roles)

                await member.send("Your Kick Has Been Lifted, {}".format(member.mention))

    @commands.slash_command(name="purge",description="Deletes _N_ Messages From The Channel Executed In")
    @commands.has_any_role("Owner", "Head Developer", "Head Administrator", "Head Designer", "Head Support")
    async def purge_message(self, inter, num: int, *, reason: str):
        if num > 25:
            return await inter.response.send_message("Do Not Purge More Than 25 Messages At A Time, {}".format(inter.author.mention), ephemeral=True)
        else:
            await inter.response.send_message(f"Purging {num} Message", ephemeral=True)
            await inter.channel.purge(limit=num)

            embed = disnake.Embed(
                color=disnake.Colour.random(),
                timestamp=inter.created_at,
                title="{}'s Purge Messages Command".format(inter.guild.name),
                description=f"User: {inter.author.name}\nAction: Purged\nWhere: {inter.channel.name}\nNumber Of Messages: {num}\nWhy: {reason}"
            ).set_thumbnail(url=self.bot.user.avatar)

            message = await inter.channel.history(limit=None).flatten()
            await inter.edit_original_message(f"Purging Of {num}/{len(message)} Messages Complete")
            log_channel = disnake.utils.get(inter.guild.text_channels, name="message_deletes")
            await log_channel.send(embed=embed)



    


def setup(bot):
    bot.add_cog(TierFourCommands(bot))
