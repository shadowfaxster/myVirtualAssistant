import ability
import aiml

class ChatBot(ability.Ability):
    def __init__(self, brain):
        super().__init__(brain)

        self.k = aiml.Kernel()

        self.k.learn("std-startup.xml")
        self.k.respond("load aiml b")

    def start(self):
        self.brain.speak("Ok. Let's chat.")

        while not self.abort:
            message = self.brain.listen()

            intent = self.brain.interpret(message, ['abort'])
            if intent == 'abort':
                self.checkAbort()
            else:
                response = self.k.respond(message)
                self.brain.speak(response)


    def chatFromKeyboard(self):
        while True:
            print(self.k.respond(input("Enter your message >> ")))



if __name__ == '__main__':
    import brain

    brain = brain.Brain()

    chatter = ChatBot(brain)
    #chatter.start()

    chatter.chatFromKeyboard()