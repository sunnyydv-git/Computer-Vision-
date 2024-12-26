import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import datetime

recognizer = sr.Recognizer()
phoneNumbers = {"abc":"34534", "xyz":"243434", "mno":"239329"}
bankAccNo = {"sbi":"9878928938", "axis bank":"2342352525", "pnb" : "3495345345"}

def speak(command):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(command)
    engine.runAndWait()

# speak('Welcome to project, buddy')

def commands():
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print('Listening...Ask Now!')
            audioin = recognizer.listen(source)
            my_text = recognizer.recognize_google(audioin)
            my_text = my_text.lower()
            print(my_text)
            # speak(my_text)

            # ask to play song
            if 'play' in my_text:
                my_text = my_text.replace('play', '')
                speak('Playing' + my_text)
                pywhatkit.playonyt(my_text)
            
            # ask date
            elif 'date' in my_text:
                today = datetime.date.today()
                speak(today)
            
            # ask time
            elif 'time' in my_text:
                timenow = datetime.datetime.now('%H:%M')
                speak(timenow)

            # ask details about a person
            elif "who is" in my_text:
                person = my_text.replace('who is', '')
                info = wikipedia.summary(person, 1)
                speak(info)

            # ask phone numbers
            elif "phone number" in my_text:
                names = list(phoneNumbers)
                print(names)
                for name in names:
                    if name in my_text:
                        print(name + "phone number is " + phoneNumbers[name])
                        speak(name + "phone number is " + phoneNumbers[name])

            # ask personal bank account number
            elif "account number" in my_text:
                banks = list(bankAccNo)
                for bank in banks:
                    if bank in my_text:
                        print(bank + "bank account number is " + bankAccNo[bank])
                        speak(bank + "bank account number is " + bankAccNo[bank])
            else:
                speak('Please ask correct question.')
    except:
        print('Error in capturing microphone...!')
while True:
    commands()

