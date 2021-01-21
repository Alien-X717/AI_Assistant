import pyttsx3
import datetime
import wikipedia
import os
import smtplib
import sys
import speech_recognition as sr

CRNT_VOICE=''
EMAIL_TO_USE = ''       #EMAIL TO BE USED AS A SENDING MAIL ACCOUNT
MAIL_ACC_PASSWORD = ''  #PASSWORD FOR THAT MAIL ACCOUNT
SMTP_URL = 'smtp.gmail.com' #SMTP SERVER TO USED
SMTP_PORT_TO_USE = 587      #SMTP PORT NO.
email_dict = {'email':"ADD YOUR CONTACT'S EMAIL" }


def chng_voice():
    
    if CRNT_VOICE=="female":
        engine.setProperty('voice',MALE_VOICE)
        global CRNT_VOICE
        CRNT_VOICE='male'
    else:
        engine.setProperty('voice',FEMALE_VOICE)
        global CRNT_VOICE
        CRNT_VOICE='female'
    speak("Voice had been succesfully changed to "+CURRENT_VOICE)


def speak(audio):
    print(audio)
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    str = "Good"
    if hour >= 0 and hour < 12:
        str += " Morning "
    elif hour >= 12 and hour <= 18:
        str += " evening "
    else:
        str += " Evening "

    str += "Jayesh!. How may I help you?"
    speak(str)


def takeCommand():  # FOR TAKING AUDIO INPUT FROM MIC 
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("[+]Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("[.]Recognizing..")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}\n")

    except Exception as e:
        print(e)
        print("[-]Can't Recognize try again :( ")
        return "None"

    return query


def wiki_srch(query):

    query = query.replace("wikipedia", "")
    speak("Searching query on wikipedia..")
    try:
        return wikipedia.summary(query, sentences=3)
    except Exception:
        return "Sorry Sir, didn't found any results .Please try again"


def tellTime(query):
    str_time = datetime.datetime.now().strftime("%H:%M")
    speak(f"Sir, the time is {str_time}")


def mail(recipient, cont):
    try:
        server = smtplib.SMTP(SMTP_URL,SMTP_PORT_TO_USE)
        server.ehlo()
        server.starttls()
        server.login(EMAIL_TO_USE, MAIL_ACC_PASSWORD)
        server.sendmail(EMAIL_TO_USE, recipient, cont)
        server.quit()
        speak("msg mailed to " + recipient)
    except Exception as ex:
        speak("Failed to send the mail, Sorry sir..")
        print(ex)


if __name__ == "__main__":
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    MALE_VOICE = voices[0].id
    FEMALE_VOICE = voices[1].id
    CRNT_VOICE=MALE_VOICE
    wishMe()
    while True:
        try:  
            query = takeCommand().lower()
            words = query.split(" ")
            
            if 'wikipedia' in query:
                speak(wiki_srch(query))

            elif 'time' in query:
                tellTime(query)

            elif 'change' and 'your' and 'voice' in query:             
                chng_voice()

            elif 'open ' in query:
                query.replace("open ", "")
                if ' chrome ' or 'google' in query:
                    os.startfile("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe")
                        

            elif 'email' in words:
                query.replace("email", "")
                cont = ""
                recipient = ""
                if words[1] in email_dict:
                    query.replace(words[1],"")
                    recipient = email_dict[words[1]]
                    if 'that' in query:
                        query.replace("that", "")
                        cont = query

                elif recipient == "":
                    query.replace(words[1], "")
                    speak("to whom you wanna send email?")
                    recipient = takeCommand()

                if cont == "":
                    speak("to " + recipient)
                    speak("whats the content, Sir? ")
                    cont = takeCommand()

                mail(recipient, cont)

            elif 'exit' in query:
                speak("Goodbye Sir")
                sys.exit()

            else:
                speak("please try again sir")
                
        except Exception as e:
            print(e)
            