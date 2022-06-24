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

    @commands.slash_command(name="appeal_ban",description="Appeal A Log On Your Record")
    @commands.has_any_role("Head Developer","Banned","Kicked","Muted")
    async def appeal_ban(self,inter):
        if inter.channel.name == "how_to_appeal":
            view = BotView(self.bot)
            await inter.response.send_message("Please Select An Item Below", view=view)
        else:
            return await inter.response.send_message(
                "You Are Not In The {} Channel!".format(
                    self.bot.get_channel(987495649358520330).mention
            ), delete_after=30)
            

    @commands.slash_command(name="gen_help",description="Returns The General Help Menu")
    @commands.has_any_role(
        "Owner", "Gawther", "Head Administrator", "Head Developer",
        "Head Designer", "Head Support", "Administrator", "Moderator",
        "Support Staff", "Community Helper", "DND_DM", "DND PL", "Developers",
        "Designers", "Nitro Member", "Programming", "Gaming", "Member"
    )
    async def gen_help_menu(self,inter):
        titles = [
            "/listrules",
            "/ping",
            "/server",
            "/whois <member>",
            "/appeal_ban <type>"
        ]

        descrip = [
            "Returns a Paginator Embed displaying all the rules for the website and discord alike.",
            "Returns the bots latency. If this number is extremely high, please contact support.",
            "Returns information about the discord server including who the owner is, and members of each staff role.",
            "Returns a solid embed displaying information entered using the CURRENTLY BEING BUILT /create_profile command.",
            "Can only be executed in the #how_to_appeal text channel located in the Support category. Allows a user to determine whether they want to appeal a mute, ban, or kick log."
        ]

        embed = disnake.Embed(
            color = disnake.Colour.random(),
            timestamp = inter.created_at,
            title = "{}'s General Help Menu".format(inter.guild.name),
            description = "The Following Pages Will Show Available Commands and How To Use Them."
        ).set_thumbnail(
            url=inter.guild.icon
        )

        for i in range(len(titles)):
            embed_title = titles[i]
            embed_description = descrip[i]

            embed.add_field(
                name = embed_title,
                value = embed_description,
                inline = False
            )

        await inter.response.send_message(embed=embed, delete_after=90)


    @commands.slash_command(name = 'server',description = "Returns Info About Guild")
    @commands.has_any_role(
        "Owner", "Gawther", "Head Administrator", "Head Developer",
        "Head Designer", "Head Support", "Administrator", "Moderator",
        "Support Staff", "Community Helper", "DND_DM", "DND PL", "Developers",
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
            value="Created At: {}\nHead Robot: {}".format(created_at_corrected, self.bot.user.name),
            inline=False
        ).set_thumbnail(
            url = guild.icon
        ).set_footer(
            text = "To Apply For Any Of The _Applications Open_ Positions, Please [Click Here]()"
        )

        list_to_ignore = ["@everyone","Muted","Banned","Kicked","Member","Gaming","Programming","Designers","Developers","DND PL","DND_DM"]

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

    @commands.slash_command(name = 'ping',description = "Returns Bot Latency.")
    @commands.has_any_role(
        "Owner", "Gawther", "Head Administrator", "Head Developer",
        "Head Designer", "Head Support", "Administrator", "Moderator",
        "Support Staff", "Community Helper", "DND_DM", "DND PL", "Developers",
        "Designers", "Nitro Member", "Programming", "Gaming", "Member"
    )
    async def ping(self, inter):
        await inter.response.send_message('Latency Returned {}ms'.format(round(self.bot.latency * 1000)), ephemeral=True)


    @commands.slash_command(name="whois",description="Returns a profile on the user.")
    @commands.has_any_role(
        "Owner", "Gawther", "Head Administrator", "Head Developer",
        "Head Designer", "Head Support", "Administrator", "Moderator",
        "Support Staff", "Community Helper", "DND_DM", "DND PL", "Developers",
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
                value=f"""Current Experience: {user_items[1]}
                        Current Level: {user_items[2]}""",
                inline=False
            ).add_field(
                name="Favorite Things",
                value=f"""Color: {user_items[3]}
                        Animal: {user_items[4]}
                        Food: {user_items[5]}
                        Educational Subject: {user_items[6]}
                        Music Artist: {user_items[7]}
                        Art Artist: {user_items[8]}
                        Season: {user_items[9]}
                        Holiday: {user_items[10]}""",
                inline=False
            )

        await inter.response.send_message(embed=embed, ephemeral=True)
        

    @commands.slash_command(name="role_select",description="Assign Yourself A Role")
    @commands.has_any_role(
        "Owner", "Gawther", "Head Administrator", "Head Developer",
        "Head Designer", "Head Support", "Administrator", "Moderator",
        "Support Staff", "Community Helper", "DND_DM", "DND PL", "Developers",
        "Designers", "Nitro Member", "Programming", "Gaming", "Member"
    )
    async def select_role(self,inter,cmd:str,role_name:str):
        await inter.response.send_message("Adding You To {}. . . ".format(role_name),ephemeral=True)

        if inter.channel.id == 989236015992553472:
            if cmd == "add":
                if role_name == "Gaming" or role_name == "Programming":
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