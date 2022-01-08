import speech as sp
import voice as vo
import threading
import re
from Levenshtein import distance as lev

class Brain:
    def __init__(self):
        self.startWorking = threading.Event()

        self.loadAbilities()
        self.terminate = False;


    def loadAbilities(self):
        self.abilities = {
                            'startCooking' : self.startCooking, 
                            'unknown' : lambda: vo.speak("I'm not sure what you mean."), 
                            'chat' : lambda: self.runChatBot
                          }


    def wakeOnKeyword(self):
        print("Waiting for keyword: Remy\n")
        self.startWorking.clear();
        listenForName = sp.listenInBackground(self.reactOnName)

        # Block here until we hear the given keyword
        self.startWorking.wait()

        # Name called => stop listening in the background
        listenForName(wait_for_stop=False)

        self.processCommand();


    def reactOnName(self, recognizer, audio):
        # Recognizes speech and wakes the brain when the name is called
        text = sp.recognize(recognizer, audio)

        if lev(text, 'Remy')<=1:
            self.startWorking.set()


    def processCommand(self):
        if self.terminate == True:
            self.shutdown()
            return

        vo.speak('Yes sir? How can I help?')

        command = sp.blockingListen();

        intent = self.interpretCommand(command)

        self.reactOnIntent(intent)

        # Finished task - go back to default state (idle - waiting to be called)
        self.wakeOnKeyword()


    def interpretCommand(self, command):
        # Here happens all the NLP to map a text to an intent/message that can be understood by the bot

        intent = "unknown"

        if re.search("(start cook.*)|(hungry)", command):
            intent = 'startCooking';

        return intent

    def reactOnIntent(self, intent):
        # Check the abilities and react on intent
        self.abilities[intent]()

    def runChatBot(self):
        # Start aiml chat bot
        pass

    def startCooking(self):
        cookingAbility = Cooking()

        cookingAbility.start()

    def requestQuit(self):
        self.terminate = True


    def shutdown(self):
        # Shutdown all threads and whatever else
        print("Shutting down")
        pass




# Abilities 
class Cooking:
    def __init__(self):
        print("Starting cooking routine...")

        # LOAD RECIPE DATABASE

    def start(self):
        # 1. Search recipe
        recipe = self.searchRecipe()

        # 2. Get all ingredients ready
        #self.getIngredientsOut(recipe)

        # 3. Start cooking process
        #self.startCookingProcess(recipe)


    def searchRecipe(self):
        found = False;
        while not found:
            vo.speak("Please tell me a recipe name:")

            name = sp.blockingListen();
            vo.speak("let's see what I can find for " + name)

            # search database for recipe
            recipe = "Chicken burritos"
            vo.speak("How about {}?".format(recipe))

            found = True

        return recipe


if __name__ == '__main__':
    b = Brain();

    try:
        b.wakeOnKeyword();

    except KeyboardInterrupt:
        b.requestQuit()