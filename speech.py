import speech_recognition as sr

import threading
import queue


def recognize(recognizer, audio):
    try:
        utterance = recognizer.recognize_google(audio, language='en-en')
        print("Recognizing command is printed = ", utterance)

        return utterance
    
    except Exception as e:
        print(e)
        print("Say that again sir.")
        return "None"

# Starts a listening process on a background thread
def listenInBackground(callback):
    print("Listening in background...\n")

    r = sr.Recognizer()
    m = sr.Microphone()
    with m as source:
        r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening

    r.pause_threshold = 0.7;
    backgroundListen = r.listen_in_background(m, callback);

    return backgroundListen;


def blockingListen():
    utterance = []

    r = sr.Recognizer();
    mic = sr.Microphone();
    with mic as source:
        print('Listening...')

        r.adjust_for_ambient_noise(source) 

        while not utterance:
            r.pause_threshold = 1
            audio = r.listen(source)

            try:
                print("Recognizing...")
                
                utterance = r.recognize_google(audio, language='en-en')
                print("the command is printed = ", utterance)

            except Exception as e:
                print(e)
                print("Say that again sir.")
                utterance = []

    return utterance


"""
class ListenerOnKeyword(threading.Thread):
    def __init__(self, commandQueue, commandReadyToProcess, keyword):
        threading.Thread.__init__(self)

        self.commandQueue = commandQueue;
        self.commandReadyToProcess = commandReadyToProcess

        self.keyword = keyword;

        self.resume = threading.Event();

        self.terminate = False;

    def stop(self):
        self.terminate = True;

    def run(self):
        print("Listening for keyword {} on thread {}".format(self.keyword, threading.get_ident()))
        global ear
        global voice

        while (not self.terminate):
            self.resume.wait();

            w = ear.listen(1);

            if (w == 'quit'):
                break;

            if (w == self.keyword):
                # User called on assistant - expect a command
                print("Keyword identified...\n")
                voice.speak("Yes Sir?");

                command = ear.listen(1);

                self.commandQueue.put(command);
                self.commandReadyToProcess.set();

        print("Terminating listener!")

class Ear:
    def __init__(self):
        self.r = sr.Recognizer();

        self.mic = sr.Microphone();

    def listen(self, timeout):
        query = []

        with self.mic as source:
                print('Listening...')

                try:
                    self.r.pause_threshold = 0.7
                    audio = self.r.listen(source, timeout=1)

                    try:
                        print("Recognizing...")
                        
                        query = self.r.recognize_google(audio, language='en-en')
                        print("the command is printed = ", query)

                    except Exception as e:
                        print(e)
                        print("Say that again sir.")
                        return "None"
            
                except sr.WaitTimeoutError:
                    print("Timedout")
                    pass

        print("Returning\n")     
        return query
      
   

if __name__=='__main__':
    print('Testing speech module...\n')

    fifo_queue = queue.Queue()
    waitOnCommand = threading.Event()
    
    listenerOnKeyword = ListenerOnKeyword(fifo_queue, waitOnCommand, 'Remy');
    listenerOnKeyword.start();

    waitOnCommand.wait()

    listenerOnKeyword.stop()
    listenerOnKeyword.join()

    print('\nTest finished')