import pyttsx3
import platform
import subprocess

sys_os = platform.system()
flMac = (sys_os == 'Darwin')

if flMac:
    import subprocess
else:
    import pyttsx3


if not flMac:
    tts = pyttsx3.init()


def speak(text):
    if flMac:
        _msg = subprocess.Popen(['echo', text], stdout=subprocess.PIPE)
        _tts = subprocess.Popen(['say'], stdin=_msg.stdout)
        _msg.stdout.close()
        _tts.communicate()
    else:
        tts.say(text)
        tts.runAndWait()


"""
class Voice:
    def __init__(self):
        # self.engine = pyttsx3.init();

        # # getter method(gets the current value
        # # of engine property)
        # voices = self.engine.getProperty('voices')
          
        # # setter method .[0]=male voice and 
        # # [1]=female voice in set Property.
        # self.engine.setProperty('voice', voices[0].id)        
        print("Voice initialized!\n")


    def speak(self, text):
        _msg = subprocess.Popen(['echo', text], stdout=subprocess.PIPE)
        _tts = subprocess.Popen(['say'], stdin=_msg.stdout)
        _msg.stdout.close()
        _tts.communicate()
# 
        # # Method for the speaking of the the assistant
        # self.engine.say(text)  

        # print("Speaking...")
        # self.engine.runAndWait()

        # print("Finished speaking 1")
        # # Wait for voice to finish before resuming
        # self.finishedSpeaking.wait()
"""