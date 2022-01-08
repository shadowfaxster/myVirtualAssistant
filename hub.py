import threading
import brain
import speechModule

class Hub:
    def __init__(self):
        self.barier = threading.Barrier()

        self.waitingForCommand = threading.Event()

        self.initializeModules()
        self.start()

    def initializeModules(self):
        self.brain = Brain()
        self.speech = Speech


    def start(self):

        self.waitingForCommand.wait();

