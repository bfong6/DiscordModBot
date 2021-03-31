import RPi.GPIO as GPIO
import lcddriver
import time

max_characters = 20
scroll_speed = 0.1

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# LCD_Controller is a utility class consisting of lcddriver helper methods
class LCD_Controller:

	lcd = lcddriver.lcd()
	bottom_text = "Loading..."

	def __init__(self):
		self.bootup_lcd()





	def bootup_lcd(self):
		self.print_to_screen('BOOTING', 1)
		self.print_to_screen('ReMod 9000', 2)



	# Scrolls text across the screen on the desired line
	def scroll_text(self, text, line = 1):
		output = ' ' * max_characters
		self.clear_screen()
		for char in text + ' ' * max_characters:
			output = output + char
			output = output[1:max_characters + 1]
			self.lcd.lcd_display_string(output, line)
			time.sleep(scroll_speed)

	# Clears the connected LCD screen 
	def clear_screen(self):
		self.clear_line(1)
		self.clear_line(2)
		self.clear_line(3)

	# Clears the line specified on the LCD
	def clear_line(self, line):
		self.print_to_screen(' ' * max_characters, line)

	# Utility method that prints to the LCD with a center justification
	def print_to_screen_center(self, text, line):
		self.print_to_screen(text.center(max_characters, ' '), line)

	# Utility method that prints to the LCD with a right justification
	def print_to_screen_right(self, text, line):
		self.print_to_screen(text.rjust(max_characters, ' '), line)

	# Utility method that prints to the LCD with a left justification
	def print_to_screen(self, text, line):
		self.lcd.lcd_display_string(text, line)
		print('=|=  ' + text)

	# Sets the text at the 4th line of the screen
	def set_bottom_text(self, text):
		self.bottom_text = text
		self._update_bottom_text()

	# A helper method that updates the bottom text
	def _update_bottom_text(self):
		self.lcd.lcd_display_string(self.bottom_text, 4)




	# Utility method that prints a large string on to the LCD, and lets you
	# scroll through it
	def print_big_message(self, longStr):
		stringLst = longStr.split()
		prntArray = self.lineBreak(stringLst, max_characters)
		self.prntLCD(prntArray)


	# Helper method for print_big_message
	def lineBreak(self, stringLst, maxChar):
		'stores lines of text in an array, sized to fit limited space'
		prntArray = []
		line = ''
		for word in stringLst:
			if len(line) == 0:
				testStr = line + word
			else:
				testStr = line + ' ' + word
			if len(testStr) <= maxChar:
				if len(line) == 0:
					line += word
				else:
					line += ' ' + word
			else:
				prntArray.append(line)
				line = word
		prntArray.append(line)

		for x in range(3 - (len(prntArray) % 3) ):
			prntArray.append('')


		return prntArray
	
	# Helper method for print_big_message
	def prntLCD(self, prntArray):
		'prints lines on LCD in groups of 3'

		print(prntArray)

		i = 0
		while i < len(prntArray):
			line = (i % 3) + 1
			print(prntArray[i])
			if line < 3:
				self.lcd.lcd_display_string(prntArray[i], line)
			else:
				self.lcd.lcd_display_string(prntArray[i], line)
				
				working = True
				while working:
					pass_state = GPIO.input(17)
					ban_state = GPIO.input(27)

					if ban_state == False:
						working = False
					elif pass_state == False:
						if i >= 3:
							i -= 6
							working = False

				self.clear_screen()
				time.sleep(0.1)
			i += 1


		self.clear_screen()
		time.sleep(0.1)
