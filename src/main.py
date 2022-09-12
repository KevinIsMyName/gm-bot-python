# imports
from datetime import datetime, timedelta
import time

import json
import os
import sys

import discord
from dotenv import dotenv_values

# logger
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
FORMAT = '%(levelname)s: "%(pathname)s", line %(lineno)s: %(funcName)s() -> %(message)s'
formatter = logging.Formatter(FORMAT)

# log to stderr
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

# log to file
fh = logging.FileHandler("src/log")
fh.setFormatter(formatter)
logger.addHandler(fh)

# load config
config = dotenv_values(".env")
TOKEN = config["TOKEN"]
CHANNEL_ID = int(config["CHANNEL_ID"])
PREFIX = config["PREFIX"]

# discord configuration
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# set timezone
os.environ["TZ"] = "America/New_York"
time.tzset()


def read_dict(filename):
    """
    Reads a JSON-serializable dictionary from a file
    """
    contents = None
    if os.path.isfile(filename):
        with open(filename, "r") as file:
            contents = file.read().strip()
        return json.loads(contents)
    return {}


def sec_to_day(t):
    return datetime.fromtimestamp(t).day


def save():
    with open(
        os.path.join("datastore", "highestStreaks"),
        "w",
    ) as file:
        json.dump(high_scores, file)

    with open(
        os.path.join("datastore", "currentStreaks"),
        "w",
    ) as file:
        json.dump(cur_scores, file)


if not os.path.exists("datastore"):
    os.mkdir("datastore")

high_scores = read_dict(os.path.join("datastore", "highestStreaks"))
cur_scores = read_dict(os.path.join("datastore", "currentStreaks"))


@client.event
async def on_ready():
    """
    Makes the bot online
    """
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    """
    Reads messages and checks for commands
    """
    if message.channel.id == CHANNEL_ID:
        # Author and message
        user_id = str(message.author.id)  # Must be string so its JSON serializable
        content = message.content

        # Time stamps
        message_t = int(time.time())
        day_t = timedelta(1).total_seconds()
        yesterday_t = message_t - day_t
        yesterday_d = sec_to_day(yesterday_t)

        # Do not count the messages from the bot
        if message.author == client.user:
            return

        if content[0] == f"{PREFIX}":
            if content == f"{PREFIX}current":
                try:
                    score, _ = cur_scores[user_id]
                    await message.reply(
                        f"{message.author.mention}'s current streak is {score} days"
                    )
                except KeyError:
                    await message.reply(
                        f"{message.author.mention} currently has no streak. Have you tried sending"
                        " *gm* or *good morning*?"
                    )

            elif content == f"{PREFIX}best":
                if high_scores.get(user_id) is None:
                    await message.reply(
                        f"{message.author.mention} currently has no streak. Have you tried sending"
                        " *gm* or *good morning*?"
                    )
                else:
                    await message.reply(
                        f"{message.author.mention}'s highest streak is {high_scores[user_id]} days"
                    )
            elif content == f"{PREFIX}leaderboard":
                leaderboard = list(cur_scores.items())
                if len(leaderboard) == 0:
                    await message.reply(
                        "No streaks have been started. Have you tried sending *gm* or *good"
                        " morning*?"
                    )
                    return
                leaderboard.sort(key=lambda i: i[1][0], reverse=True)
                lb_msg = "Leaderboard:\n"
                counter = 1
                for user_id, [score, _] in leaderboard:
                    lb_msg += (
                        f"{counter}. {await client.fetch_user(user_id)}: {score} days\n"
                    )
                    counter += 1
                await message.reply(lb_msg)

            elif content == f"{PREFIX}top5":
                highscores = list(high_scores.items())
                if len(highscores) == 0:
                    await message.reply(
                        "No streaks have been started. Have you tried sending *gm* or *good"
                        " morning*?"
                    )
                    return
                highscores.sort(key=lambda i: i[1], reverse=True)
                highscore_msg = "Top 5 high scores:\n"
                num_listings = 5
                for counter, [user_id, score] in zip(range(num_listings), highscores):
                    highscore_msg += f"{counter + 1}. {await client.fetch_user(user_id)}: {score} days\n"
                    counter += 1
                await message.reply(highscore_msg)

            elif content == f"{PREFIX}help":
                await message.reply(
                    "Start a streak by sending *gm* or *good morning*!\n"
                    f"{PREFIX}current: Show current score\n"
                    f"{PREFIX}best: Show personal highest score\n"
                    f"{PREFIX}leaderboard: Show leaderboard\n"
                    f"{PREFIX}top5: Check top 5 highest scores\n"
                    f"{PREFIX}help: Show all commands\n"
                )
            elif content == f"{PREFIX}save":
                save()
                await message.add_reaction("👍")

            elif content == f"{PREFIX}stop":
                save()
                await message.add_reaction("👋")
                sys.exit(0)

        logger.log(
            logging.DEBUG,
            f"{time.strftime('%x %X %Z')}: {user_id} sent message -> {content}",
        )

        # Check for 'gm' or 'good morning'
        if content[:2].lower() == "gm" or content[:12].lower() == "good morning":
            await message.add_reaction("☀️")
        else:
            return  # Skip non gm-messages

        # New user has started a streak.
        if user_id not in high_scores.keys() and user_id not in cur_scores.keys():
            high_scores[user_id] = 1
            cur_scores[user_id] = 1, message_t

        # It is the same day. Nothing happens
        elif sec_to_day(message_t) == sec_to_day(cur_scores[user_id][1]):
            return

        # It is the next day. The streak continues
        elif sec_to_day(cur_scores[user_id][1]) == yesterday_d:
            score, t = cur_scores[user_id]
            cur_scores[user_id] = score + 1, message_t
            high_scores[user_id] = max(int(high_scores[user_id]), score + 1)

        # It is a new day, but not the next day. The streak is broken and restarted
        elif sec_to_day(cur_scores[user_id][1]) != yesterday_d:
            score, t = cur_scores[user_id]
            cur_scores[user_id] = 1, message_t
            high_scores[user_id] = max(int(high_scores[user_id]), score)

    save()


client.run(TOKEN)
