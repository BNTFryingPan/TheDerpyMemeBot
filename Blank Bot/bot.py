#bot.py
#Twitch Chat Bot
#TheDerpyMemeBot
#---------------

if __name__ == "__main__":
    import run


# Imports
import sys
import socket
import time
import string
#from config import debug as debug
#from config import admins as admins
import config as cfg
import re
from json import loads
import json
from urllib.request import urlopen
import commands
import threading
import random
import tkinter as Tk

blab = 0

class TraceConsole():

    def __init__(self):
        # Init the main GUI window
        self._logFrame = Tk.Frame()
        self._log      = Tk.Text(self._logFrame, wrap=Tk.NONE, setgrid=True)
        self._scrollb  = Tk.Scrollbar(self._logFrame, orient=Tk.VERTICAL)
        self._scrollb.config(command = self._log.yview) 
        self._log.config(yscrollcommand = self._scrollb.set)
        # Grid & Pack
        self._log.grid(column=0, row=0)
        self._scrollb.grid(column=1, row=0, sticky=Tk.S+Tk.N)
        self._logFrame.pack()

    def log(self, msg, level=None):
        # Write on GUI
        self._log.insert('end', msg + '\n')

    def exitWindow(self):
        # Exit the GUI window and close log file
        print('exit..')

t = TraceConsole()


nonTurboColors = ["blue", "blueviolet", "cadetblue", "chocolate", "coral", "dodgerblue", "firebrick", "goldenrod", "green", "hotpink", "orangered", "Red", "seagreen", "springgreen", "yellowgreen"]

def timeLoop(reset=False):
    global seconds
    
    if reset == True:
        seconds == 0
    else:
        while True:
            seconds = seconds + 1
            time.sleep(1)        

# True/False
true = True
false = False

# Other true or false things
sendMsgs = true
doTimeout = True

regulars = []
mods = []
permittedLinkSenders = []
chatOut = []
allChatters = []
allModerators = []
allStaff = []
allAdmins = []
allGlobalMods = []
allViewers = []
chatlist = {}

noBanList = ["melly_22", "msg", "Welcome"]

antibanlines = 0

# Debug things
debug = false
error = 0

unicode = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

def p(text): # Info text printing

    try:
        print(cfg.INFO + str(text).translate(unicode))
        t.log(cfg.INFO + str(text).translate(unicode))
    except UnicodeEncodeError:
        print("There are unsupported unicode characters in the message FeelsBadMan")

def dp(text): # Debug printing
    
    p("[DEBUG] " + text)
    
def errored(errors=1):
    ret = "Error: " + str(sys.exc_info)
    global error
    error = error + errors
    return ret

p("Loading bot...")
#Network Functions

s = socket.socket()
##private = socket.socket()

CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
#link = 
##def getChatters():
##    global allChatters
##    global chatlist
##    response = urlopen('https://tmi.twitch.tv/group/user/leotomasmc/chatters') # gets a list of chatters
##    readable = response.read().decode('utf-8') # decodes the list
##    chatlist = loads(readable) #
##    chatlist = chatlist
    
def refreshAllRanks():
    global allChatters
    global allStaff
    global allGlobalMods
    global allModerators
    global allAdmins
    global allVeiwers
    edit = 0
    p("Updating all chatter lists...")

    response = urlopen('https://tmi.twitch.tv/group/user/leotomasmc/chatters') # gets a list of chatters
    readable = response.read().decode('utf-8') # decodes the list
    p(str(response))
    p(str(readable))

    chatlist = loads(readable) # makes a newlist
    chatters = chatlist['chatters']

    p(str(chatlist))
    
    p(str(allChatters))
    
    newModerators = chatters['moderators'] # puts all moderaters in a list
    for mod in newModerators:
        if mod not in allModerators:
            allModerators.append(mod)
            edit = 1
        if mod not in allChatters:
            allChatters.append(mod)
            edit = 1
            
    newStaff = chatters['staff']
    for staff in newStaff:
        if staff not in allStaff:
            allStaff.append(staff)
            edit = 1
        if staff not in allChatters:
            allChatters.append(staff)
            edit = 1

    newGlobalMods = chatters['global_mods']
    for glomod in newGlobalMods:
        if glomod not in allGlobalMods:
            allGlobal_mods.append(glomod)
            edit = 1
        if glomod not in allChatters:
            allChatters.append(glomod)
            edit = 1

    newAdmins = chatters['admins']
    for admin in newAdmins:
        if admin not in allAdmins:
            allAdmins.append(admin)
            edit = 1
        if admin not in allChatters:
            allChatters.append(admin)
            edit = 1

    newViewers = chatters['viewers']
    for veiwer in newViewers:
        if veiwer not in allVeiwers:
            allViewers.append(viewer)
            edit = 1
        if viewer not in allChatters:
            allChatters.append(viewer)
            edit = 1

    if edit == 0:
        p("There was nothing to add to any chatter list")
    elif edit == 1:
        p("Updated chatter lists")
    else:
        p("[WARN Something went wrong D:")

def refreshAdmins():
    global allChatters
    global mods
    p("Updating moderator list...")

    response = urlopen('https://tmi.twitch.tv/group/user/leotomasmc/chatters') # gets a list of chatters
    readable = response.read().decode('utf-8') # decodes the list
    chatlist = loads(readable) # makes a newlist
    chatters = chatlist['chatters']

    moderators = chatters['moderators'] # puts all moderaters in a list

    p("Adding new moderators...")

    edit = 0

    if "leotomasmc" not in mods:
        mods.append("leotomasmc") # adds me to the admin list, if not already
        edit = 1

    if cfg.CHAN.lower() not in mods:
        mods.append(cfg.CHAN.lower()) # adds the channel owner to the admin list, if not already
        edit = 1

    for mod in moderators:
        if mod not in mods:
            mods.append(mod) # adds the found mods, that arent in the admin list, to the admin list
            edit = 1

    if cfg.NICK.lower() not in mods:
        mods.append(cfg.NICK)
        edit = 1

    if "tmi" not in mods:
        mods.append("tmi")

    if "msg" not in mods:
        mods.append("tmi")

    if "Welcome" not in mods:
        mods.append("Welcome")

    if edit == 1:
        p("Added new moderators.")
    elif edit == 0:
        p("No new moderators were found, or added")
    else:
        p("[WARN] Something crazy happened!")
        errored()

    p("Updated moderator list.")
    p("Current admins: " + str(mods))

def syncRegulars():

    p("Adding moderaters to the regulars list")
    edit = 0
    for mod in mods:
        if mod not in regulars:
            regulars.append(mod)
            edit = 1

    if edit == 1:
        f = open("regulars.txt", "w")
        f.write(str(regulars))
        f.close
        
        p("Added moderaters to regulars")
    elif edit == 0:
        p("No users were added to the regulars list")
    else:
        p("Something crazy happened!")
        errored()

    p("Updated regulars list")
    p("Current regulars: " + str(regulars))
    
p("Initlizing Functions...")
# Functions
quotes = {}
def getQuotes():
    global quotes
    try:
        with open("quotes.json") as f:
            quotes = json.load(f)
    except:
        errored()
        p("error D:")
        
commandsList = {}
def getCustomCommands():
    global commandsList
    try:
        #f = open("commands.json", "r")
        #commandsList = dict(f.read())
        #f.close
        with open("commands.json") as f:
            commandsList = json.load(f)
    except:
        #p(str(sys.exc_info()[0]))
        p("There was a problem getting the command list FeelsBadMan [" + str(sys.exc_info()) + "]")
        errored()
        
class chat:
    global sendMsgs
    def chat(message):# Function for sending a message to the Twitch Chat
        msg = message #\
        if antibanlines < 50:
            if cfg.CHAN.startswith("#"):
                blab = "PRIVMSG " + cfg.CHAN.lower() + " :" + msg + "\r\n"
            else:
                blab = "PRIVMSG #" + cfg.CHAN.lower() + " :"  + msg + "\r\n"
            if debug == true:
            
                dp("Sending chat message: " + msg)

            if sendMsgs == true:
                pass
                #s.send(bytes(str(r"PRIVMSG #" + cfg.CHAN + r" :"  + msg + r"\r\n", "UTF-8"))) # This is just the old statement to send a message
                #s.send(bytes(str(blab), 'UTF-8'))
        else:
            p("Too many chat messages!")
            
        queue(msg)
        
    def ban(username):
        
        p("Attemtpting to ban " + username)
        
        if username in mods:
            p("Was going to ban " + username + ", but they are on the Admin list")
            doTimeout = false
            
            
        if doTimeout == true:
                
            chat.chat(".ban " + user)
            
        doTimeout = true

    def timeout(username, seconds=cfg.TIMEOUT):
        sec = seconds
        global doTimeout
        p("Attempting to timeout " + username + " for " + sec + " seconds...")
        if username in mods or username in noBanList:
            p("Was going to timeout " + username + " for " + sec + " seconds, but they are a moderater")
            doTimeout = False
            
            
        if doTimeout == True:
            
            if sec == "99999999":
                chat.ban(username)
            else:
                chat.chat(".timeout " + username + " " + sec)
                
        doTimeout = true

    def purge(username):
        chat.timeout(username, "1")

    def p(username):
        chat.purge(username)

    def color(colorName):
        chat.chat(".color " + colorName)

    def colour(colorName):
        chat.chat(".color " + colorName)

    def me(msg):
        chat.chat(".me " + msg)

    def shrug(msg):
        chat.chat(msg + " ¯\_(ツ)_/¯")

    def u(username):
        chat.chat(".unban " + username)

    def unban(username):
        chat.chat(".unban " + username)

    def sub(ts):
        try:
            bool(ts)
        
            if ts == True:
                chat.chat(".subscribers")
            elif ts == False:
                chat.chat(".subscribersoff")

        except:
            p("Error!")
            #critError = 1

    def slow(ts):
        try:
            bool(ts)

            if ts == True:
                chat.chat(".slow")
            elif ts == False:
                chat.chat(".slowoff")

        except:
            p("Error!")
            #critError = 1

    def r9k(ts):
        if ts == True:
            chat.chat(".r9kbeta")
        elif ts == False:
            chat.chat(".r9kbetaoff")

    def whisper(user, msg):
        chat.chat(".w " + user + " " + msg)
        print("Whisper to" + user + ": " + msg)

    def emote(ts):
        if ts == True:
            chat.chat(".emoteonly")
        elif ts == False:
            chat.chat(".emoteonlyoff")

    def followers(ts, time="10m"):
        if ts == True:
            chat.chat(".followers " + time)
        elif ts == False:
            chat.chat(".followersoff")

    # Will add more by request, if possible

def catchUp():
    global unicode
    global chatOut
    for msg in chatOut:
        try:
            print(cfg.NICK + ": " + msg.translate(unicode))
        except UnicodeEncodeError:
            print(cfg.NICK + ": A message with ded characters")
    chatOut = []

def queue(msg):
    global chatOut
    chatOut.append(msg)

def reconnect():
    try:
        init_()
    except:
        print(sys.exc_info())

p("Initliazed Functions.")

globalCommands = {
    "!son": True,
    "!soff": True,
    "!on": True,
    "!off": True,
    "!kill": True,
    "!enablemsgs": True,
    "!disablemsgs": True,
    "!errors": True,
    "!hug": True,
    "!addmod": True,
    "!addregular": True,
    "!addcom": True,
    "!delcom": True,
    "!425": True,
    "darkoChair": True
    }
botIsOn = true
superBot = true
space = " "
nothing = ""
yesList = ["yes", "on", "true", "y"]
noList = ["no", "off", "false", "n"]
chatLines = 0
totalLines = 0

def refreshAll(doChat=False):
    """blab"""
    if doChat == True:
        #getChatters()
        chat.chat("Refreshing Bot... 0%")
        
        chat.chat("Refreshing Userlists...")
        refreshAllRanks()
        chat.chat("20%")
        refreshAdmins()
        chat.chat("40%")
        syncRegulars()
        chat.chat("Refreshed User Lists. 60%")

        chat.chat("Refreshing Custom Commands...")
        getCustomCommands()
        chat.chat("Refreshed Custom Commands. 80%")

        chat.chat("Refreshing Quotes List...")
        getQuotes()
        chat.chat("Refreshed Quote List. 100%")
    
        p("Refreshed everything! 100%")
    else:
        refreshAllRanks()
        refreshAdmins()
        syncRegulars()
        getCustomCommands()
        getQuotes()


##class inputSystem(): ####################################################################################################################################################
##    userInput = str()
##    
##    def _init():
##        pass
##
##    def getInput():
##        userInput = input("> ")
##
##    def useInput():
##        chat.chat(userInput)
##
##    def inputLoop():
##        while True:
##            try:
##                getInput()
##                useInput()
##            except:
##                print(str(sys.exc_info))
##                print("Error")
##                break
    
##def randomAlert():
##    global tmr
##    tmr = TimerThread(900, 0, randomAlert)
##    tmr.start()
##
##def chatBuffer():
##    global antibanlines
##    buffer = TimerThread(30, 0, chatBuffer)
##    antibanlines = 0
##    
##def whisperLoop():
##    global unicode
##    global botIsOn
##    global debug
##    global doTimeout
##    global true
##    global false
##    global chatOut
##    global s
##    global regulars
##    global mods
##    global superBot
##    global chatters
##    global sendMsgs
##    global error
##    global space
##    global nothing
##    global permittedLinkSenders
##    global commandsList
##    global chatLines
##    global totalLines
##
##    p("� is the Unicode Replacement Character. It replaces any character that the Python IDLE cant understand.")
##    p("You might see is when someone uses the BTTV emote :thinking: as BTTV turns it into a Unicode character.")
##
##    while True:
##        response = s.recv(1027).decode("utf-8") # Gets chat from the server
##        if response == "PING :tmi.twitch.tv\r\n": # Checks if the message is a ping from Twitch
##            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8")) # Pongs the server
##            p("Repinged the Twitch Server") # Prints to the console that the server was repinged.
##        else:
##            username = re.search(r"\w+", response).group(0) # Makes the username not be gibberish
##            message = CHAT_MSG.sub("", response) # seperates the username, from the actual messages
##            msg = message.lower() # makes a lowercase version, for the sake of MANY hours of time...
##
##            # ARGUMENTS
##
##            arguments = message.split("\r\n")
##            arguments = arguments[0].split(" ")
##            argumentsL = msg.split("\r\n")
##            argumentsL = argumentsL[0].split(" ")
##
##            if arguments == []:
##                p("blab")
##            else:
##                chatLines = chatLines + 1
##                totalLines = totalLines + 1
##
##            p(str(arguments))
##
##        try:
##                print(cfg.CHAN + "> " + username.translate(unicode) + ": " + message.translate(unicode)) # prints the chat message to the log
##                
##            except UnicodeEncodeError:
##                p("D: there are unsupported unicode characters in the message FeelsBadMan")
##                
##            if debug == true:
##                dp(response)
##            catchUp() # catch up!
##            blab = 0

def miniLoop():
    pass
    
def globalChat():
    global unicode
    global botIsOn
    global debug
    global doTimeout
    global true
    global false
    global chatOut
    global s
    global regulars
    global mods
    global superBot
    global chatters
    global sendMsgs
    global error
    global space
    global nothing
    global permittedLinkSenders
    global commandsList
    global chatLines
    global totalLines

    global blab

    immad = 0
    sendMsgs = false
    
    chat.color(cfg.defaultColor)

    #time.sleep(10)
    #randomAlert()

    #chatBuffer()

    if cfg.doJoinMsg == true: # if the user wans custom join msg:
        if cfg.customJoinMessage == "default": # if its default:
            chat.chat(cfg.NICK + " has arrived!!!") #say default message
        else:
            chat.chat(str(customJoinMessage)) # says custom join message
    
    while True:
        rawResponse = s.recv(1027).decode("utf-8") # Gets chat from the server
        #response = rawResponse
        if rawResponse == "PING :tmi.twitch.tv\r\n": # Checks if the message is a ping from Twitch
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8")) # Pongs the server
            p("Repinged the Twitch Server") # Prints to the console that the server was repinged.
        else:
            if rawResponse.startswith("@"):
                if rawResponse.startswith("@msg-id="):
                    msg = rawResponse
                    if msg.startswith("@msg-id=color_changed :tmi.twitch.tv NOTICE #"):
                        print(cfg.CHAN + "> Notice: " + cfg.NICK + ", Your color has been changed.")
                elif rawResponse.startswith("tmi.twitch.tv"):
                    if rawResponse.startswith("tmi.twitch.tv USERSTATE #"):
                        pass
                else:
                    try:
                        responseSplit = rawResponse.split(" :", 1)
                        userinfo = responseSplit[0]
                        response = responseSplit[1]
                        username = re.search(r"\w+", response).group(0) # Makes the username not be gibberish
                        message = CHAT_MSG.sub("", response) # seperates the username, from the actual messages
                        
                        if debug == True:
                            dp("User Info: " + userinfo)
                            
                        mainCommands(rawResponse)
                        
                        if debug == True:
                            dp(response.translate(unicode))
                        try:
                            message = response.split(" :", 1)[1]
                        except IndexError as e:
                            print("Error creating message")
                            immad = 1
                        msg = message.lower() # makes a lowercase version, for the sake of MANY hours of time...
                        if immad == 1 or username == "tmi" or username == "msg" or username == "Welcome":
                            pass
                        else:
                            pass
                    except AttributeError:
                        print("Error! " + str(sys.exc_info()))
                        break
                    
                    try:
                        print(cfg.CHAN.translate(unicode) + "> " + username.translate(unicode) + ": " + message.translate(unicode)) # prints the chat message to the log
                    
                    except UnicodeEncodeError:
                        p("D: there are unsupported unicode characters in the message FeelsBadMan")
                    
                if debug == true:
                    dp(response)
                catchUp() # catch up!
                blab = 0

                #if critError == 1:
                    #break
                time.sleep(1)
            else:
                try:
                    responseSplit = rawResponse.split(" :", 1)
                    userinfo = responseSplit[0]
                    response = responseSplit[1]
                    username = re.search(r"\w+", response).group(0) # Makes the username not be gibberish
                    message = CHAT_MSG.sub("", response) # seperates the username, from the actual messages
                    msg = message.lower()
                    
                    mainCommands(rawResponse)
                    
                    #print(response.translate(unicode))
                    try:
                        message = response.split(" :", 1)[1]
                    except IndexError as e:
                        print("Error creating message")
                        immad = 1
                    msg = message.lower() # makes a lowercase version, for the sake of MANY hours of time...
                    if immad == 1 or username == "tmi" or username == "msg" or username == "Welcome":
                        pass
                    else:
                        pass
                except AttributeError:
                    print("Error! " + str(sys.exc_info()))
                    break
                
                try:
                    print(cfg.CHAN + "> " + username.translate(unicode) + ": " + message.translate(unicode)) # prints the chat message to the log
                
                except UnicodeEncodeError:
                    p("D: there are unsupported unicode characters in the message FeelsBadMan")

                if debug == true:
                    dp(response)
                catchUp() # catch up!
                blab = 0
            immad = 0

def mainCommands(rawResponse="ERROR NoResponseProvided"):
    global unicode
    global botIsOn
    global debug
    global doTimeout
    global true
    global false
    global chatOut
    global s
    global regulars
    global mods
    global superBot
    global chatters
    global sendMsgs
    global error
    global space
    global nothing
    global permittedLinkSenders
    global commandsList
    global chatLines
    global totalLines

    global blab
    
    response = rawResponse
    
    if rawResponse == "ERROR NoResponseProvided":
        p("Error: No Raw Response provided")
    else:
        try:
            responseSplit = rawResponse.split(" :", 1)
            userinfo = responseSplit[0]
            response = responseSplit[1]
            username = re.search(r"\w+", response).group(0)
            message = CHAT_MSG.sub("", response) # seperates the username, from the actual messages
            msg = message.lower()

            try:
                message = response.split(" :", 1)[1]
                msg = message.lower()
            except IndexError as e:
                print("Error creating message" + errored())
                immad = 1

            
        except:
            p(errored())
            
        arguments = message.split("\r\n")
        arguments = arguments[0].split(" ")
        argumentsL = msg.split("\r\n")
        argumentsL = argumentsL[0].split(" ")
        
        doBreak = 0
        try:
            message = response.split(" :", 1)[1]
        except IndexError as e:
            print("Error creating message")
            doBreak = 1

        if doBreak == 1:
            return

        if arguments == []:
            p("blab")
        else:
            chatLines = chatLines + 1
            totalLines = totalLines + 1
            
        if debug == true:    
            p(message)
            p(username)
            p(str(arguments))

        # END ARGUMENTS

        #timer beta
        
        #if msg.startswith("!timeroff"):
            #if username in mods:
                #try:
                    #tmr.stop()
                #except:
                    #chat.chat("An unknown error occured D:")
                    #break

        #if msg.startswith("!timeron"):
            #if username in mods:
                #try:
                    #tmr.start()
                #except:
                    #chat.chat("An unknown error occured D:")
                    #break

        # end timer beta

        # DEBUG

        if msg.startswith("!debug"):
            if username == "leotomasmc" or username == cfg.CHAN.lower():
                try:
                    p(arguments[1])
                except IndexError:
                    if debug == True:
                        chat.chat("[DEBUG] Debug mode is currently on!")
                    elif debug == False:
                        chat.chat("[DEBUG] Debug mode is currently off!")
                    else:
                        chat.chat("D: Debug mode is currently broken, somehow: " + str(debug))
                    blab = 1

                if blab == 0:
                    if arguments[1] in yesList:
                        if debug == false:
                            chat.chat("[DEBUG] Turning debug mode on...")
                            debug = true
                            chat.chat("[DEBUG] Debug mode on!")
                        else:
                            chat.chat("Debug mode is already on!")
                    elif arguments[1] in noList:
                        if debug == true:
                            chat.chat("[DEBUG] Turning debug mode off...")
                            debug = false
                            chat.chat("[DEBUG] Debug mode off!")
                        else:
                            chat.chat("Debug mode is already off!")

        # refresh
        
        if msg.startswith("!refresh"):
            if username == "leotomasmc" or username == cfg.CHAN.lower():
                if argumentsL[1] == yesList:
                    try:
                        chat.chat("Refreshing Bot... Prepare for spam D:")
                        refreshAll(True)
                        chat.chat("Refreshed the bot!")
                    except:
                        chat.chat("There was an error refreshing the bot FeelsBadMan")
                        return True
                else:
                    try:
                        chat.chat("Refreshing bot WITHOUT spam!")
                        refreshAll(False)
                        chat.chat("Refreshed te bot!")
                    except:
                        chat.chat("There was an enexpected error while refreshing the bot")

        #disable sending messages
        
        if msg.startswith("!disablemsgs"):
            if username in mods or username == "leotomasmc" or username == cfg.CHAN.lower():
                chat.chat("The bot will stop sending messages")
                chat.chat("The bot will still do normal actions, it just wont say anything!")
                sendMsgs = false

        if msg.startswith("!enablemsgs"):
            if username in mods or username == "leotomasmc" or username == cfg.CHAN.lower():
                sendMsgs = true
                chat.chat("The bot is now sending messages")

        # debug ability so i can turn your bot off, and then you cant turn it back on Kappa
        if msg.startswith("!son"):
            if username == "leotomasmc":
                if superBot == false:
                    superBot = true
                    botIsOn = true
                elif botIsOn == true and superBot == true:
                    chat.chat("Bot is already on 4Head")
                else:
                    superBot = true
                    botIsOn = true
            elif username == cfg.CHAN.lower():
                if superBot == false:
                    chat.chat(r"Only the person who made the bot can do this, send a whisper to LeotomasMC on Twitch if your bot was deactivated somehow")
            
        if msg.startswith("!soff"):
            if username == "leotomasmc":
                superbot = false
                botIsOn = false
            elif username == cfg.CHAN.lower():
                chat.chat(r"Only the person who made the bot can do this D:")

        # kill switch. useful if your bot is freaking out, but you dont want to ban it/unmod it.
        if msg.startswith("!kill"):
            if username == "leotomasmc" or username == cfg.CHAN.lower():
                chat.chat(r"Killing bot... " + username)
                return True

        if superBot == true:

            if msg.startswith("!nextupdate"):
                chat.chat("Up Next: " + cfg.nextUpdate + "!")

##                if msg.startswith("!refresh"):
##                    refreshAll()
##                    if username in (allModerators or allStaff or allGlobal_mods or allAdmins):
##                        chat.chat("Updated all chatter lists")
                    
            # Turn the bot off. Mods and above can turn it on and off.
            # possible config option for levels?
            if msg.startswith("!off"):
                if username in mods:
                    if botIsOn == true:
                        botIsOn = false
                        chat.chat(r"Bot is now off FeelsBadMan")
                    else:
                        chat.chat(r"The bot is already off D:")
                else:
                    chat.chat(r"Hey! " + username + "! You cant do that!")

            if msg.startswith("!on"):
                if username in mods:
                    if botIsOn == false:
                        botIsOn = true
                        chat.chat(r"Bot is now on! 4Head")
                    else:
                        chat.chat(r"The bot is already on D:")
                else:
                    chat.chat(r"Hey! " + username + "! You cant do that!")
                
            if botIsOn == true:

                if msg.startswith("!age"):
                    try:
                        p(arguments[1])
                        chat.chat(arguments[1] + " is " + str(random.randint(0, 100)) + " years old Kappa")
                    except IndexError:
                        chat.chat(username + " is " + str(random.randint(0, 100)) + " years old Kappa") # random age command. i did this to avoid giving ouy my real age DansGame
                        

                if msg.startswith("!lines"):
                    if username in regulars: # debugish chat lines command
                        chat.chat("Chat Lines this Session: " + str(totalLines))

                if msg.startswith("!commands"): # commands list
                    chat.chat("Global Commands: !addfail !removefail !fails !setfails !on !off !son !soff !addregular !addmod !addcom !delcom !kill !refresh !enablemsgs !disablemsgs !errors !425 !hug")
                    #chat.chat("Custom Commands: " + str(commandsList))

                #if username not in chatters:
                    #if username == "tmi":
                        #p("D:")
                    #else:
                        #if ("bye") not in msg:
                            #chat.chat(r"Welcome to " + cfg.CHAN + "'s stream chat!")
                            #chatters.append(username)
                            #refreshChatters()

                for pattern in cfg.blacklist:
                    if pattern in msg:
                        p("Blacklisted word found...")
                        if username in mods:
                            p("User was a moderater!")
                        elif username in regulars: # Blacklist words/phrases check
                            chat.purge(username)
                            chat.chat(r"D: dont say bad things! [" + username + "] [regular: purge]")
                        else:
                            chat.timeout(username, "60")
                            chat.chat(r"D: dont say bad things! {" + username + "] [non-regular: timeout]")

                # REGULARS and MODS ---------------------------------------------------------------------------
                if msg.startswith("!addregular"):
                    if username in mods:
                        if " " in msg:
                            blab = msg.split(" ", 1)
                            newReg = blab[1].split("\r\n")

                            if newReg[0] not in regulars:

                                regulars.append(newReg[0])

                                f = open("regulars.txt", "w")
                                f.write(str(regulars))
                                f.close
                            
                                chat.chat(r"Added " + newReg[0] + "to the regulars list")
                            else:
                                chat.chat(r"Is " + newReg[0] + " already in the regulars list? D:")

                        else:
                            chat.chat(r"Did you define the user to become a new regular? D:")
                    else:
                        chat.chat(r"D: Hey! You cant do that! [mod] D:")

                if msg.startswith("!addmod"):
                    if username == cfg.CHAN.lower() or username == "leotomasmc":
                        if " " in msg:
                            blab = msg.split(" ", 1)
                            newMod = blab[1].split("\r\n")

                            if newMod[0] not in mods:

                                mods.append(newMod[0])
                                regulars.append(newMod[0])
                                f = open("mods.txt", "w")
                                f.write(str(mods))
                                f.close
                                f = open("regulars.txt", "w")
                                f.write(str(regulars))
                                f.close
                                
                                chat.chat(r"Added user " + newMod[0] + " to the moderator list")

                            else:
                                chat.chat(r"Is " + newMod[0] + " already a moderator? D:")
                        else:
                            chat.chat(r"Did you define the user to become a new mod? D:") 
                    else:
                        chat.chat(r"Hey! You cant do that! [owner] D:")

                # clear command
                if msg.startswith("!clear"):
                    if msg.startswith("!clearpermits"):
                        p("Other command found!")
                    else:
                        if username in mods:
                            chat.chat(r"/clear")
                            chat.chat(r"Chat was cleared by " + username)
                        else:
                            chat.chat(r"Hey! " + username + "! You cant do that! [mod] D:")

                # FAILS ---------------------------------------------
                if msg.startswith("!fails"):
                    f = open("fails.txt", "r") 
                    fails = f.read() #gets fails
                    f.close()

                    if fails == "":
                        chat.chat("There was nothing in the fails file. Creating int of 0")
                        fails = int(0)

                    p(str(fails))

                    try:
                        fails = int(fails)
                        #p(fails)
                        chat.chat(r"Fails: " + str(fails)) #tells chat the # of fails
                    except ValueError:
                        errored()
                        chat.chat("There was an error converting the number of fails from a str to an int FeelsBadMan")
                        if debug == true:
                            chat.chat(str(sys.exc_info()[0]))
                    
                        
                if msg.startswith("!setfails"):

                    f = open("fails.txt", "r")
                    failsWas = f.read() # Gets current fails
                    f.close()

                    try:
                        failsIntWas = int(failsWas)
                    except ValueError:
                        errored()
                        chat.chat("There was an error converting the number of fails from a str to an int FeelsBadMan")
                        if debug == true:
                            chat.chat(str(sys.exc_info()[0]))

                    p(str(failsWas))
                    
                    if username in mods:

                        if " " in msg:

                            newFails = arguments[1]
                            try:
                                newFails = int(newFails)
                            except ValueError:
                                chat.chat("Did you define a number? D:")
                                errored()
                                blab = 1
                                if debug == true:
                                    chat.chat(str(sys.exc_info()[0]))

                            if blab == 0:

                                p(str(newFails))
                                try:
                                    f = open("fails.txt", "w")
                                    f.write(str(newFails)) #writes to the file
                                    f.close

                                    chat.chat(str("Fails: Was " + str(fails) + ", now " + str(newFails))) # Tells chat.chat the new fails

                                except ValueError:
                                    errored()
                                    chat.chat("Did you define a number? D:")
                                    if debug == true:
                                        chat.chat(str(sys.exc_info()[0]))
                        else:
                            chat.chat("Did you define a number? D:")
                    else:
                        chat.chat(r"Hey! You cant do that! [mod]")

                if msg.startswith("!addfail"):
                    
                    f = open("fails.txt", "r")
                    fails = f.read() # Gets current fails
                    f.close()

                    if fails == "":
                        chat.chat("There was nothing in the fails file. Creating int of 0")
                        fails = int(0)

                    try:
                        failsInt = int(fails)

                    except ValueError:
                        chat.chat("There was an error converting the number of fails from a str to an int FeelsBadMan")
                        errored()
                        if debug == true:
                            chat.chat(str(sys.exc_info()[0]))

                    failsIntWas = failsInt

                    if username in regulars:
                        #chat.chat(r"D: this doesnt work yet! D: FeelsBadMan")
                        failsInt = failsInt + 1

                        f = open("fails.txt", "w")
                        f.write(str(failsInt)) #writes to the file
                        f.close

                        chat.chat("Fails: Was " + str(failsIntWas) + ", now: " + str(failsInt))
                        
                        
                    else:
                        chat.chat(r"Hey! You cant do that! [regular] Current fails: " + fails)                            

                if msg.startswith("!removefail"):
                    f = open("fails.txt", "r")
                    fails = f.read() # Gets current fails
                    f.close()

                    if fails == "":
                        chat.chat("There was nothing in the fails file. Creating int of 0")
                        fails = int(0)

                    try:
                        failsInt = int(fails)
                        
                    except ValueError:
                        chat.chat("There was an error converting the number of fails from a str to an int FeelsBadMan")
                        errored()
                        if debug == true:
                            chat.chat(str(sys.exc_info()[0]))

                    failsIntWas = failsInt

                    if username in regulars:
                        #chat.chat(r"D: this doesnt work yet! D: FeelsBadMan")
                        failsInt = failsInt - 1

                        f = open("fails.txt", "w")
                        f.write(str(failsInt)) #writes to the file
                        f.close

                        chat.chat("Fails: Was " + str(failsIntWas) + ", now: " + str(failsInt))
                        
                        
                    else:
                        chat.chat(r"Hey! You cant do that! [regular] Current fails: " + fails)

                # end FAILS -----------------------------------------------
                    

                if msg.startswith("!errors"):
                    if username in mods or username in allStaff or username == cfg.CHAN.lower() or username == "leotomasmc":
                        chat.chat("Errors so far: " + str(error))
                    
                if msg.startswith("!425"):
                    if username in regulars: # 425!
                        chat.chat(cfg.CHAN + " is taking a break (probably). Their chair will be entertainment until They come back!")

                if message.startswith("darkoChair"):
                    if username == "leotomasmc": # why not?
                        chat.chat(r"Chairs will rule the world with @LeotomasMC Kappa")
                    elif username == "darkosto": # because why not? Kappa
                        chat.shrug("Chairs will rule the world with Chairosto Kappa oh wait, its Darksoto, no its @Darkosto Kappa")

                if msg.startswith("!hug"):
                    blab = msg.split(" ", 1) # HUGS!!!
                    hugee = blab[1].split("\r\n")
                    hugger = username
                    chat.chat(r"/me makes " + hugger + " hug " + hugee[0] + "! HUGS! TwitchUnity bleedPurple <3")


                # CUSTOM COMMANDS -------------------------------------------
                if msg.startswith("!addcom ") or msg.startswith("!comadd "):
                    if username == cfg.CHAN.lower() or username == "leotomasmc" or username in mods:
                        if msg.count(space) >= 2:
                            try:
                                newargs = arguments[2:]
                                output = " ".join(newargs)
                                    
                                commandadd = arguments[1]
                                answer = output
                            except IndexError:
                                errored()
                                blab = 1
                                chat.chat("[ERROR] Did you use the command the right way? !addcom <commandTrigger> <output>")
                                if debug == true:
                                    chat.chat(str(sys.exc_info()[0]))
                            if blab == 0:
                                if commandadd in globalCommands:
                                    chat.chat("You cant add that command, as it is already a global TDMB command")
                                else:
                                    try:
                                        commandsList[commandadd]
                                    except KeyError:
                                        commandsList[commandadd] = answer
                                        chat.chat("The command, " + commandadd + " has been added")
                                        with open("commands.json", "w") as commandsDatabase:
                                            json.dump(commandsList, commandsDatabase)

                    else:
                        chat.chat("You dont have permission to use that command! [mod]")
                                        
                if msg.startswith("!delcom ") or msg.startswith("!comdel "):
                    if username == cfg.CHAN.lower() or username == "leotomas" or username in mods:
                        if msg.count(space) == 1:
                            try:
                                commanddel = arguments[1]

                            except IndexError:
                                chat.chat("did you use the command the right way?")
                                errored()
                                blab = 1
                                if debug == true:
                                    chat.chat(str(sys.exc_info()[0]))

                            if blab == 0:
                                if commanddel in globalCommands:
                                    chat.chat("You cant delete that command, as it is a global TDMB command")
                                else:
                                    try:
                                        p(str(commandsList[commanddel]))
                                    except KeyError:
                                        chat.chat("that command doesnt exist!")
                                        blab = 1

                                    if blab == 0:
                                        del commandsList[commanddel]
                                        chat.chat("command deleted")
                                        with open("commands.json","w") as commandsDatabase:
                                            json.dump(commandsList, commandsDatabase)
                    else:
                        chat.chat("You dont have permission to use that command! [mod]")

                if msg.startswith("!editcom ") or msg.startswith("!comedit "):
                    if username == cfg.CHAN.lower() or username == "leotomas" or username in mods:
                        if msg.count(space) >= 2:
                            try:
                                newargs = arguments[2:]
                                output = " ".join(newargs)
                                    
                                commandedit = arguments[1]
                                answer = output
                            except IndexError:
                                errored()
                                blab = 1
                                chat.chat("[ERROR] Did you use the command the right way? !editcom <commandTrigger> <output>")
                                if debug == true:
                                    chat.chat(str(sys.exc_info()[0]))
                            if blab == 0:
                                if commandedit in globalCommands:
                                    chat.chat("You cant add that command, as it is already a global TDMB command")
                                else:
                                    try:
                                        commandsList[commandedit]
                                    except KeyError:
                                        del commandList[commandedit]
                                        commandsList[commandedit] = answer
                                        chat.chat("The command, " + commandadd + " has been edited")
                                        with open("commands.json", "w") as commandsDatabase:
                                            json.dump(commandsList, commandsDatabase)
                    else:
                        chat.chat("You dont have permission to use that command! [mod]")

                # END CUSTOM COMMANDS -----------------------------------------

                # QUOTES ----------------------------------------------------

                if msg.startswith("!quotes") or msg.startswith("!quote"):
                    try:
                        if argumentsL[1] == "add":
                            if username in mods or username == cfg.CHAN.lower() or username == "leotomasmc":
                                try:
                                    newargs = arguments[2:]
                                    newQuote = " ".join(newargs)

                                    quoteNumber = len(quotes) + 1
                                except IndexError:
                                    chat.chat("D:")
                                    errored()
                                    blab = 1
                                
                                if blab == 0:
                                    try:
                                        quotes[newQuote]
                                    except KeyError:
                                        quotes[newQuote] = quoteNumber
                                        chat.chat("Quote Added!")
                                        with open("quotes.txt", "a") as f:
                                            f.write("\n")
                                            f.write(newQuote)
                                            
                            else:
                                chat.chat("You cant add a quote! [mod]")
                        elif argumentsL[1] == "del":
                            if username in mods or username == cfg.CHAN.lower() or username == "leotomasmc":
                                chat.chat("Removing Quotes: Coming Soon!")
                            else:
                                chat.chat("You cant delete a quote! [mod]")
                        else:
                            try:
                                quoteNumber = int(arguments[1])
                            except ValueError:
                                chat.chat("Did you enter a quote number?")
                                blab = 1
                            if blab == 0:
                                try:
                                    lines = open('quotes.txt').read().splitlines()
                                    myline = lines[quoteNumber]
                                    chat.chat(myline)
                                except IndexError:
                                    chat.chat("That quote doesnt exist!")

                    except IndexError:
                        try:
                            lines = open('quotes.txt').read().splitlines()
                            myline =random.choice(lines)
                            chat.chat(myline)
                        except IndexError:
                            chat.chat("There are no quotes yet!")

                # END QUOTES -------------------------------------------------------

                if msg.startswith("!color"): # color command
                    if msg.startswith("!color "):
                        if username == "leotomasmc" or username == cfg.CHAN.lower():
                            tryColor = arguments[1]
                            if arguments[1] in nonTurboColors:
                                chat.color(tryColor)
                                chat.chat("Changing color to " + tryColor)
                                chat.chat("Changed color to " + tryColor)
                            elif cfg.hasTurbo:
                                chat.color(tryColor)
                                chat.chat("Changing color to #" + tryColor)
                                chat.chat("Changed color to #" + tryColor)
                            else:
                                chat.chat("Does the bot have Twitch Prime and/or Twitch Turbo? D:")
                                
                                
                            
                            
                commands.commands(username, message) # ADVANCED custom commands
                
                for key in commandsList:
                    if msg.startswith(key): # NORMAL custom commands
                        chat.chat(str(commandsList.get(key)))

                #try:
                # Anti Link Protection -----------------------------------
                urlsInMsg = re.findall("(([\w]+:)?//)?(([\d\w]|%[a-fA-f\d]{2,2})+(:([\d\w]|%[a-fA-f\d]{2,2})+)?@)?([\d\w][-\d\w]{0,253}[\d\w]\.)+[\w]{2,63}(:[\d]+)?(/([-+_~.\d\w]|%[a-fA-f\d]{2,2})*)*(\?(&?([-+_~.\d\w]|%[a-fA-f\d]{2,2})=?)*)?(#([-+_~.\d\w]|%[a-fA-f\d]{2,2})*)?", msg)
                if urlsInMsg == []:
                    if debug == True:
                        p("No links in message!")
                else:
                    if username != "msg" or username != "Welcome":
                        p("Link found!")
                        if username in mods or username == cfg.CHAN.lower() or username == "leotomasmc":
                            p("User was allowed to post a link!")
                        elif username in permittedLinkSenders:
                            p("Allowing user to post a link, and removeing them from permitted link sender list")
                        elif username in noBanList:
                            p("User is in anti ban list")
                        elif username in regulars:
                            chat.purge(username)
                            chat.chat("Hey! " + username + "! You arent allowed to post a link! Ask first! [regular: purge]")
                        else:
                            if username == "tmi":
                                p("D:")
                            else:
                                chat.timeout(username, "60")
                                chat.chat("Hey! " + username + "! You arent allowed to post a link! Ask first! [non-regular: timeout]")

                capitalLetters = sum(1 for c in message if c.isupper())
                p(capitalLetters)
                if username == cfg.CHAN.lower() or username == "leotomasmc" or username in mods:
                    p("Caps allowed!")
                else:
                    if capitalLetters >= cfg.capLimit:
                        if username in regulars:
                            chat.purge(username)
                            chat.chat("Too many caps! [regular: purge]")
                        else:
                            chat.timeout(username, "60")
                            chat.chat("Too many caps! [non-regular: timeout]")
                            
                if debug == true:
                    p(urlsInMsg)

                if msg.startswith("!permit"):
                    if username in mods or username == cfg.CHAN.lower() or username == "leotomasmc":
                        permittedLinkSenders.append(str(arguments[1]))
                        chat.chat("Allowing " + arguments[1] + " to post 1 link. Use !clearpermits to remove all permits.")
                    else:
                        chat.chat("You dont have permission to do that [mod]")

                if msg.startswith("!clearpermits"):
                    if username in mods or username == cfg.CHAN.lower() or username == "leotomasmc":
                        permittedLinkSenders = []
                        chat.chat("Cleared all permits for links")
                    else:
                        chat.chat("You dont have permission to do that [mod]")

                # End Anti Link Protection

                # Moderation Commands
                if username in mods:
                    if msg.startswith("!subonly"):
                        if msg.startswith("!subonly "):
                            if arguments[1] in yesList:
                                chat.sub(True)
                            else:
                                chat.sub(False)



                if msg.startswith("!whisperme"):
                    chat.whisper(username, "You requested this message sent to you! Blab Blab Blab PowerUpL Kappa PowerUpR")
                    
                if msg.startswith("!eta"):
                    chat.chat("There is no ETA. In 5 minutes, there will be no ETA. Stop asking. 4Head Kappa")

                if msg.startswith("!version"): # version command (TheDerpyMemeBot: Version: beta: 1.0, random update!)
                    chat.chat("TheDerpyMemeBot: Version: " + cfg.abr + ": " + cfg.ver + ", " + cfg.verName)
                    
                    

                
                
                if msg.startswith("!tdms"): # Dev discord
                    chat.chat("The home of development for TDMB: https://discord.gg/2e3hWKH")


def _initLogWindow():
    t.__init__()
    
    root = Tk.Tk()
    root.mainloop()
    
def init_():
    ##inputSystem._init()
    p("Connectiong to twitch chat...")


    s.connect((cfg.HOST, cfg.PORT))
    s.send(bytes("PASS " + cfg.PASS.lower() + "\r\n", "UTF-8")) # joins twitch chat
    s.send(bytes("NICK " + cfg.NICK.lower() + "\r\n", "UTF-8"))
    if cfg.CHAN.startswith("#"):
        s.send(bytes("JOIN " + cfg.CHAN.lower() +"\r\n", "UTF-8"))
    else:
        s.send(bytes("JOIN #" + cfg.CHAN.lower() + "\r\n", "UTF-8"))
    s.send(bytes("CAP REQ :twitch.tv/tags :twitch.tv/commands " + cfg.CHAN.lower() + "\r\n", "UTF-8"))

##    try:
##        private.connect((cfg.HOST, cfg.PORT))
##        private.send(bytes("PASS " + cfg.PASS + "\r\n", "UTF-8"))
##        private.send(bytes("NICK " + cfg.NICK + "\r\n", "UTF-8")) # allows for reciving whispers
##        private.send(bytes("CAP REQ :twitch.tv/tags twitch.tv/commands " + cfg.CHAN + "\r\n", "UTF-8"))
##    except OSError as e:
##        print(e)
##        if e.message != "A connect request was made on an already connected socket":
##            raise
##        else:
##            print(" ""A connect request was made on an already connected socket"" Ignore this message then i geuss?")

    

    p("Connected to twitch chat.")

    p("� is the Unicode Replacement Character. It replaces any character that the Python IDLE cant understand.")
    p("You might see is when someone uses the BTTV emote :thinking: as BTTV turns it into a Unicode character.")


    refreshAll()

    if debug == true:

        chat("[DEBUG] Joined Chat")
        chat("[DEBUG] TheDerpyMemeBot is currently in debug mode!")

    p("Joining Chat")

    print(chatlist)
    

#reconnect()
