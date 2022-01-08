import speech_recognition as sr
import pyttsx3
import threading

def speak(audio):
    engine = pyttsx3.init()
    # getter method(gets the current value
    # of engine property)
    voices = engine.getProperty('voices')
      
    # setter method .[0]=male voice and 
    # [1]=female voice in set Property.
    engine.setProperty('voice', voices[0].id)
      
    # Method for the speaking of the the assistant
    engine.say(audio)  
      
    # Blocks while processing all the currently
    # queued commands
    engine.runAndWait()

def listenForKeyword(keyword):
    
    keepAlive = True;
    while (keepAlive):
        print("Listening for keyword " + keyword)
        q = listen();

        if (q == 'quit'):
            return;

        if (q == keyword):
            keepAlive = False;

    return;


def listen():
    r = sr.Recognizer()

    mic = sr.Microphone();
    
    with mic as source:
        print('Listening...')

        r.pause_threshold = 0.7
        audio = r.listen(source)

        try:
            print("Recognizing...")
            
            query = r.recognize_google(audio, language='en-en')
            print("the command is printed = ", query)

        except Exception as e:
            print(e)
            print("Say that again sir.")
            return "None"
          
    return query


if __name__=='__main__':
    print('Testing speech module...\n')

    listenForKeyword('Remy')

    print("\nListening for some command...");
    command = listen()
    speak("You said: " + command)

    print('\nTest finished')


"""
// 1. Cauta reteta 
-> speak('tell me a recipe name')
-> reteta = ... 


// 2. Start cooking 
-> Boil some water 
.... listen for (keyword)

-> Take the rice out of the again
.... 


initiate... 
listenForKeyword('I'm done');


nextStep...
-> speak(now .... )
-> listenForKeyword(..)

"""

