import disnake

from disnake.ext import commands
from disnake.ext.commands import Cog


class PromotionCommand(Cog):
    def __init__(self,bot):
        self.bot = bot


    @commands.slash_command(name="promote",description="Promote A Member To The Next Level!",guild_ids=[779290532622893057])
    @commands.has_any_role("Owner", "Head Developer", "Head Administrator")
    async def promote_member(self,inter,member:disnake.Member):
        await inter.response.send_message("Promoting Member. . .",ephemeral=True)
        curr_mem_roles = []

        for role in member.roles:
            curr_mem_roles.append(role.name)

        log_channel = disnake.utils.get(inter.guild.text_channels,name="bot_logs")
        prom_channel = disnake.utils.get(inter.guild.text_channels,name="promotions")

        if "Community Member" in curr_mem_roles:
            if "Support Staff" in curr_mem_roles:
                if "Moderator" in curr_mem_roles:
                    if "Administrator" in curr_mem_roles:
                        await inter.edit_original_message("You Are The Highest Promotable Role. You Will Need To Apply For A Head Position")
                    else:
                        prom_role = disnake.utils.get(inter.guild.roles,name="Administrator")
                        clock_role = disnake.utils.get(inter.guild.roles,name="clocked_out")

                        await member.add_roles(prom_role)
                        await member.add_roles(clock_role)

                        embed = disnake.Embed(
                            color = disnake.Colour.green(),
                            timestamp = inter.created_at,
                            title = f"{member.name} Has Been Promoted!",
                            description = f"{member.name} Has Been Promoted To {prom_role.name}! Let's Give Them A Round Of Applause!"
                        ).set_thumnail(url=member.avatar)

                        await log_channel.send(f"{inter.author.name} Has Promoted {member.name} To {prom_role.name}")
                        await prom_channel.send(f"{inter.guild.default_role.mention}",embed=embed)
                        return inter.edit_original_message("Promotion Successful")
                else:
                    prom_role = disnake.utils.get(inter.guild.roles,name="Moderator")
                    clock_role = disnake.utils.get(inter.guild.roles,name="clocked_out")

                    await member.add_roles(prom_role)
                    await member.add_roles(clock_role)

                    embed = disnake.Embed(
                        color = disnake.Colour.green(),
                        timestamp = inter.created_at,
                        title = f"{member.name} Has Been Promoted!",
                        description = f"{member.name} Has Been Promoted To {prom_role.name}! Let's Give Them A Round Of Applause!"
                    ).set_thumbnail(url=member.avatar)

                    await log_channel.send(f"{inter.author.name} Has Promoted {member.name} To {prom_role.name}")
                    await prom_channel.send(f"{inter.guild.default_role.mention}",embed=embed)
                    await inter.edit_original_message("Promotion Successful")
            else:
                prom_role = disnake.utils.get(inter.guild.roles,name="Support Staff")
                clock_role = disnake.utils.get(inter.guild.roles,name="clocked_out")

                await member.add_roles(prom_role)
                await member.add_roles(clock_role)

                embed = disnake.Embed(
                    color = disnake.Colour.green(),
                    timestamp = inter.created_at,
                    title = f"{member.name} Has Been Promoted!",
                    description = f"{member.name} Has Been Promoted To {prom_role.name}! Let's Give Them A Round Of Applause!"
                ).set_thumbnail(url=member.avatar)

                await log_channel.send(f'{inter.author.name} Has Promoted {member.name} To {prom_role.name}')
                await prom_channel.send(f"{inter.guild.default_role.mention}",embed=embed)
                await inter.edit_original_message("Promotion Successful")
        else:
            prom_role = disnake.utils.get(inter.guild.roles,name="Community Helper")
            clock_role = disnake.utils.get(inter.guild.roles,name="clocked_out")

            await member.add_roles(prom_role)
            await member.add_roles(clock_role)

            embed = disnake.Embed(
                color = disnake.Colour.green(),
                timestamp = inter.created_at,
                title = f"{member.name} Has Been Promoted!",
                description = f"{member.name} Has Been Promoted To {prom_role.name}! Let's Give Them A Round Of Applause!"
            ).set_thumbnail(url=member.avatar)

            await log_channel.send(f'{inter.author.name} Has Promoted {member.name} To {prom_role.name}')
            await prom_channel.send(f"{inter.guild.default_role.mention}",embed=embed)
            await inter.edit_original_message("Promotion Successful")


def setup(bot):
    bot.add_cog(PromotionCommand(bot))