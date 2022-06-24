import disnake

from disnake.ext import commands
from disnake.ext.commands import Cog
from Paginator import CreatePaginator


class StaffHelpMenus(Cog):
    def __init__(self,bot):
        self.bot = bot

    
    @commands.slash_command(name="staff_help",description="Returns a Paginator Help Menu For Available Staff Commands")
    @commands.has_any_role(
        "Owner", "Head Administrator", "Head Developer", "Head Support", "Head Designer",
        "Administrator", "Moderator", "Support Staff", "Community Helper"
    )
    async def staff_help_menu(self,inter):
        author_id = inter.author.id

        embed = disnake.Embed(
            color = disnake.Colour.random(),
            timestamp = inter.created_at,
            title = "{}'s Staff Help Menu".format(inter.guild.name),
            description = "All Available Staff Commands Are In The Pages That Follow."
        ).add_field(
            name="Commands That Required Member Argument",
            value="The member argument can be either the members id, or the members name. Do not use the members nickname!",
            inline=False
        ).add_field(
            name="Commands That Require Time Arguments",
            value="The time argument is built to be done in seconds. Please ensure you are using realistic time frames. Do not be like Kata and try to ban someone using PI for the seconds. It won't work!",
            inline=False
        ).add_field(
            name="Commands and Your Deparments",
            value="If you know that you do not have permissions to use certain commands, do not try and run them.\nStay In Your Lane! Each department has a Head role and then there are Administrators/Moderators/Community Helpers that help with the discord server in general. Head Support and Support Staff run ONLY the support category!",
            inline=False
        ).add_field(
            name="Purging Messages",
            value="Only Purge Messages When Needed! This means in case of LockDown, or spam attack!",
            inline=False
        ).add_field(
            name="Clock In/Out",
            value="You Must Have The clocked_out Role In Order To Use This Command. You Must Apply For This Role!"
        ).set_thumbnail(
            url = inter.guild.icon
        )

        titles = [
            "/warn_member <member> <reason>",
            "/mute_member <member> <time_in_seconds> <reason>",
            "/kick_member <member> <time_in_seconds> <reason>",
            "/ban_member <member> <time_in_seconds> <reason>",
            "/createrule <rule_name> <rule_info>",
            "/editrule <rule_number> <type> <replacement_info>",
            "/delrule <rule_number> <reason>",
            "/update_database",
            "/purge <whole_number> <reason>"
        ]

        descrip = [
            "Allows you to send a warning to a members direct messages.",
            "Allows you to mute a member which places them in the muted role for the duration of the time you entered. Please use this if warning a member does not work. Do not use discords built-in time-out, mute, kick, or ban commands. Those are for the Owner ONLY.",
            "Allows you to kick a member which places them in the kicked role for the duration fo the time you entered. Please use this if muting a member does not work. Do not use discords build-in time-out, mute, kick, or ban commands. Those are for the Owner ONLY.",
            "Allows you to ban a member which places them in the banned role for the duration fo the time you entered. Please use this if muting a member does not work. Do not use discords build-in time-out, mute, kick, or ban commands. Those are for the Owner ONLY.",
            "Allows ONLY The Owner, Head Administrator, and Head Developers to create new rules to be included in the `/listrules` command.",
            "Allows ONLY The Owner, Head Administrator, and Head Developers to edit rules to be included in the `/listrules` command.",
            "Allows ONLY The Owner, Head Administrator, and Head Developers to delete rules to be included in the `/listrules` command.",
            "Allows ONLY The Owner to delete and reset the database. This will only occur as a last resort to any type of attack against the discord server.",
            "Allows ONLY The Owner and 4 Head Roles to purge _N_ number of messages from the channel the command is executed in. This command does get logged to a log channel. **Do Not Abuse This Command Or It Will Be Removed!**"
        ]

        questions = [
            "What Happens When A Member Is Warned/Muted/Kicked/Banned?",
            "Why Doesn't The User Get Reconnected To The Voice Channel?",
            "How Does The Appeal Ban Command Work?"
        ]

        answers = [
            "When you execute the command, the bot stores a copy of the users current roles, then removes them. Once finished, it then gives the user the corresponding role. Then, the members profile for warn/mute/kick/ban counts is updated by 1, and the user receives a message from the bot in their dm's with the information as to why the command was executed. The warning command does not have a role.",
            "To be a dick about it, shouldn't have been muted, kicked, or banned. The user got in trouble, the user was removed for inappropriate behavior, therefore, the user can reconnect themselves.",
            "The command can only be executed in the #how_to_appeal text channel under the support category. The command starts by the user typing `/appeal_ban <type>` where type is either mute, kick, or ban. The user then receives messages with dropdowns showing each log and its details, one log per embed page. Afterwards, the user can select which number log they want to appeal, and given that they meet the requirements (go to the channel), then they can appeal the ban. Once the selection has been made, a preset channel under the Appeals category (under construction) will then alert the user that the channel has been appended to them, if a channel is avaialable. If not, they'll go into a que (future updates). If the decision is made to allow the appeal, then the record is deleted from the database, or `stricken from the record`"
        ]

        for j in range(len(titles)):
            embed_title = titles[j]
            embed_description = descrip[j]

            embed.add_field(
                name = embed_title,
                value = embed_description,
                inline=False
            ).set_thumbnail(
                url = inter.guild.icon
            )

        for i in range(len(questions)):
            embed_title = questions[i]
            embed_description = answers[i]

            embed.add_field(
                name = embed_title,
                value = embed_description,
                inline=False
            ).set_thumbnail(
                url = inter.guild.icon
            )

        await inter.response.send_message(embed=embed, delete_after=90)


def setup(bot):
    bot.add_cog(StaffHelpMenus(bot))