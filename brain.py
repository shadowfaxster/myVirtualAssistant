import ear as sp
import voice as vo
from cook import Cooking

import threading
import re

class NlpProcessor:
    def __init__(self):
        pass

    def decodeIntent(self, message, expectedIntent):
        intent = self.interpretMessage(message)

        if intent in expectedIntent:
            return intent;
        else:
            return "unknown"

    def interpretMessage(self, message):
        if re.search("(.*start.*cook.*)|(hungry)", message):
            intent = 'startCooking';
            return intent

        if re.search("(.*yes.*)|(.*ok.*)|(.*fine.*)", message):
            intent = 'yes'
            return intent

        if re.search("(.*no.*)|(.*nah.*)", message):
            intent = 'no'
            return intent

        if re.search(".*abort.*", message):
            intent = 'abort'
            return intent

        if re.search("(.*quit.*)|(exit)|(shutdown)", message):
            intent = 'quit'
            return intent


class Brain:
    def __init__(self):
        self.startWorking = threading.Event()

        self.loadAbilities()
        self.terminate = False;

        self.nlpProcessor = NlpProcessor()


    def loadAbilities(self):
        self.abilities = {
                            'startCooking' : self.startCooking, 
                            'unknown' : lambda: self.speak("What the fuck does that mean?"), 
                            'chat' : lambda: self.runChatBot,
                            'quit' : lambda: self.requestQuit
                          }


    def wakeOnKeyword(self):
        while not self.terminate:
            print("Waiting for keyword: Remy\n")
            self.startWorking.clear();
            listenForName = sp.listenInBackground(self.reactOnName)

            # Block here until we hear the given keyword
            self.startWorking.wait()

            # Name called => stop listening in the background
            listenForName(wait_for_stop=False)

            self.speak('Yes sir? How can I help?')
            
            message = self.listen();
            intent = self.interpret(message, list(self.abilities.keys()))

            self.processCommand(intent)

        self.shutdown()


    def interpret(self, message, expectedIntent):
        return self.nlpProcessor.decodeIntent(message, expectedIntent);


    def listen(self):
        return sp.blockingListen()

    def speak(self, message):
        vo.speak(message)


    def reactOnName(self, recognizer, audio):
        # Recognizes speech and wakes the brain when the name is called
        text = sp.recognize(recognizer, audio)

        # Listen for Remy and some common misspellings (ramy, rumy, etc)
        if re.search('r[aeu]{1}[m]{1,2}y', text.lower()):
            self.startWorking.set()


    def processCommand(self, intent):
        if intent == 'quit':
            self.terminate = True;
            return

        self.reactOnIntent(intent);


    def reactOnIntent(self, intent):
        # Check the abilities and react on intent
        self.abilities[intent]()

    def runChatBot(self):
        # Start aiml chat bot
        pass

    def startCooking(self):
        cookingAbility = Cooking(self)

        cookingAbility.start()

    def requestQuit(self):
        self.terminate = True


    def shutdown(self):
        # Shutdown all threads and whatever else
        print("Shutting down")
        pass


if __name__ == '__main__':
    b = Brain();

    try:
        b.wakeOnKeyword();

    except KeyboardInterrupt:
        b.requestQuit()
