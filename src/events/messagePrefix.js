const { Events } = require('discord.js');
const { allowedChannels, allowedMessagePrefixes } = require('../config.json');

module.exports = {
	name: Events.MessageCreate,
	async execute(message) {
		if (message.author.bot) return;
		if (allowedChannels.includes(message.channel.id) === false) {
			return;
		}
		const msg = await message.fetch();
		const content = msg.content;
		let accepted = false;
		for (const prefix of allowedMessagePrefixes) {
			if (content.indexOf(prefix) == 0) {
				accepted = true;
				break;
			}
		}
		message.channel.send(`Message was ${accepted ? ' ' : 'not '}accepted for ${message.author}`);
	},
};