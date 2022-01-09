import abc

class Ability:
    def __init__(self, brain):
        self.brain = brain
        self.abort = False

    def checkAbort(self):
        self.brain.speak("Would you like to abort?")

        answer = self.brain.listen()
        intent = self.brain.interpret(answer, ['yes', 'no'])

        if intent == 'yes':
            self.brain.speak("Ok, aborting process")
            self.abort == True
            return True
        else:
            return False

    @abc.abstractmethod
    def start(self):
        pass