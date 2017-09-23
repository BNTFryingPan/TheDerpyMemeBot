import bot
import commands
import sys
import time
import threading

blab = 0
breaks = 0

def startBot():
    global blab
    global breaks
    if blab == 2:
        try:
            bot.globalChat()
        except ConnectionAbortedError:
            print(str(sys.exc_info()))
            print("Connection to Twitch lost. Reconnecting...")
            print("Reconnect Coming Soon")
        finally:
            print(str(sys.exc_info))
            raise
        
def main():
    global blab
    global breaks
    
    try:
        bot.init_()
        #bot.getQuotes()
        bot.getCustomCommands()
    except:
        print("ERROR: " + str(sys.exc_info()))
        blab = 1
        
    try:
        botThread = threading.Thread(target=startBot())
        botThread.start()
        bot._initLogWindow()
        print("Blab")
    except:
        bot.p(str(sys.exc_info()))
        #bot.chat.chat("Something broke D: FeelsBadMan")
        bot.p("Oh noes! Somehow, the loop was broken! Please tell me!")
        bot.p(str(sys.exc_info()))
    else:
        print(str(sys.exc_info()))
        print("AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
        print("Send this to the developer ( LeotomasMC@outlook.com )")
    finally:
        input("")

main()
input("")
