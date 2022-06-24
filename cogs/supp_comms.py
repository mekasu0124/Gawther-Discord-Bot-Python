import disnake 
import asyncio
import json

from disnake.ext import commands
from disnake.ext.commands import Cog
from datetime import date

"""FIRST VIEW IS THE BOT VIEW."""
class BotView(disnake.ui.View):
    def __init__(self, bot:commands.Bot):
        super().__init__()
        self.bot = bot
        self.add_item(Dropdown())

"""BELONGS TO BOTVIEW"""
class DropdownView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Dropdown())

"""BELONGS TO BOTVIEW"""
class Dropdown(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(label = "Discord Support",description = "Follow On-Screen Prompts For Assistance Within The Discord Platform"),
            disnake.SelectOption(label = "Website Support",description = "Follow On-Screen Prompts For Assistance Within The Website Platform")
        ]

        super().__init__(
            placeholder="Select One",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self,inter):
        if inter.values[0] == "Discord Support":
            view = DiscordSupportView()
            await inter.response.edit_message("Please Select A Sub-Category Below ",view=view)
        elif inter.values[0] == "Website Support":
            view = WebsiteSupportView()
            await inter.response.edit_message("Please Select A Sub-Category Below",view=view)
        else:
            await inter.response.edit_message("Invalid Category. Report To Staff")

"""SECOND VIEW IS THE DISCORD SUPPORT VIEW."""
class DiscordSupportView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Dropdown2())

"""BELONGS TO DISCORDSUPPORTVIEW"""
class Dropdown2(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(label = "Roles", description="Get Support With Your Current Role(s)"),
            disnake.SelectOption(label = "Voice", description="Get Support With Voice Channels"),
            disnake.SelectOption(label = "Text", description="Get Support With Text Channels"),
            disnake.SelectOption(label = "Categories", description="Get Support With A Category")
        ]

        super().__init__(
            placeholder="Select One",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self,inter):
        value = inter.values[0]

        embed = disnake.Embed(
            color = disnake.Colour.random(),
            timestamp = inter.created_at,
            title = "The Channel Now Belongs To {}. I have Gotten Them Started For You <3".format(inter.author.name),
            description = """Member ID: {}
                             Member Name: {}
                             Member Nick: {}
                             Category: Discord Support
                             Sub-Category: {}""".format(
                                 inter.author.id,
                                 inter.author.name,
                                 inter.author.nick,
                                 value
                             )
        ).add_field(
            name = "What Do I Do Now?",
            value = """Please enter as much information as you can for our support 
                       team to be able to help you with the best accuracy possible. 
                       Once you've submitted your information, PLEASE BE PATIENT. 
                       No one gets paid, and therefore will not be rushed. If it is an
                       emergency, call 9-1-1.""",
            inline = False
        ).set_thumbnail(url = inter.guild.icon)

        member = inter.author
        avai_cat = disnake.utils.get(inter.guild.categories, name="Available Support Channels")
        occu_cat = disnake.utils.get(inter.guild.categories, name="Occupied Support Channels")
        new_role_name = avai_cat.text_channels[0].name

        if new_role_name:
            new_role = []

            for role in inter.guild.roles:
                if role.name == new_role_name:
                    new_role.append(role)
                    break

            ping_role = disnake.utils.get(inter.guild.roles, name="clocked_in")
            await member.add_roles(new_role[0])

            for channel in inter.guild.text_channels:
                if channel.name == new_role_name:
                    await channel.edit(category=occu_cat)
                    a = "{}, Please enter in as many details as possible".format(inter.author.mention)
                    b = a + ' ' + "Whoemever is {} will be with you shortly :) <3".format(ping_role.mention)
                    await channel.send(b)
                    return await inter.response.edit_message("You've Been Mentioned In The Appropriate Channel", view=None)
        else:
            return await inter.response.edit_message("The Que System For Our Support Area Has Not Been Setup Yet. Please Wait For An Available Channel", view=None)


"""SECOND_ALPHA VIEW IS THE WEBSITE SUPPORT VIEW"""
class WebsiteSupportView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Dropdown3())

"""BELONGS TO WEBSITESUPPORTVIEW"""
class Dropdown3(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(label="Forums", description="Get Support With Website Forum Actions"),
            disnake.SelectOption(label="Sign Up", description="Get Support With Signing Up For The Website"),
            disnake.SelectOption(label="Shop", description="Get Support With The Websites' Online Shop")
        ]

        super().__init__(
            placeholder="Select One",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self,inter):
        value = inter.values[0]

        if value == "Shop":
            return await inter.response.edit_message("The Online Shop For The Website Has Not Been Setup Yet.",view=None)
        elif value == "Sign Up":
            return await inter.response.edit_message("The Sign Up Process For The Website Has Not Been Setup Yet.", view=None)
        elif value == "Forums":
            return await inter.response.edit_message("The Forums For The Website Has Not Been Setup Yet.",view=None)
        else:
            return await inter.response.edit_message("Something went wrong. Contact Support",view=None)

class SupportFunctions(Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.slash_command(name="support",description="Get Support For Either Discord, Or The Website")
    @commands.has_any_role(
        "Owner", "Gawther", "Head Administrator", "Head Developer",
        "Head Designer", "Head Support", "Administrator", "Moderator",
        "Support Staff", "Community Helper", "DND_DM", "DND PL", "Developers",
        "Designers", "Nitro Member", "Programming", "Gaming", "Member"
    )
    async def get_support(self,inter):
        view = BotView(self.bot)
        await inter.response.send_message("Please Select A Category Below", view=view, ephemeral=True)


    @commands.slash_command(name="close",description="close your support channel")
    async def move_dormant(self,inter):
        await inter.response.send_message("Channel Is Closing! Please Do Not Type Into Channel!")
        all_messages = await inter.channel.history(limit=None).flatten()
        rem_role = disnake.utils.get(inter.guild.roles,name=inter.channel.name)

        all_roles = []

        for role in inter.author.roles:
            all_roles.append(role.name)

        if inter.channel.name in all_roles:
            await inter.edit_original_message(":rotating_light:CLOSING CHANNEL STOP TYPING!!!:rotating_light:")
            await inter.author.remove_roles(rem_role)

            with open(f'./support_files/{inter.author.name}_support.txt','w') as file:
                all_messages = await inter.channel.history(limit=None).flatten()

                for message in all_messages:
                    file.write(f'Author: {message.author.name}\nDate: {message.created_at}\nMessage: {message.content}\n================================================\n')
                    await message.delete()

            with open(f'./support_files/{inter.author.name}_support.txt','rb') as file:
                embed = disnake.Embed(
                    color = disnake.Colour.random(),
                    timestamp = inter.created_at,
                    title = "Your Support File",
                    description = "Your Support File Is Ready For Downloading. Please Download Your File Now, Otherwise, On Sunday It Will Be Deleted."
                ).set_thumbnail(url=inter.guild.icon)

                for member in self.bot.get_guild(inter.guild.id).members:
                    if member.id == inter.author.id:
                        await member.send(embed=embed,file=disnake.File(file, f'{inter.author.name}_support.txt'))
                        break

            avail_cat = disnake.utils.get(inter.guild.categories,name="Available Support Channels")
            await inter.channel.edit(category=avail_cat)
            return await inter.channel.send(f'{inter.channel.name} Has Been Reset And Is Ready To Use')
        elif "clocked_in" in all_roles:
            await inter.edit_original_message(":rotating_light:CLOSING CHANNEL STOP TYPING!!!:rotating_light:")
            
            await inter.channel.send("Enter The ID Of The User Who Ran The Support Command, {}".format(inter.author.mention))
            user_id = await self.bot.wait_for('message')

            if all(i.isnumeric() for i in user_id.content):
                for member in inter.guild.members:
                    if member.id == int(user_id.content):
                        await member.remove_roles(rem_role)

                        with open(f'./support_files/{member.name}_support.txt', 'w') as file:
                            all_messages = await inter.channel.history(limit=None).flatten()

                            for message in all_messages:
                                file.write(f'Author: {message.author.name}\nDate: {message.created_at}\nMessage: {message.content}\n================================================\n')
                                await message.delete()

                        with open(f'./support_files/{member.name}_support.txt','rb') as file:
                            embed = disnake.Embed(
                                color = disnake.Colour.random(),
                                timestamp = inter.created_at,
                                title = "Your Support File",
                                description = "Your Support File Is Ready For Downloading. Please Download Your File Now, Otherwise, On Sunday It Will Be Deleted."
                            ).set_thumbnail(url=inter.guild.icon)

                            await member.send(embed=embed,file=disnake.File(file, f'{inter.author.name}_support.txt'))
                            break
                avail_cat = disnake.utils.get(inter.guild.categories,name="Available Support Channels")
                await inter.channel.edit(category=avail_cat)
                return await inter.channel.send(f'{inter.channel.name} Has Been Reset And Is Ready TO Use')

            else:
                return await inter.edit_original_message("That is not an ID. If you are entering in an ID and are getting this message, contact the developers")
        else:
            await inter.edit_original_message("You Are Not Staff or The Member Needing Support. You Cannot Close This Channel!")


    @commands.slash_command(name="clock",description="Clock In or Out For Helping With Support")
    @commands.has_any_role(
        "Owner", "Head Administrator", "Head Support", "Head Designer", "Head Developer",
        "Administrator", "Moderator", "Support Staff", "Community Helper"
    )
    async def clock_functions(self,inter,opt:str):
        await inter.response.send_message("One Moment While I Try That. . .",ephemeral=True)

        if opt == "in":
            if "clocked_in" in inter.author.roles:
                return await inter.edit_original_message("You've Already Been Clocked In/Out!")
            else:
                add_role = disnake.utils.get(inter.guild.roles,name="clocked_in")
                rem_role = disnake.utils.get(inter.guild.roles,name="clocked_out")
                await inter.author.remove_roles(rem_role)
                await inter.author.add_roles(add_role)
                return await inter.edit_original_message("You've Been Clocked In")
        else:
            add_role = disnake.utils.get(inter.guild.roles,name="clocked_out")
            rem_role = disnake.utils.get(inter.guild.roles,name="clocked_in")
            await inter.author.remove_roles(rem_role)
            await inter.author.add_roles(add_role)
            return await inter.edit_original_message("You Have Been Clocked Out! Have A Great Day!")
                

def setup(bot):
    bot.add_cog(SupportFunctions(bot))
