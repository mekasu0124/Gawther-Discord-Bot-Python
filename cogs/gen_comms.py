import disnake
import asyncio
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
                description="Appeal a Mute Log"
            ),
            disnake.SelectOption(
                label="Kick",
                description="Appeal A Kick Log"
            ),
            disnake.SelectOption(
                label="Ban",
                description="Appeal A Ban Log"
            )
        ]

        super().__init__(
            placeholder="Select One",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self,inter):
        with sql.connect('main.db') as mdb:
            cur = mdb.cursor()

            srch = f'SELECT {inter.values[0].lower()}_id FROM {inter.values[0].lower()}_logs WHERE id=?'
            val = (inter.author.id,)

            results = cur.execute(srch, val).fetchone()

            if results:
                print(results)
                log_channel = disnake.utils.get(inter.guild.text_channels, name="appeals")
                await log_channel.send(f":rotating_light:Incoming Appeal Request:rotating_light:\n{inter.author.name} is wanting to appeal a {inter.values[0]} log. Please pull them into a channel at your earliest convenience and use the `/mem_prof_staff <name/id>` command to see all relavent information.")
                await inter.response.edit_message("Your Request Has Been Sent. Please Be Patient And We Will Be With You As Soon As Possible.",view=None)
            else:
                return await inter.response.edit_message(f"You Do Not Have Any {inter.values[0]} Logs, {inter.author.mention}",view=None)


class GeneralCommands(Cog):
    def __init__(self,bot):
        self.bot = bot

    # done
    @commands.slash_command(name="appeal_ban",description="Appeal A Log On Your Record")
    @commands.has_any_role("Head Developer","Banned","Kicked","Muted")
    async def appeal_ban(self,inter):
        if inter.channel.name == "how_to_appeal":
            view = BotView(self.bot)
            await inter.response.send_message("Please Select An Item Below", view=view,ephemeral=True)
        else:
            mention_channel = disnake.utils.get(inter.guild.text_channels, name="how_to_appeal")
            return await inter.response.send_message(f"You Are Not In The {mention_channel.mention} Channel!", delete_after=30)


    # done
    @commands.slash_command(name = 'server',description = "Returns Info About Guild")
    @commands.has_any_role(
        "Owner", "Gawther", "Head Administrator", "Head Developer",
        "Head Designer", "Head Support", "Administrator", "Moderator",
        "Support Staff", "Community Helper", "DND DM", "DND PL", "Developers",
        "Designers", "Nitro Member", "Programming", "Gaming", "Member"
    )
    async def server(self, inter):
        guild = inter.guild
        created_at_corrected = guild.created_at.__format__("%m/%d/%Y - %H:%M:%S")

        embed = disnake.Embed(
            color=disnake.Colour.random(),
            title="{} Server Info".format(guild.name),
            description = "Below you can find information about {}".format(guild.name)
        ).add_field(
            name="Creation Information",
            value=f"Created At: {created_at_corrected}\nOwned By: {inter.guild.owner.name}\nHead Robot: {self.bot.user.name}",
            inline=False
        ).set_thumbnail(
            url = guild.icon
        ).set_footer(
            text = "To Apply For Any Of The _Applications Open_ Positions, Please [Click Here]()"
        )

        list_to_ignore = [
            "@everyone","Muted","Banned","Kicked","Member","Gaming","Programming",
            "Designers","Developers","DND PL","DND DM","clocked_in","clocked_out",
            "alpha","bravo","charlie","delta","echo","foxtrot","golf","hotel","india",
            "juliett"
        ]

        for role in guild.roles[::-1]:
            if role.managed or role.name in list_to_ignore:
                pass
            else:
                all_mems = ""

                for member in role.members:
                    if member:
                        name = member.name+', '
                        all_mems += name
                    else:
                        pass

                if all_mems == "":
                    embed.add_field(name=role.name,value="Applications Open",inline=False)
                else:
                    embed.add_field(name=role.name,value=all_mems,inline=False)

        await inter.response.send_message(embed=embed, ephemeral=True)


    # done
    @commands.slash_command(name = 'ping',description = "Returns Bot Latency.")
    @commands.has_any_role(
        "Owner", "Gawther", "Head Administrator", "Head Developer",
        "Head Designer", "Head Support", "Administrator", "Moderator",
        "Support Staff", "Community Helper", "DND DM", "DND PL", "Developers",
        "Designers", "Nitro Member", "Programming", "Gaming", "Member"
    )
    async def ping(self, inter):
        await inter.response.send_message('Latency Returned {}ms'.format(round(self.bot.latency * 1000)), ephemeral=True)


    # done
    @commands.slash_command(name="whois",description="Returns a profile on the user.")
    @commands.has_any_role(
        "Owner", "Gawther", "Head Administrator", "Head Developer",
        "Head Designer", "Head Support", "Administrator", "Moderator",
        "Support Staff", "Community Helper", "DND DM", "DND PL", "Developers",
        "Designers", "Nitro Member", "Programming", "Gaming", "Member"
    )
    async def whois(self, inter, member:disnake.Member=None):
        if member is None:
            member = inter.author
        else:
            member = member

        embed = disnake.Embed(
            color = disnake.Colour.random(),
            timestamp = inter.created_at,
            title = "Who Is {}?".format(member.name),
            description = "Below Is {}'s Profile Information".format(member.name)
        ).set_thumbnail(
            url = member.avatar
        )

        with sql.connect('main.db') as mdb:
            cur = mdb.cursor()

            srch = 'SELECT * FROM members WHERE id=?'
            val = (member.id,)

            user_items = cur.execute(srch, val).fetchall()[0]

            embed.add_field(
                name="General Information",
                value=f"""Member ID: {member.id}
                            Member Name: {member.name}
                            Member Nick: {member.nick}
                            Member Age: {user_items[-2]}
                            Member Birthday: {user_items[-1]}""",
                inline=False
            ).add_field(
                name="Account Information",
                value=f"""Current Experience: {user_items[2]}
                        Current Level: {user_items[3]}
                        Current Bank Balance: {user_items[1]}""",
                inline=False
            ).add_field(
                name="Favorite Things",
                value=f"""Color: {user_items[4]}
                        Animal: {user_items[5]}
                        Food: {user_items[6]}
                        Educational Subject: {user_items[7]}
                        Music Artist: {user_items[8]}
                        Art Artist: {user_items[9]}
                        Season: {user_items[10]}
                        Holiday: {user_items[11]}""",
                inline=False
            )

        await inter.response.send_message(embed=embed, ephemeral=True)

    
    # done
    @commands.slash_command(name="pay",description="Allows the user to pay a member owed money.")
    @commands.has_any_role(
        "Owner", "Gawther", "Head Administrator", "Head Developer",
        "Head Designer", "Head Support", "Administrator", "Moderator",
        "Support Staff", "Community Helper", "DND DM", "DND PL", "Developers",
        "Designers", "Nitro Member", "Programming", "Gaming", "Member"
    )
    async def pay(self,inter,member:disnake.Member,amount:float,*,reason:str):
        await inter.response.send_message("Please Wait While I Execute That Transaction. . .",ephemeral=True)
        with sql.connect('main.db') as mdb:
            cur = mdb.cursor()

            srch = 'SELECT bal FROM members WHERE id=?'
            val = (inter.author.id,)

            srch2 = 'SELECT bal FROM members WHERE id=?'
            val2 = (member.id,)

            author_bal = cur.execute(srch,val).fetchone()[0]
            member_bal = cur.execute(srch2,val2).fetchone()[0]

            if author_bal >= amount:
                new_author_bal = author_bal - amount
                new_member_bal = member_bal + amount

                author_bal = round(author_bal,2)
                member_bal = round(member_bal,2)
                new_author_bal = round(new_author_bal,2)
                new_member_bal = round(new_member_bal,2)
                amount = round(amount,2)

                srch3 = 'UPDATE members SET bal=? WHERE id=?'
                val3 = (new_author_bal,inter.author.id,)

                srch4 = 'UPDATE members SET bal=? WHERE id=?'
                val4 = (new_member_bal,member.id,)

                cur.execute(srch3, val3)
                cur.execute(srch4, val4)

                embed_author = disnake.Embed(
                    color = disnake.Colour.green(),
                    timestamp = inter.created_at,
                    title = f"{self.bot.user.name}'s Banking System",
                    description = f":money_with_wings:You Made A Payment!!!:money_with_wings:"
                ).add_field(
                    name = "Transaction Report",
                    value = f"""Payer: {inter.author.name}
                                Payee: {member.name}
                                Amount: {amount}GB
                                Date: {inter.created_at.__format__('%m/%d/%Y - %H:%M:%S')}""",
                    inline=False
                ).add_field(
                    name="Reason",
                    value=reason,
                    inline=False
                ).add_field(
                    name = "Account Updates",
                    value = f"""Starting Balance: {author_bal}GB
                                Amount Withdrawn: {amount}GB
                                New Balance: {new_author_bal}GB""",
                    inline = False
                ).set_thumbnail(url=inter.author.avatar)

                embed_member = disnake.Embed(
                    color = disnake.Colour.green(),
                    timestamp = inter.created_at,
                    title = f"{self.bot.user.name}'s Banking System",
                    description = ":money_with_wings:You Got Paid!!!:money_with_wings:"
                ).add_field(
                    name = "Transaction Report",
                    value = f"""Payer: {inter.author.name}
                                Payee: {member.name}
                                Amount: {amount}GB
                                Date: {inter.created_at.__format__('%m/%d/%Y - %H:%M:%S')}""",
                    inline=False
                ).add_field(
                    name="Reason",
                    value=reason,
                    inline=False
                ).add_field(
                    name = "Account Updates",
                    value = f"""Starting Balance: {member_bal}GB
                                Amount Deposited: {amount}GB
                                New Balance: {new_member_bal}GB""",
                    inline = False
                ).set_thumbnail(url=inter.author.avatar)

                await asyncio.sleep(5)

                log_channel = disnake.utils.get(inter.guild.text_channels,name="bot_logs")

                await inter.author.send(embed=embed_author)
                await member.send(embed=embed_member)
                await log_channel.send(f"{member.name} paid {inter.author.name} {amount}GB on {inter.created_at.__format__('%m/%d/%Y - %H:%M:%S')}")
                await inter.edit_original_message("Transaction Successful!")
            elif author_bal < amount:
                await inter.edit_original_message("You Cannot Have A Negative Balance!")
            else:
                await inter.edit_original_message("Member/Author Not Registered In Database. Contact Head Developers")

    
    # done
    @commands.slash_command(name="request",description="Allows the user to request payment from another member.")
    @commands.has_any_role(
        "Owner", "Gawther", "Head Administrator", "Head Developer",
        "Head Designer", "Head Support", "Administrator", "Moderator",
        "Support Staff", "Community Helper", "DND DM", "DND PL", "Developers",
        "Designers", "Nitro Member", "Programming", "Gaming", "Member"
    )
    async def request(self,inter,member:disnake.Member,amount:float,*,reason:str):
        await inter.response.send_message("Please Wait While I Execute That Transaction. . .",ephemeral=True)
        with sql.connect('main.db') as mdb:
            cur = mdb.cursor()

            srch = 'SELECT bal FROM members WHERE id=?'
            val = (inter.author.id,)

            srch2 = 'SELECT bal FROM members WHERE id=?'
            val2 = (member.id,)

            author_bal = cur.execute(srch,val).fetchone()[0]
            member_bal = cur.execute(srch2,val2).fetchone()[0]

            await member.send(f"{inter.author.name} is requesting {amount}GB from you in payment. Do you Accept or Decline? Response Will Timeout In 300 seconds")
            member_choice = await self.bot.wait_for('message',timeout=300)

            if member_choice.content.lower() == "accept":
                if author_bal >= amount:
                    new_author_bal = author_bal + amount
                    new_member_bal = member_bal - amount

                    author_bal = round(author_bal,2)
                    member_bal = round(member_bal,2)
                    new_author_bal = round(new_author_bal,2)
                    new_member_bal = round(new_member_bal,2)
                    amount = round(amount,2)

                    srch3 = 'UPDATE members SET bal=? WHERE id=?'
                    val3 = (new_author_bal,inter.author.id,)

                    srch4 = 'UPDATE members SET bal=? WHERE id=?'
                    val4 = (new_member_bal,member.id,)

                    cur.execute(srch3, val3)
                    cur.execute(srch4, val4)

                    embed_author = disnake.Embed(
                        color = disnake.Colour.green(),
                        timestamp = inter.created_at,
                        title = f"{self.bot.user.name}'s Banking System",
                        description = ":money_with_wings:You Got Paid!!!:money_with_wings:"
                    ).add_field(
                        name = "Transaction Report",
                        value = f"""Payer: {inter.author.name}
                                    Payee: {member.name}
                                    Amount: {amount}GB
                                    Date: {inter.created_at.__format__('%m/%d/%Y - %H:%M:%S')}""",
                        inline=False
                    ).add_field(
                        name="Reason",
                        value=reason,
                        inline=False
                    ).add_field(
                        name = "Account Updates",
                        value = f"""Starting Balance: {author_bal}GB
                                    Amount Deposited: {amount}GB
                                    New Balance: {new_author_bal}GB""",
                        inline = False
                    ).set_thumbnail(url=inter.author.avatar)

                    embed_member = disnake.Embed(
                        color = disnake.Colour.green(),
                        timestamp = inter.created_at,
                        title = f"{self.bot.user.name}'s Banking System",
                        description = ":money_with_wings:You Made A Payment!!!:money_with_wings:"
                    ).add_field(
                        name = "Transaction Report",
                        value = f"""Payer: {inter.author.name}
                                    Payee: {member.name}
                                    Amount: {amount}GB
                                    Date: {inter.created_at.__format__('%m/%d/%Y - %H:%M:%S')}""",
                        inline=False
                    ).add_field(
                        name="Reason",
                        value=reason,
                        inline=False
                    ).add_field(
                        name = "Account Updates",
                        value = f"""Starting Balance: {member_bal}GB
                                    Amount Withdrawn: {amount}GB
                                    New Balance: {new_member_bal}GB""",
                        inline = False
                    ).set_thumbnail(url=inter.author.avatar)

                    log_channel = disnake.utils.get(inter.guild.text_channels,name="bot_logs")

                    await inter.author.send(embed=embed_author)
                    await member.send(embed=embed_member)
                    await log_channel.send(f"{inter.author.name} paid {member.name} {amount}GB on {inter.created_at.__format__('%m/%d/%Y - %H:%M:%S')}")
                    await inter.edit_original_message("Transaction Successful!")
                elif author_bal < amount:
                    await inter.edit_original_message("You Cannot Have A Negative Balance!")
                else:
                    await inter.edit_original_message("Member/Author Not Registered In Database. Contact Head Developers")
            else:
                await member.send("You Selected Decline. Declining Transaction")
                await inter.edit_original_message(f"{member.name} has declined payment to you.")
    
    
    # done
    # keep updated
    @commands.slash_command(name="role_select",description="Assign Yourself A Role")
    @commands.has_any_role(
        "Owner", "Gawther", "Head Administrator", "Head Developer",
        "Head Designer", "Head Support", "Administrator", "Moderator",
        "Support Staff", "Community Helper", "DND DM", "DND PL", "Developers",
        "Designers", "Nitro Member", "Programming", "Gaming", "Member"
    )
    async def select_role(self,inter,cmd:str,role_name:str):
        await inter.response.send_message(f"Adding You To {role_name}. . . ",ephemeral=True)

        if inter.channel.name == "role_selection":
            if cmd == "add":
                if role_name.lower() == "gaming" or role_name.lower() == "programming":
                    for role in inter.author.roles:
                        if role_name == role.name:
                            await asyncio.sleep(0.5)
                            return await inter.edit_original_message("You Already Have That Role!")
                    
                    add_role = disnake.utils.get(inter.guild.roles,name=role_name)
                    await inter.author.add_roles(add_role)
                    await asyncio.sleep(0.5)
                    all_roles = []

                    for role in inter.author.roles:
                        if role.name == "@everyone":
                            pass
                        else:
                            all_roles.append(role.name)

                    await inter.edit_original_message(f"You've Been Added To The Role {add_role.name}. You're Now In The Following Roles: {', '.join(all_roles)}")
                else:
                    await inter.edit_original_message("You Are Not Allowed To Assign Yourself That Role!")
            elif cmd == "remove":
                if role_name == "Gaming" or role_name == "Programming":
                    rem_role = disnake.utils.get(inter.guild.roles,name=role_name)
                    await inter.author.remove_roles(rem_role)
                    await asyncio.sleep(0.5)
                    all_roles = []

                    for role in inter.author.roles:
                        if role.name == "@everyone":
                            pass
                        else:
                            all_roles.append(role.name)

                    await inter.edit_original_message(f"You Have Been Removed From {rem_role.name}. Your Roles Are: {', '.join(all_roles)}")
            else:
                await inter.edit_original_message("You Must Enter `add` or `remove` For The CMD Option!")
        else:
            return await inter.edit_original_message("You Are Not In The Appropriate Channel!")



def setup(bot):
    bot.add_cog(GeneralCommands(bot))