#config.py
#Twitch Chat Bot
#TheDerpyMemeBot
#---------------

# \/ DO NOT CHANGE THIS \/
false = False
true = True

abr = "Alpha"
ver = "2.1.0"
verName = "The 'fixed the whole bot' update 4Head also reverted back to alpha FeelsBadMan"

nextUpdate = "Remembering Better? maybe"
# ^ DO NOT CHANGE THIS ^

debug   = False                                  # FOR DEBUGGING PURPOSES!!!
                                                 # ONLY USE IF YOU KNOW WHAT YOU ARE DOING!!!!
HOST    = "irc.chat.twitch.tv"                   # Twitch's hostname. Dont change this unless you know what you are doing.
PORT    = 6667                                   # Twitch's port. DDont change this unless you know what you are doing.
NICK    = "<BotName>"                            # The Username of the account you are using for the bot
PASS    = "oauth:<token>"                        # The bot account's OAuth token. apps.twitch.tv/tmi for your OAuth. Make 
                                                 # sure you are logged into the bots account when doing this

CHAN    = "<channelName>"                        # The name of the channel you want the bot to join.
                                                 # Dont start it with a '#'
TIMEOUT = "120"                                  # MUST BE IN QUOTATION MARKS!!!! "time" default timeout length, in seconds. 
                                                 # Set to 99999999 for permban
INFO    = "[INFO] "                              # Prefix for informational messages. You should probably add a space at the end.

doJoinMsg = false                                # set to true to say something in chat when the bot joins the chat.
                                                 # set to false to have the bot not say anything when it joins.
customJoinMessage = "default"                    # allows you to set a custom message for when the bot joins chat.
                                                 # set to "default" (in quotes) to use the default message.
                                                 
hasTurbo = False                                 # set to true if your bot account has Twitch Prime and/or Twitch Turbo, otherwise, set to False!

capLimit = 99 # The maximum number of caps you want people to say in 1 message



defaultColor = "BlueViolet" # type /color in chat for a list of default colors

# WARNING!!!!!!!! YOU MUST PUT A COMMA AFTER EVERY LINE IN EACH LIST EXCEPT FOR THE LAST LINE IN EACH LIST!!!!!!!!!!!!!!!
blacklist = [
    
]

commands = [ # These simple custom commands are coming soon. If you want to make one, type !addcom in chat
    #command format
    #"COMMAND_NAME ""COMMANDS_OUTPUT"" USER_LEVEL"
]

admins = [ # People who have more control over the bot.
           # The channel owner and all chat mods are
           # automatctally added to this list.
           
    "nightbot", # because nightbot is so big
    "thederpymemebot"
    
]

regulars = [ # People who you trust in chat. anyone in the admin list is automatically added to this list.
    
]
def refreshLists():
    f = open("regulars.txt", "r")
    regularFile = list(f.read())
    f.close()

    f = open("mods.txt", "r")
    modsFile = list(f.read())
    f.close()

    for regular in regulars:
        if regular in regularFile:
            print("Already in file!")
        else:
            regularFile.append(regular)
            
    for mod in admins:
        if mod in modsFile:
            print("Already in file!")
        else:
            modsFile.append(mod)

    f = open("regulars.txt", "w")
    f.write(str(regularFile))
    f.close

    f = open("mods.txt", "w")
    f.write(str(modsFile))
    f.close

if __name__ == "__main__":
    refreshLists()






