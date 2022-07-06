import disnake
import asyncio
import sqlite3 as sql

from disnake.ext import commands
from disnake.ext.commands import Cog
from datetime import datetime, timedelta


class TierFourCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    # Support Staff, Community Helper commands

    @commands.slash_command(name="kick_member",description="Kick A Member",guild_ids=[779290532622893057])
    @commands.has_any_role(
        "Owner", "Head Administrator", "Head Support", "Head Designer", "Head Developer",
        "Administrator", "Moderator"
    )
    async def mem_kick(self,inter,member:disnake.Member,time:int,*,reason:str):
        guild_id = inter.guild.id
        
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

    # done
    @commands.slash_command(name="adjust_balance",description="Adjust A Members Balance",guild_ids=[779290532622893057])
    @commands.has_any_role(
        "Owner", "Head Administrator", "Head Support", "Head Designer", "Head Developer",
        "Administrator", "Moderator"
    )
    async def adj_bal(self,inter,member:disnake.Member,cmd:str,amount:float,*,reason:str):
        await inter.response.send_message("Please Wait While I Execute That Transaction. . .",ephemeral=True)

        embed = disnake.Embed(
            color = disnake.Colour.green(),
            timestamp = inter.created_at,
            title = f"{self.bot.user.name}'s Banking System",
            description = f"{inter.author.name} Has Adjusted Your Balance"
        ).add_field(
            name = "Transaction Details",
            value = f"""Staff: {inter.author.name}
                        Member: {member.name}
                        Action: Balance Adjustment""",
            inline = False
        ).add_field(
            name = "Reason",
            value = reason,
            inline = False
        ).set_thumbnail(url = self.bot.user.avatar)

        with sql.connect('main.db') as mdb:
            cur = mdb.cursor()

            srch = 'SELECT bal FROM members WHERE id=?'
            val = (member.id,)

            member_balance = cur.execute(srch, val).fetchone()[0]

            if cmd == "deposit":
                new_bal = member_balance + amount

                srch3 = 'UPDATE members SET bal=? WHERE id=?'
                val3 = (new_bal,member.id,)

                cur.execute(srch3, val3)

                member_balance = round(member_balance,2)
                new_bal = round(new_bal,2)

                embed.add_field(
                    name = "Balance Information",
                    value = f"""Starting Balance: {member_balance}GB
                                Adjusted By: {amount}GB
                                Ending Balance: {new_bal}GB""",
                    inline = False
                )

                await asyncio.sleep(5)

                log_channel = disnake.utils.get(inter.guild.text_channels, name="bot_logs")

                await log_channel.send(f"{inter.author.name} Adjusted {member.name}s' Balance By {amount}GB For The Reason Of {reason}.")
                await member.send(embed=embed)
                await inter.edit_original_message("Transaction Successful")
            elif cmd == "withdrawl":
                new_bal = member_balance - amount

                srch3 = 'UPDATE members SET bal=? WHERE id=?'
                val3 = (new_bal, member.id,)

                cur.execute(srch3, val3)

                member_balance = round(member_balance,2)
                new_bal = round(new_bal,2)

                embed.add_field(
                    name = "Balance Information",
                    value = f"""Starting Balance: {member_balance}GB
                                Adjusted By: {amount}GB
                                Ending Balance: {new_bal}GB""",
                    inline = False
                )

                await asyncio.sleep(5)

                log_channel = disnake.utils.get(inter.guild.text_channels, name="bot_logs")

                await log_channel.send(f"{inter.author.name} Adjusted {member.name}s' Balance By {amount}GB For The Reason Of {reason}.")
                await member.send(embed=embed)
                await inter.edit_original_message("Transaction Successful")
            else:
                await inter.edit_original_message(f"You Must Enter `deposit` or `withdrawl` For The Action, {inter.author.mention}")

    
def setup(bot):
    bot.add_cog(TierFourCommands(bot))
