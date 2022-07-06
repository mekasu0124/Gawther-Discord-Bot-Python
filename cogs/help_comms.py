import disnake
import asyncio
import sqlite3 as sql

from disnake.ext import commands
from disnake.ext.commands import Cog
from Paginator import CreatePaginator


class GeneralHelpMenu(Cog):
    def __init__(self,bot):
        self.bot = bot
        
        
    # done
    # keep updating
    @commands.slash_command(name="gen_help",description="Returns The General Help Menu",guild_ids=[779290532622893057])
    @commands.has_any_role(
        "Owner", "Gawther", "Head Administrator", "Head Developer",
        "Head Designer", "Head Support", "Administrator", "Moderator",
        "Support Staff", "Community Helper", "DND DM", "DND PL", "Developers",
        "Designers", "Nitro Member", "Programming", "Gaming", "Member"
    )
    async def gen_help_menu(self,inter):
        titles = [
            "/listrules",
            "/ping",
            "/server",
            "/whois <member>",
            "/appeal_ban <type>",
            "/close",
            "/support",
            "/role_select <add/remove> <role name>",
            "/gen_help",
            "/pay <member> <amount> <reason>",
            "/request <member> <amount> <reason>"
        ]

        descrip = [
            "Returns a Paginator Embed displaying all the rules for the website and discord alike.",
            "Returns the bots latency. If this number is extremely high, please contact support.",
            "Returns information about the discord server including who the owner is, and members of each staff role.",
            "Returns a solid embed displaying information entered using the CURRENTLY BEING BUILT /create_profile command.",
            "Can only be executed in the #how_to_appeal text channel located in the Support category. Allows a user to determine whether they want to appeal a mute, ban, or kick log.",
            "If you've opened a support channel, here's how you close it! This command can only be executed by the member who opened the support channel, or any staff member that is clocked in.",
            "In need of assistance? Create a support channel in the #how_to_support channel under the Support category by executing `/support`",
            "Are you a new member? Go to the Information category at the top left side of your screen, and click the #role_selection channel and use this command with the available roles already listed :)",
            "Returns a help menu to the user ephemerally (only the user can see it) to help show a list of available commands.",
            "Do you owe someone money? Pay Up!",
            "Does someone owe you money? Request them to pay up!"
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

        await inter.author.send(embed=embed)
        await inter.edit_original_message(f"{inter.author.mention} Check Your DM's")


    # done
    @commands.slash_command(name="hstaff_help",description="Returns a Paginator Help Menu For Available Staff Commands",guild_ids=[779290532622893057])
    @commands.has_any_role(
        "Owner", "Head Administrator", "Head Developer", "Head Support", "Head Designer",
        "Administrator", "Moderator", "Support Staff", "Community Helper"
    )
    async def high_staff_help(self,inter):
        titles = [
            "/ban_member <member> <time> <reason>",
            "/purge <amount> <reason>",
            "/promote <member>",
            "/create_rule <rule_name> <rule_info>",
            "/edit_rule <rule_num> <title/rule> <new_info>",
            "/delete_rule <rule_num> <reason>"
        ]

        descrip = [
            "Places the member in the Banned role for the duration of the time in seconds you entered when executing the command.",
            "Deletes the entered amount of messages from the channel that the command in executed in. Use with caution!",
            "Promotes a member to the next role available in the set given roles. See #staff_announcements",
            "Creates a new rule and adds it to the database",
            "Edits an existing rule and then updates the database.",
            "Deletes an existsing rule and then removes it from the database."
        ]

        embed = disnake.Embed(
            color = disnake.Colour.random(),
            timestamp = inter.created_at,
            title = "{}'s High Tier Staff Help Menu".format(inter.guild.name),
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

        await inter.author.send(embed=embed)
        await inter.edit_original_message(f"{inter.author.mention} Check Your DM's")

    # done
    @commands.slash_command(name="mstaff_help",description="Returns a Paginator Help Menu For Available Staff Commands",guild_ids=[779290532622893057])
    @commands.has_any_role(
        "Owner", "Head Administrator", "Head Developer", "Head Support", "Head Designer",
        "Administrator", "Moderator"
    )
    async def mid_staff_help(self,inter):
        titles = [
            "/kick_member",
            "/adjust_balance"
        ]

        descrip = [
            "Places the member in the kicked role for the duration of the time entered when the command was executed.",
            "Increases/Decreases the members balance by the desired amount."
        ]

        embed = disnake.Embed(
            color = disnake.Colour.random(),
            timestamp = inter.created_at,
            title = "{}'s Mid Tier Staff Help Menu".format(inter.guild.name),
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

        await inter.author.send(embed=embed)
        await inter.edit_original_message(f"{inter.author.mention} Check Your DM's")

    # done
    @commands.slash_command(name="lstaff_help",description="Returns a Paginator Help Menu For Available Staff Commands",guild_ids=[779290532622893057])
    @commands.has_any_role(
        "Owner", "Head Administrator", "Head Developer", "Head Support", "Head Designer",
        "Administrator", "Moderator", "Support Staff", "Community Helper"
    )
    async def low_staff_help(self,inter):
        titles = [
            "/mute_member <member> <time> <reason>",
            "/warn_member <member> <reason>",
            "/clock <in/out>"
        ]

        descrip = [
            "Places the member in the muted role for the amount of time entered when the command was executed.",
            "Send a warning to the member if they're acting inappropriately",
            "Allows anyone with the clocked_in/clocked_out role to clock in or out. You must be clocked in to assist with support channels."
        ]

        embed = disnake.Embed(
            color = disnake.Colour.random(),
            timestamp = inter.created_at,
            title = "{}'s Low Tier Help Menu".format(inter.guild.name),
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

        await inter.author.send(embed=embed)
        await inter.edit_original_message(f"{inter.author.mention} Check Your DM's")

    # done
    @commands.slash_command(name="ostaff_help",description="Returns a Paginator Help Menu For Available Staff Commands",guild_ids=[779290532622893057])
    @commands.has_any_role("Owner", "Head Developer")
    async def owner_help(self,inter):
        titles = [
            "/update_database"
        ]

        descrip = [
            "Resets the bot's database by re-writing every user in the database back to zero count on all items."
        ]

        embed = disnake.Embed(
            color = disnake.Colour.random(),
            timestamp = inter.created_at,
            title = "{}'s Owner Help Menu".format(inter.guild.name),
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

        await inter.author.send(embed=embed)
        await inter.edit_original_message(f"{inter.author.mention} Check Your DM's")


def setup(bot):
    bot.add_cog(GeneralHelpMenu(bot))