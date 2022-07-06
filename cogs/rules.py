import disnake 
import json 
import sqlite3 as sql

from disnake.ext import commands
from disnake.ext.commands import Cog
from Paginator import CreatePaginator


class RulesFunctions(Cog):
    def __init__(self, bot):
        self.bot = bot

    # done
    @commands.slash_command(name="createrule",description="Create A New Rule",guild_ids=[779290532622893057])
    @commands.has_any_role("Owner", "Head Administrator", "Head Developer")
    async def create_rule(self,inter,rule_name:str,rule_info:str,*,reason:str):
        with open('./rules.json','r',encoding='utf-8-sig') as f:
            data = json.load(f)

            data["rules"].append({
                    "title": rule_name,
                    "rule": rule_info
            })

            with open('./rules.json','w+',encoding='utf-8-sig') as new:
                data = json.dump(data, new, indent=4)
            
            await inter.response.send_message("Successfully Added New Rule To Database", ephemeral=True)

        log_channel = disnake.utils.get(inter.guild.text_channels, name="bot_logs")

        await log_channel.send(f"{inter.author.name} Has Added A New Rule For The Reason Of {reason}.")


    # done
    @commands.slash_command(name="edit_rule",description="Edit A Rule",guild_ids=[779290532622893057])
    @commands.has_any_role("Owner", "Head Administrator", "Head Developer")
    async def edit_rule(self,inter,rule_num:int,type:str,new_info:str,*,reason:str):
        with open('./rules.json','r',encoding='utf-8-sig') as f:
            data = json.load(f)

        item_popped = data["rules"].pop(rule_num-1)

        if type == "title":
            data["rules"].insert(rule_num-1,{
                "title": x,
                "rule": item_popped["rule"]
            })
        else:
            data["rules"].insert(rule_num-1, {
                "title": item_popped["title"],
                "rule": x
            })
            
        with open('./rules.json','w+',encoding='utf-8-sig') as new:
            data = json.dump(data,new,indent=4)

        await inter.response.send_message("Successfully Edited Rule", ephemeral=True)

        log_channel = disnake.utils.get(inter.guild.text_channels, name="bot_logs")

        await log_channel.send(f"{inter.author.name} Has Edited Rule #{rule_num} For The Reason Of {reason}.")

    
    # done
    @commands.slash_command(name="delete_rule",description="Delete A Rule",guild_ids=[779290532622893057])
    @commands.has_any_role("Owner", "Head Administrator", "Head Developer")
    async def del_rule(self,inter,rule_num:int,*,reason:str):
        with open('./rules.json','r',encoding='utf-8-sig') as f:
            data = json.load(f)

        data["rules"].pop((rule_num-1))

        with open('./rules.json','w+',encoding='utf-8-sig') as new:
            data = json.dump(data,new,indent=4)

        await inter.response.send_message("Successfully Deleted Rule", ephemeral=True)

        log_channel = disnake.utils.get(inter.guild.text_channels, name="bot_logs")

        await log_channel.send(f"{inter.author.name} Has Deleted Rule #{rule_num} For The Reason Of {reason}.")


    # done
    @commands.slash_command(name="listrules",description="List All Rules",guild_ids=[779290532622893057])
    @commands.has_any_role(
        "Owner", "Head Administrator", "Head Developer",
        "Head Designer", "Head Support", "Administrator", "Moderator",
        "Support Staff", "Community Helper", "DND DM", "DND PL", "Developers",
        "Designers", "Nitro Member", "Programming", "Gaming", "Member"
    )
    async def list_rule(self,inter):
        with open('./rules.json','r',encoding='utf-8-sig') as f:
            data = json.load(f)

        embed = disnake.Embed(
            color = disnake.Colour.random(),
            timestamp = inter.created_at,
            title = "{}'s Rules".format(inter.guild.name),
            description = "The Following Pages Hold All The Rules For Both The Website and The Discord Server"
        ).set_thumbnail(
            url=inter.guild.icon
        ).set_footer(
            text = "If you disagree with a rule, please submit a suggestion"
        )

        count = 1
        emb_name = "embed"+ str(count)

        all_embs = []

        for index in data["rules"]:
            rule_title = index["title"]
            rule_details = index["rule"]

            emb_name = disnake.Embed(
                color = disnake.Colour.random(),
                timestamp = inter.created_at,
                title = rule_title,
                description = rule_details
            )

            all_embs.append(emb_name)
            count += 1

        timeout = 0
        author_id = inter.author.id

        await inter.response.send_message(embed=embed,view=CreatePaginator(all_embs, author_id, timeout),ephemeral=True)


def setup(bot):
    bot.add_cog(RulesFunctions(bot))