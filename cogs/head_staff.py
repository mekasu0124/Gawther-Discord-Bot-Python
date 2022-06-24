import disnake
import sqlite3 as sql

from disnake.ext import commands
from disnake.ext.commands import Cog
from Paginator import CreatePaginator


class BotView(disnake.ui.View):
    def __init__(self,bot:commands.Bot):
        super().__init__()
        self.bot = bot
        self.add_item(Dropdown())


class DropdownView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Dropdown())

    
class Dropdown(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(
                label="Mute",
                description="Select If User Has Selected A Mute Appeal"
            ),
            disnake.SelectOption(
                label="Kick",
                description="Select If User Has Selected A Kick Appeal"
            ),
            disnake.SelectOption(
                label="Ban",
                description="Select If User Has Selected A Ban Appeal"
            )
        ]

        super().__init__(
            placeholder="Select One",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self,inter):
        choice = inter.values[0]
        msg = await inter.channel.send("Enter Member's ID",view=None)
        iden = await inter.bot.wait_for('message')
        await msg.delete()
        await iden.delete()
        all_embeds = []
        titles = ["ID","Exp","Level","Warnings","Mutes","Kicks","Bans"]
        titles2 = ["ID","Log ID","Staff Member","Start Time","End Time","Reason"]

        if all(i.isnumeric() for i in iden.content):
            with sql.connect('main.db') as mdb:
                cur = mdb.cursor()

                srch = 'SELECT id,exp,level,warnings,mutes,bans,kicks FROM members WHERE Id=?'
                val = (iden.content,)

                srch2 = f'SELECT * FROM {choice.lower()}_logs WHERE id=?'
                val2 = (iden.content,)

                all_mem_info = cur.execute(srch, val).fetchall()
                all_log_info = cur.execute(srch2, val2).fetchall()

                embed = disnake.Embed(
                    color = disnake.Colour.random(),
                    timestamp = inter.created_at,
                    title = "General information",
                    description = "Account Information"
                )

                for title in titles:
                    embed.add_field(
                        name="\u200b",
                        value=f"{title}: {all_mem_info[0][titles.index(title)]}",
                        inline=False
                    )

                all_embeds.append(embed)

                if all_log_info:
                    embed2 = disnake.Embed(
                        color = disnake.Colour.random(),
                        timestamp = inter.created_at,
                        title = "Log Information",
                        description = f"Members {choice} Logs"
                    )

                    for title2 in titles2:
                        embed2.add_field(
                            name="\u200b",
                            value=f"{title2}: {all_log_info[0][titles2.index(title2)]}",
                            inline=False
                        )

                    all_embeds.append(embed2)
                    await inter.response.edit_message(embed=all_embeds[0],view=CreatePaginator(all_embeds[::-1],inter.author.id,timeout)) 
                else:
                    return await inter.response.edit_message("User Has No Log Info",view=None)
              

        else:
            return await inter.response.edit_message("User's ID Must Be An Integer (Whole Number)",view=None)


class TierOneCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    # owner and/or owner and head position commands

    @commands.slash_command(name="mem_prof_staff",description="Shows All Of The Designated Users Information That Is Stored In The Database.")
    @commands.has_any_role("Owner","Head Administrator","Head Support","Head Designer","Head Developer")
    async def show_profile(self,inter):
        if inter.channel.name == "appeal_discussion":
            view = BotView(self.bot)
            await inter.response.send_message("Select Type Of Member Appeal",view=view)
        else:
            ping = disnake.utils.get(inter.guild.text_channels, name="appeal_discussion")
            await inter.response.defer("Invalid Channel. {}".format(ping.mention), delete_after=30)

    @commands.slash_command(name="update_database",description="Updates Database To Insert Non-Existent Members")
    @commands.has_any_role("Owner","Head Developer")
    async def update_mems(self, inter):
        with sql.connect('main.db') as mdb:
            cur = mdb.cursor()

            for member in inter.guild.members:
                if not member.bot:
                    srch = 'INSERT INTO members(id,\
                        exp,level,color,animal,food,edu_subj,\
                            artist_music,artist_art,season,holiday,\
                                warnings,mutes,bans,kicks,age,dob) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
                    val = (member.id, 0, 0, "empty", "empty", "empty", "empty",
                           "empty", "empty", "empty", "empty", 0, 0, 0, 0, 0, "empty")
                    cur.execute(srch, val)

        await inter.response.send_message("Finished Updating Members & Database", ephemeral=True)

    @commands.slash_command(name="ban_member",description="Ban A Member")
    @commands.has_any_role("Owner", "Gawther", "Head Administrator", "Head Support", "Head Designer", "Head Developer")
    async def mem_ban(self, inter, member: disnake.Member, time: int, *, reason: str):
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


def setup(bot):
    bot.add_cog(TierOneCommands(bot))