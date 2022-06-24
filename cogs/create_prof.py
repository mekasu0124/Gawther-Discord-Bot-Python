import disnake
import asyncio
import sqlite3 as sql

from disnake.ext import commands 
from disnake.ext.commands import Cog


class CreateProfile(Cog):
    def __init__(self,bot):
        self.bot = bot


    @commands.slash_command(name="create_profile",description="Allows A User To Create A Profile")
    async def create_prof(self,inter):
        member = inter.author

        for role in inter.author.roles:
            if role.name == "Muted" or role.name == "Kicked" or role.name == "Banned":
                return await inter.response.send_message("You Are Not Allowed To Execute This Command!")

        await inter.response.send_message("{}, you have been sent a DM".format(inter.author.mention),ephemeral=True)

        await asyncio.sleep(0.5)

        embed = disnake.Embed(
            color = disnake.Colour.random(),
            timestamp = inter.created_at,
            title = "{}'s Profile Creator".format(inter.guild.name),
            description = "Creating A Profile - Read Below"
        ).add_field(
            name = "Start Information",
            value = "A few things to remember while creating your profile.",
            inline = False
        ).add_field(
            name = "Timed Responses",
            value = "Response are set to time-out if you do not respond within 30 seconds. This is to keep the bot from getting hungup on the thread of your command instance for an unsubstantial amount of time.",
            inline = False
        ).add_field(
            name = "Response Requirements",
            value = "All responses must be legible and using the 26 English Letter Alphabet and/or numbers from 0-9. Do not use special alt codes/characters will not be allowed!",
            inline=False
        ).add_field(
            name = "Getting Started",
            value = "In 30 seconds, this embed will update with the first question which will get you started on your way with creating your profile. Remember, respond to each question within 30 seconds, or you'll have to start over! Good Luck!"
        ).add_field(
            name = "Last Note:",
            value = "If you choose to not answer a question, or leave a question blank, please enter None for the answer!",
            inline = False
        ).set_thumbnail(url=self.bot.user.avatar)

        msg = await member.send(embed=embed)

        # await asyncio.sleep(28) # change back
        await asyncio.sleep(3)

        embed.add_field(
            name = "Question #1",
            value = "What's your favorite color?",
            inline = False
        )

        await msg.edit(embed=embed)

        fav_col = await self.bot.wait_for('message',timeout=30)

        if all(i.isalpha() for i in fav_col.content):
            embed2 = disnake.Embed(
                color = disnake.Colour.random(),
                timestamp = inter.created_at,
                title = "{}'s Profile Creator".format(inter.guild.name),
                description = "Your Profile So Far"
            ).add_field(
                name = "Question #1",
                value = f"What Is Your Favorite Color?\n{fav_col.content}",
                inline = False
            ).set_thumbnail(url=self.bot.user.avatar)


            await msg.edit(embed=embed2)

            msg2 = await member.send("What Is Your Favorite Animal?")
            fav_anim = await self.bot.wait_for('message',timeout=30)

            if all(i.isalpha() for i in fav_anim.content):
                embed2.add_field(
                    name = 'Question #2',
                    value = f"What Is Your Favorite Animal?\n{fav_anim.content}",
                    inline = False
                )

                await msg.edit(embed=embed)
                await msg2.edit("What Is Your Favorite Food?")
                fav_food = await self.bot.wait_for('message',timeout=30)

                if all(i.isalpha() for i in fav_food.content):
                    embed2.add_field(
                        name = 'Question #3',
                        value = f"What Is Your Favorite Food?\n{fav_food.content}",
                        inline = False
                    )

                    await msg.edit(embed=embed)
                    await msg2.edit("What Is Your Favorite Educational Subject?")
                    fav_sub = await self.bot.wait_for('message',timeout=30)

                    if all(i.isalpha() for i in fav_sub.content):
                        embed2.add_field(
                            name = 'Question #4',
                            value = f"What Is Your Favorite Educational Subject?\n{fav_sub.content}",
                            inline = False
                        )

                        await msg.edit(embed=embed2)
                        await msg2.edit("Who Is Your Favorite Music Artist?")
                        fav_music_art = await self.bot.wait_for('message',timeout=30)

                        if all(i.isprintable() for i in fav_music_art.content):
                            embed2.add_field(
                                name = 'Question #5',
                                value = f"Who Is Your Favorite Music Artist?\n{fav_music_art.content}",
                                inline = False
                            )

                            await msg.edit(embed=embed2)
                            await msg2.edit("Who Is Your Favorite Art Artist?")
                            fav_art_artist = await self.bot.wait_for('message',timeout=30)

                            if all(i.isalpha() for i in fav_art_artist.content):
                                embed2.add_field(
                                    name = 'Question #6',
                                    value = f"Who Is Your Favorite Art Artist?\n{fav_art_artist.content}",
                                    inline = False
                                )

                                await msg.edit(embed=embed2)
                                await msg2.edit("When Is Your Favorite Season?")
                                fav_season = await self.bot.wait_for('message',timeout=30)

                                if all(i.isalpha() for i in fav_season.content):
                                    embed2.add_field(
                                        name = 'Question #7',
                                        value = f"When Is Your Favorite Season?\n{fav_season.content}",
                                        inline = False
                                    )

                                    await msg.edit(embed=embed2)
                                    await msg2.edit("When Is Your Favorite Holiday?")
                                    fav_holiday = await self.bot.wait_for('message',timeout=30)

                                    if all(i.isalpha() for i in fav_holiday.content):
                                        embed2.add_field(
                                            name = 'Question #8',
                                            value = f"When Is Your Favorite Holiday?\n{fav_holiday.content}",
                                            inline = False
                                        )

                                        await msg.edit(embed=embed2)
                                        await msg2.edit("How Old Are You?")
                                        user_age = await self.bot.wait_for('message',timeout=30)

                                        if all(i.isnumeric() for i in user_age.content) and len(user_age.content) <= 2:
                                            embed2.add_field(
                                                name = 'Question #9',
                                                value = f"How Old Are You?\n{user_age.content}",
                                                inline = False
                                            )

                                            await msg.edit(embed=embed2)
                                            await msg2.edit("When Is Your Birthday?")
                                            user_dob = await self.bot.wait_for('message',timeout=30)

                                            if all(i.isprintable() for i in user_dob.content):
                                                embed2.add_field(
                                                    name = 'Question #10',
                                                    value = f"When Is Your Birthday?\n{user_dob.content}",
                                                    inline = False
                                                )

                                                await msg.edit(embed=embed2)
                                                await msg2.edit("Are You Satisfied With Your Profile? Once Created, Staff Will Have To Edit It! If you deny, you will have to start over!\n\nEnter Confirm or Deny")
                                                user_confirm = await self.bot.wait_for('message',timeout=30)

                                                if user_confirm.content.lower() == "confirm":
                                                    await msg2.edit("You Confirmed. Creating Profile Now. . .")

                                                    with sql.connect('main.db') as mdb:
                                                        cur = mdb.cursor()

                                                        all_members = cur.execute('SELECT id FROM members').fetchall()
                                                        all_member_ids = [i[0] for i in all_members]

                                                        if member.id in all_member_ids:
                                                            return await msg2.edit("You've Already Created A Profile. Create A Support Ticket For Futher Assistance")
                                                        else:
                                                            with sql.connect('main.db') as mdb:
                                                                cur = mdb.cursor()

                                                                srch = 'INSERT INTO members(id,exp,level,color,animal,food,edu_subj,artist_music,artist_art,season,holiday,warnings,mutes,bans,kicks,age,dob) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
                                                                val = (
                                                                    member.id, 0, 0,
                                                                    fav_col.content,
                                                                    fav_anim.content,
                                                                    fav_food.content,
                                                                    fav_sub.content,
                                                                    fav_music_art.content,
                                                                    fav_art_artist.content,
                                                                    fav_season.content,
                                                                    fav_holiday.content,
                                                                    0, 0, 0, 0,
                                                                    int(user_age.content),
                                                                    user_dob.content,
                                                                )

                                                                cur.execute(srch,val)

                                                            await asyncio.sleep(2)
                                                            return await msg2.edit("Your Profile Has Been Created! Enjoy <3")
                                                else:
                                                    return await member.send("You Denied. Cancelling Operation")
                                            else:
                                                return await member.send("Answer Must Be Formated As MM/DD/YYYY")
                                        else:
                                            return await member.send("Answer Must Be No More Than 2 Whole Numbers Ex: 17")
                                    else:
                                        return await member.send("Answer Must Be Using The 26-Letter English Alphabet")
                                else:
                                    return await member.send("Answer Must Be Using The 26-Letter English Alphabet")
                            else:
                                return await member.send("Answer Must Be Using The 26-Letter English Alphabet")
                        else:
                            return await member.send("Answer Must Be Using The 26-Letter English Alphabet and/or Numbers Between 0-9")
                    else:
                        return await member.send("Answer Must Be Using The 26-Letter English Alphabet")
                else:
                    return await member.send("Answer Must Be Using The 26-Letter English Alphabet")
            else:
                return await member.send("Answer Must Be Using The 26-Letter English Alphabet")
        else:
            return await member.send("Answer Must Be Using The 26-Letter English Alphabet")


def setup(bot):
    bot.add_cog(CreateProfile(bot))