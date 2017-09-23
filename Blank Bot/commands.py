#commands.py
#diode's custom commands

# How to make a custom commands:
#
# In the function commands, type:
#
#   if msg.startswith("<command>"):
#
# replace <command> with whatever you want to trigger the command.
#
# 
#
# A list of functions:
# bot.chat.shrug(<message>)
# bot.chat.chat(<message>)
# bot.chat.ban(<username>)
# bot.chat.timeout(<username>, [time in seconds])
# bot.chat.purge(<username>)
# bot.chat.color(<TwitchDefaultColor | #<HEX color code>> You can only use a hex color if your bots account has Twitch Prime or Twitch Turbo
# bot.p(<text>)

# A list of variables you might need:
# cfg.NICK # the bots name
#


if __name__ == "__main__":
    import run
import sys
import socket
import time
#from config import debug as debug
#from config import admins as admins
import config as cfg
import re
from json import loads
from urllib.request import urlopen
#from bot import chat
import bot

true = True
false = False

version = "1.2"

afkList = []

def commands(user, message):
    global all
    username = user
    msg = message.lower()

    arguments = message.split("\r\n")
    arguments = arguments[0].split(" ")

    if msg.startswith("!commandsversion"):
        bot.chat.chat("Advanced Custom Commands File Version: " + str(version))

    if bot.debug == true: # DEBUG ONLY COMMANDS!!!
        if msg.startswith("blab"):
            bot.p("blab")
        
    # NORMAL COMMANDS

    if "blab" in msg:
        pass

    if msg.startswith("!wave"):
        try:
            bot.chat.chat("Lets all wave at " + arguments[1] + " ! Hi, " + arguments[1] + " !")
        except IndexError:
            bot.chat.chat("Lets all wave at " + username + " ! Hi, " + username + " !")
            
##        if str(arguments[1]).startswith("@"):
##            bot.chat("Lets all wave hello at " + arguments[1] + " ! Hello, " + arguments[1] + " !")
##        else:
##            bot.chat("Lets all wave hello at @" + arguments[1] + " ! Hello, @" + arguments[1] + " !")

    if msg.startswith("!afk"):
        if username in afkList:
            try:
                afkList.remove(username)
                bot.chat.chat(username + " is now back! Welcome back!")
            except ValueError:
                pass
        else:
            afkList.append(username)
            bot.chat.chat(username + " is now AFK. See you soon!")
                    

    
    
