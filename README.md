# gm-bot

A discord bot that counts the amount of days an user said 'gm' or 'good morning' on a discord channel. The bot counts the current streak and the max streak and it also includes a leaderboard.

## Install

```sh
make build || python3 -m pip install -r requirements.txt
```

1. Open [Discord bots](https://discord.com/developers/docs) and create a new application
2. Click on the bot tab and create a new bot
3. Copy the bot's token and assign the variable TOKEN as a string
4. Create a .env file at the root of this repository
5. Copy the bot's token as `TOKEN=myBotTokenHere` in the .env file
6. Turn on the developer mode on Discord and copy the channel's ID as `CHANNEL_ID=myChannelIDHere` in the .env file

## Usage

```sh
make run
```

## Commands

The following commands are supported. Try sending them into the registered channel!

- `.current` to show your current score
- `.best-best` to show your personal high score
- `.leaderboard` to show the leaderboard
- `.top5` to show the top 5 highest score
- `.help` to show all commands
