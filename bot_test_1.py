import discord

client = discord.Client()


@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

	if message.author == client.user:
		return

	if message.content.startswith('$hello'):
		await client.send_message(message.channel, 'Hello!')

#tokenFile = open('src/botToken.txt', 'r')
#botToken = tokenFile.readline()
#tokenFile.close()
client.run('NTA2OTAxODQ0MjA4MTIzOTA2.Dro8DQ.jIULoEEXxGrt3-rQuEEZobmzy7k')
