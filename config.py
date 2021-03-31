import os
import discord



configPath = os.getcwd() + '/config/'
tokenPath = configPath + 'botToken.txt'
blacklistPath = configPath + 'testBlacklist.txt'

# A utility class to load options from the config folder
class Config:
        botToken = ''
        blacklist = []
        
        def __init__(self):
                tokenFile = open(tokenPath, 'r')
                self.botToken = tokenFile.readline()
                tokenFile.close()

                blistFile = open(blacklistPath, 'r')
                for line in blistFile.readlines():
                        self.blacklist.append(line.strip())
                blistFile.close()

        def check_for_bad_words(self, message):
                for word in self.blacklist:
                        if word in message.content.lower():
                                return word
                return None
