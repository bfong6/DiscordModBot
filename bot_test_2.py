import discord
from config import Config

client = discord.Client()
config = Config()









@client.event
async def on_ready():
	print('Remod 9000 started as {0.user}'.format(client))

@client.event
async def on_message(message):

	if message.author == client.user:
		return


	# Checks to see if the current message has a blacklisted word in it
	check_result = config.check_for_bad_words(message)
	
	if check_result is null:
		return
	else:
		found_blacklisted_word(message, check_result)





def found_blacklisted_word(message, bad_word):
	print('Yikes! {0.author} said {0.message}. Found offending word {1}'.format(message, bad_word))


















client.run('NTA2OTAxODQ0MjA4MTIzOTA2.Dro8DQ.jIULoEEXxGrt3-rQuEEZobmzy7k')