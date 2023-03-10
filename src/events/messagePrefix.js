const { Events } = require('discord.js');
const { DateTime } = require('luxon');
const { allowedChannels, allowedMessagePrefixes } = require('../../config.json');

const incrementCountForUserID = (id) => {
	console.log(`Incrementing for ${id}`);
	console.log('To be implemented.');
};

module.exports = {
	name: Events.MessageCreate,
	async execute(message) {
		if (message.author.bot) return;
		if (allowedChannels.includes(message.channel.id) === false) {
			return;
		}
		const msg = await message.fetch();
		let accepted = false;
		for (const prefix of allowedMessagePrefixes) {
			if (msg.content.indexOf(prefix) == 0) {
				accepted = true;
				break;
			}
		}
		message.channel.send(`Message was${accepted ? ' ' : ' not '}accepted for ${message.author}`);
		if (!accepted) return;
		console.log(msg);
		const timestamp = msg.createdTimestamp;
		const date = new DateTime(timestamp);
		console.log(date);
		incrementCountForUserID(message.author.id);
	},
};