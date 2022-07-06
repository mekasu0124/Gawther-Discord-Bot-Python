import disnake
import asyncio
import sqlite3 as sql

from disnake.ext import commands
from disnake.ext.commands import Cog
from Paginator import CreatePaginator
from datetime import datetime, timedelta


class TierOneCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    # done
    @commands.slash_command(name="ban_member",description="Ban A Member",guild_ids=[779290532622893057])
    @commands.has_any_role("Owner", "Gawther", "Head Administrator", "Head Support", "Head Designer", "Head Developer")
    async def mem_ban(self, inter, member: disnake.Member, time: int, *, reason: str):
        guild_id = inter.guild.id
        
        embed = disnake.Embed(
            color=disnake.Colour.red(),
            timestamp=inter.created_at,
            title="{}'s Moderation System".format(self.bot.user.name),
            description="Member: {}\nStaff Member: {}\nType: Banned\nTime To Serve: {}".format(
                member.name, inter.author.name, str(time)
            )
        ).add_field(
            name="Reason",
            value=reason,
            inline=False
        ).set_footer(
            text="To Appeal This Decision, Please Use The '/appealban' command."
        ).set_thumbnail(url=self.bot.user.avatar)

        member_current_roles = member.roles
        ban_role = disnake.utils.get(inter.guild.roles, name="Banned")
        log_channel = disnake.utils.get(inter.guild.text_channels, name="ban_logs")

        with sql.connect('main.db') as mdb:
            cur = mdb.cursor()

            srch = 'SELECT bans FROM members WHERE id=?'
            val = (member.id,)

            current_count = cur.execute(srch, val).fetchone()

            if current_count:
                new_count = current_count[0] + 1

                srch2 = 'UPDATE members SET bans=? WHERE id=?'
                val2 = (new_count, member.id,)

                cur.execute(srch2, val2)

                total_logs = cur.execute('SELECT * FROM ban_logs').fetchall()

                ban_id = len(total_logs) + 1

                start = datetime.now()
                end = datetime.now() + timedelta(seconds=time)

                srch3 = 'INSERT INTO ban_logs(id,ban_id,staff,start_time,end_time,reason) VALUES (?,?,?,?,?,?)'
                val3 = (member.id, ban_id, inter.author.id, start, end, reason)

                cur.execute(srch3, val3)

                for channel in self.bot.get_guild(guild_id).voice_channels:
                    for mem in channel.members:
                        if mem.id == member.id:
                            await member.move_to(None)

                await member.send(embed=embed)
                await log_channel.send(embed=embed)
                await inter.response.send_message("Successfully Banned {}".format(member.name), ephemeral=True)
                await member.edit(roles=[ban_role])

                while time > 0:
                    await asyncio.sleep(1)
                    time -= 1
                else:
                    await member.edit(roles=member_current_roles)

                await member.send("Your Ban Has Been Lifted, {}".format(member.mention))
            else:
                new_count = 1

                srch2 = 'UPDATE members SET bans=? WHERE id=?'
                val2 = (new_count, member.id,)

                cur.execute(srch2, val2)

                total_logs = cur.execute('SELECT * FROM ban_logs').fetchall()

                ban_id = len(total_logs) + 1

                start = datetime.now()
                end = datetime.now() + timedelta(seconds=time)

                srch3 = 'INSERT INTO ban_logs(id,ban_id,staff,start_time,end_time,reason) VALUES (?,?,?,?,?,?)'
                val3 = (member.id, ban_id, inter.author.id, start, end, reason)

                cur.execute(srch3, val3)

                for channel in self.bot.get_guild(guild_id).voice_channels:
                    for mem in channel.members:
                        if mem.id == member.id:
                            await member.move_to(None)

                await member.send(embed=embed)
                await log_channel.send(embed=embed)
                await inter.response.send_message("Successfully Banned {}".format(member.name), ephemeral=True)
                await member.edit(roles=[ban_role])

                while time > 0:
                    await asyncio.sleep(1)
                    time -= 1
                else:
                    await member.edit(roles=member_current_roles)

                await member.send("Your Ban Has Been Lifted, {}".format(member.mention))

    # done
    @commands.slash_command(name="purge",description="Deletes _N_ Messages From The Channel Executed In",guild_ids=[779290532622893057])
    @commands.has_any_role("Owner", "Head Developer", "Head Administrator", "Head Designer", "Head Support")
    async def purge_message(self, inter, num: int, *, reason: str):
        await inter.response.send_message(f"Purging {num} Message", ephemeral=True)

        total = num
        
        for i in range(num):
            await inter.channel.purge(limit=1)
            await asyncio.sleep(1)
            total -= 1
            await inter.edit_original_message(f'{total}/{num} messages left to delete')

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

    @commands.slash_command(name="promote",description="Promote A Member To The Next Level!",guild_ids=[779290532622893057])
    @commands.has_any_role("Owner", "Head Developer", "Head Administrator")
    async def promote_member(self,inter,member:disnake.Member,*,reason:str):
        await inter.response.send_message("Promoting Member. . .",ephemeral=True)

        list_of_role_names = ["Community Helper","Support Staff","Moderator","Administrator"]
        list_of_top_roles = ["Head Support","Head Developer","Head Designer","Head Administrator"]

        if member.top_role.name in list_of_top_roles:
            await inter.edit_original_message("You Already Have A Head Role and Cannot Be Promoted Further!")
        elif member.top_role.name in list_of_role_names:
            x = member.top_role # used in embed below. don't erase
            new_role = disnake.utils.get(inter.guild.roles, name=list_of_role_names[list_of_role_names.index(member.top_role.name)+1])
            await member.remove_roles(member.top_role)
            await member.add_roles(new_role)

            log_channel = disnake.utils.get(inter.guild.text_channels, name="bot_logs")
            prom_channel = disnake.utils.get(inter.guild.text_channels, name="promotions")

            embed=disnake.Embed(
                color = disnake.Colour.random(),
                timestamp = inter.created_at,
                title = f"{self.bot.user.name}'s Member Promoter",
                description = f"{member.name} Has Been Promoted From {x.name} To {new_role.name} By {inter.author.name}"
            ).add_field(
                name = "Details",
                value = f"{reason}",
                inline=False
            ).set_thumbnail(url=self.bot.user.avatar)

            await log_channel.send(f'{inter.author.name} Has Promoted {member.name} From {x.name} To {new_role.name}')
            await prom_channel.send(embed=embed)
            await member.send(f'You Have Been Promoted! Check Out The {prom_channel.mention} For More Details!')
            await inter.edit_original_message("Member Has Been Promoted!")
        else:
            await inter.edit_original_message("Unsure of what error this would be")

def setup(bot):
    bot.add_cog(TierOneCommands(bot))