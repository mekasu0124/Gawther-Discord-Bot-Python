<h1>Welcome To Gawther's Repository!</h1>
<h2>Creator: Mekasu - Mekasu#7632</h2>
<p>
    Welcome to the start of my take on what a discord bot should be. Gawther is, in the end, going to be the discord bot to amaze. From co-parenting two separate extensions, to maintaining members log records and staff actions, Gawther is doing it all!
</p>
<h2>Getting Started</h2>
<p>
    Required Dependencies
    <ol>
        <li><a href="https://docs.disnake.dev/en/latest/">disnake.py</a></li>
        <li><a href="https://pypi.org/project/disnake-pagination/">disnake-pagination 1.0</a></li>
    </ol>
</p>
<p>
If you do not want to install each dependency, run <code>pip install -r requirements.txt</code> for Python 2 or <code>pip3 install -r requirements.txt</code> for Python 3+
</p>
<h2>Details On Setup &  Choices</h2>
<p>
    I'm the type of person that once I have completed something, I cannot leave it alone. I'll find the smallest thing to pick at my code with and will give myself unecessary stress trying to fix it which typically ends in making things worse until I give up and revert back to the original completion I had. The purpose of my setup style, especially with the main bot file <code>bot.py</code>, is so that I can have a developement mode type feature to allow me to control 2 bots, one for my main server and one for my development server, and decide which bot get's loaded while I'm working on my code. This is also so that my friends in my main server do not have to consistently keep the server muted, or mute numerous channels, that they would otherwise not have muted and allows them to be able to interact with the bot while I'm testing the final completion of the commands/events I'm building. 
</p>
<h2>Config.json</h2>
<p>
    The <code>config.json</code> is the main file that is needed. This file holds your bot(s) tokens, value of dev_mode, and all of your guild_ids that your bot is in. The structure for the <code>config.json</code> is as follows:
</p>

```json

    {
        "token_dev": "your_token_for_your_development_bot",
        "token_live": "your_token_for_your_live_bot",
        "guild_ids": {
            "a": 00000000000,<br>
            "b": 00000000000<br>
        }
    }
```

<p>
    You're welcome to edit the code to allow iteration through bot tokens as well if you prefer a setup with list/dict indexing. . .I do not. They key names "a" and "b" are not relavent and therefore it does not matter what you set them to as the code uses the variable <i>i</i> as a placeholder for those values when loading the guild_ids.<br>
</p>
<p>
    <u style="color: red;">Note:</u><br>
    The guild_ids stored in the json file are only used for passing all of them to your bot for slash commands. The bot itself already stores all the guilds ids. I do plan to re-write the first part of the bot file to iterate through the guild ids the bot already has stored and pass them through for the guild_ids variable needed for slash_commands.
</p>
<h2>The Main Bot File <code>bot.py</code></h2>
<p>
    This file is setup in a mannor that checks your value for <code>dev_mode</code> that is located in the <code>config.json</code>. It is also setup in a manor for if you only want to maintain one bot, all you have to do is comment out/remove the if-else statement and replace it with the one-liner for initiating the bot.<br>
</p>

```python

    # replace this
    if dev_mode == "True":
        bot = commands.Bot(. . .)
    else:
        bot = commands.Bot(. . .)

    # with this<br>
    bot = commands.Bot(. . .)
```

<h3><u>The <code>on_ready()</code> Function</u></h3>
<p>
    The <code>on_ready()</code> function first iterates through the guild_ids that were loaded into the guild_ids array at the start of the file after opening the json file. As it iterates through each guild id, it obtains that guilds terminal channel for Gawther and creates a counter set equal to 0. This counter is used later for the channels purge method. Next we iterate through the files located in your <code>./cogs</code> folder and telling the bot to load them. Regardless to which server you're in, a bot without commands is a bot that can't do anything, so you'll want to load your cogs in. While loading each cog, the bot tells the terminal channel that each cog has been loaded successfully and increases the counter by one. For each cog that is loaded, a message is sent. 20 cogs = 20 load messages. Now we bring in the purge method <code>await term_channel.purge(limit=count)</code>. This goes back through and cleans up all those cog loaded messages, removes the initial "Logging In" message, and returns that the bot has logged in. There is also an update command placed after this. This command is executable in any text channel, and follows the same steps listed above. The only difference is that when updating, the bot will leave behind both "Gawther is updating" and the confirmation message for logging in.<br>
</p>
<h3>AT THE END OF THE FILE</h3>
<p>
    At the end of the <code>bot.py</code> file there is another check system that involves <code>dev_mode</code>'s value. This tells which bot to load based off whether you're in development mode, or not. If you do not see your bot online in the wanted discord server, please double check that you put the right BOT TOKEN for the corresponding key name in the config.json for that bots purpose <code>"bot_live"</code> or <code>"bot_dev"</code>. Also, ensure that you're bot has been invited to your server, and if so then ensure that they have the roles it needs to view the channels needed.
</p>
<h2>Required Channels For Gawther</h2>
<p>
    Gawther does come with required channels. There are checks in place for each command that checks whether it's needed log channel exists. If it does not exist, Gawther will create it. This is annoying to some, I'm aware, however, it's setup in a manor that helps you too. Instead of having to mute random channels that pop up wherever, Gawther checks for a "Logs" category and checks that the category has the needed channel. If not => create. <code>In addition, not only are checks setup with each command that needs a log channel, but when Gawther first joins the server, he checks for the logs category and creates it, and its' channels, if needed.</code><br><br>
</p>
<ol>Required Channels & Meanings:
    <li>Gawther Logs
        <ul>
            <li>Suggestions
                <ul>
                    <li>
                        This channel is to log each suggestion that your members want to share with you. In my server, this channel is setup to where only developers can see it as I like giving people surprises so when they submit their suggestions and it becomes approved, when they log in again. . .SURPRISE! haha
                    </li>
                </ul>
            </li>
            <li>Warnings/Mutes/Kicks/Bans Log Channels
                <ul>
                    <li>
                        These channel log and display the resulting embed from when your staff member uses the <code>/warn_mem <member_id/name></code> command. It's a safety feature in the sense of all staff can see who, what, when, where, and why the command was executed so that when the member requests to <code>/appeal_ban <mute/kick/ban></code>, the staff member that would approve/deny the appeal will be able to go back and look at what happened when and where, however, that can take a while. As a backup feature, Gawther writes all Mute, Kick, and Ban logs to the database and has a command to allow the staff members to pull up a user's information outside of the <code>/whois < member:optional ></code> command.
                    </li>
                </ul>
            </li>
            <li>Message Deletes Log
                <ul>
                    <li>
                        This channel is only used by the purge command. It records who deleted how many messages, up to 25, in what channel and why. This is so that if a channel is deleted, whether on purpose or accident, it was logged as to why. The reason for this command is required. Otherwise, you can't even hit enter to send it. This is so that it cannot accidentally run without a reason.
                    </li>
                </ul>
            </li>
            <li>
                <ul>
                    <li>
                        This channel is currently used to output other commands that are executed by staff that holds information on an action that is needed, much like the Message Deletes Log channel. This isn't a tattle-tail system, but is a system that if an important action was executed, then you know why. Which is the same reason for all logs. 
                    </li>
                </ul>
            </li>
        </ul>
    </li>
</ol>
<footer style="color: orange;">
    At this time Gawther is a private bot built solely for the Gawther Platform. I am only sharing the main bot files structure for those who want to work with two bots. Anyone is welcome to clone the repository, but you will need to go back and adjust all code to match your server, it's roles, and channels. With this code being private, I will not assist in a re-write for your server. That is on you to figure out
</footer>