import discord
import time
from config import Config
from lcd_controller import LCD_Controller
import RPi.GPIO as GPIO

client = discord.Client()
config = Config()
lcd_controller = LCD_Controller()

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)


requests = []



# This method gets called as soon as the bot is connected to Discord
# and ready to recieve callbacks.
@client.event
async def on_ready():
	lcd_controller.clear_screen()
	lcd_controller.set_bottom_text("Online")
	lcd_controller.print_to_screen_center('Remod 9000 started', 1)

	#try:
		#while True:
	#		if len(requests) > 0:
	#			await handle_request(requests.pop(0))
	#finally:
	#	GPIO.cleanup()
	#	print('CLeaning up')


	
# This method gets called by discord.py every time a message is sent in
# any connected Discord server.
@client.event
async def on_message(message):
	# If the message recieved is from this bot, ignore it
	if message.author == client.user:
		return

	# Checks to see if the current message has a blacklisted word in it
	check_result = config.check_for_bad_words(message)

	# If there was a bad word found in this message, HANDLE IT AND ALERT THE ADMIN.
	if check_result is not None:
		requests.append(('BadWord', message, check_result))
		await handle_request(requests.pop(0))
		




# This method is called from on_message().
#    It takes in a bot request and processes it.
#    (currently there's only one type of request, a bad word handling request.
#     the reason for this is that we wanted to provide some kind of structure
#     for other administration requests.)
async def handle_request(this_request):
	print('Handling ' + str(this_request))

	if this_request[0] == 'BadWord':
		await found_blacklisted_word(this_request[1], this_request[2])



# This method is called when a bad word is detected in a new message.
#    This class does most of the heavy lifting during the bad word detection
#    phase. It controls the alert UI, and a ton of user input
async def found_blacklisted_word(message, bad_word):

	# Creates an ALERT UI on the connected LCD screen
	for x in range(0, 2):
		lcd_controller.clear_screen()
		if x % 2 == 1:
			lcd_controller.print_to_screen_center('! BAD WORD !', 2)
		else:
			lcd_controller.print_to_screen_center('!!!ALERT!!!', 1)
		time.sleep(0.5)

	lcd_controller.clear_screen()

	# Displays information about the bad word incident
	lcd_controller.print_to_screen('User: {0.author}'.format(message), 1)
	lcd_controller.print_to_screen('Word: {0}'.format(bad_word), 2)
	time.sleep(0.5)

	# The below set of statements waits for user input in order to continue
	# to the next screen.
	working = True
	ticker = 0
	has_ticked = False
	while working:
		pass_state = GPIO.input(17)
		if pass_state == False:
			working = False
		
		if ticker > 5:
			has_ticked = not has_ticked
			ticker = 0

		if has_ticked:
			lcd_controller.print_to_screen_right('Continue ->', 3)
		else:
			lcd_controller.print_to_screen_right('Continue   ', 3)
		ticker += 1
	lcd_controller.clear_screen()
	time.sleep(0.1)
	lcd_controller.clear_screen()


	# Displays the entire message from the user to the LCD screen, allowing the admin
	# to scroll through it / get context.
	lcd_controller.print_big_message(message.content)


	# The below set of statements prompts the admin to make their decision on whether to:
	#     PASS / WARN / BAN
	# It then stores this choice in a variable (named choice)
	choice = ""
	taking_action = True
	while taking_action:
		taking_action = False
		lcd_controller.print_to_screen_center('* TAKE ACTION *', 1)
		lcd_controller.print_to_screen_center('Pass             Ban', 2)
		lcd_controller.print_to_screen_center('Warn', 3)

		choice = ""
		ticker = 0
		has_ticked = False
		while choice is "":
			pass_state = GPIO.input(17)
			warn_state = GPIO.input(18)
			ban_state = GPIO.input(27)

			if pass_state == False:
				choice = "pass"
			elif warn_state == False:
				choice = "warn"
			elif ban_state == False:
				choice = "ban "
			
			if ticker > 5:
				has_ticked = not has_ticked
				ticker = 0

			if has_ticked:
				lcd_controller.print_to_screen_center('+ TAKE ACTION +', 1)
			else:
				lcd_controller.print_to_screen_center('* TAKE ACTION *', 1)
			ticker += 1
		lcd_controller.clear_screen()
		time.sleep(0.1)
		lcd_controller.clear_screen()


		# The below set of statements prompt the admin to confirm their action,
		# and wait for input from them.
		lcd_controller.print_to_screen_center('Press again to', 1)
		lcd_controller.print_to_screen_center('{0} {1.author}'.format(choice, message), 2)
		working = True
		while working:
			pass_state = GPIO.input(17)
			warn_state = GPIO.input(18)
			ban_state = GPIO.input(27)

			if choice == "pass":
				if not pass_state:
					working = False
				elif not warn_state or not ban_state:
					working = False
					taking_action = True
			elif choice == "warn":
				if not warn_state:
					working = False
				elif not pass_state or not ban_state:
					working = False
					taking_action = True
			elif choice == "ban ":
				if not ban_state:
					working = False
				elif not warn_state or not pass_state:
					working = False
					taking_action = True
		lcd_controller.clear_screen()
		time.sleep(0.1)


	print('User chose to ' + choice)
	lcd_controller.clear_screen()
	
	# Takes action depending on the admins choice made above!
	await bot_take_action(choice, message)

	time.sleep(1)
	lcd_controller.clear_screen()


# This method is called by found_blacklisted_word. It is called
# at the end of the action sequence, and handles the result of
# the admins input (it either passes, warns, or bans a user).
async def bot_take_action(choice, message):
	print(choice)
	if choice == "ban ":
		lcd_controller.print_to_screen_center('~ BOOM ~', 1)
		await client.send_message(message.channel, 'By the power of my glorious ban-hammer, {0.author.mention} is officially banned!'.format(message))
		print('banning!!!')
		#await client.ban(message.author)
		time.sleep(1)

	elif choice == "warn":
		lcd_controller.print_to_screen_center('~ .... ~', 1)
		await client.send_message(message.channel, '{0.author.mention}, you have officially been WARNED. Watch your back my dude...'.format(message))
		print('warning!!!')
		time.sleep(0.5)


	lcd_controller.print_to_screen('{0} {1.author}'.format(choice + '\'d', message), 2)














client.run(config.botToken)