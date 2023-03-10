const { Events } = require('discord.js');
const { allowedChannels } = require('../../config.json');
const ping = require('../commands/ping.js');

module.exports = {
	name: Events.MessageCreate,
	async execute(message) {
		if (message.author.bot) return;
		if (allowedChannels.includes(message.channel.id) === false) {
			return;
		}
		const msg = await message.fetch();
		const content = msg.content;
		if (content != '.ping') return;
		ping.execute(message);
	},
};