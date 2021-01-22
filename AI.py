import pyttsx3
import datetime
import wikipedia
import os
import smtplib
import sys
import speech_recognition as sr


class AIAsst():
    
    def __init__(self):
        
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.NAME=""          # YOUR NAME
        self.MALE_VOICE = voices[0].id
        self.FEMALE_VOICE = voices[1].id
        self.CRNT_VOICE=self.MALE_VOICE
        self.email_dict = {'email dictionary':"YOUR CONTACT'S EMAILS" }
        self.EMAIL_TO_USE = ''           #EMAIL TO BE USED AS A SENDING MAIL ACCOUNT
        self.MAIL_ACC_PASSWORD = ''      #PASSWORD FOR THAT MAIL ACCOUNT
        self.SMTP_URL = 'smtp.gmail.com' #SMTP SERVER TO USED
        self.SMTP_PORT_TO_USE = 587      #SMTP PORT NO.
        self.logic()
            
    
    def logic(self):
        self.wishMe()
        while True:
            try:  
                query = self.takeCommand().lower()
                words = query.split(" ")
                
                if 'wikipedia' in query:
                    self.speak(self.wiki_srch(query))

                elif 'time' in query:
                    self.tellTime(query)

                elif 'change' and 'your' and 'voice' in query:             
                    self.chng_voice()

                elif 'open ' in query:
                    query.replace("open ", "")
                    if ' chrome ' or 'google' in query:
                        os.startfile("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe")
                            

                elif 'email' in words:
                    query.replace("email", "")
                    cont = ""
                    recipient = ""
                    if words[1] in self.email_dict:
                        query.replace(words[1],"")
                        recipient = self.email_dict[words[1]]
                        if 'that' in query:
                            query.replace("that", "")
                            cont = query

                    elif recipient == "":
                        query.replace(words[1], "")
                        self.speak("to whom you wanna send email?")
                        recipient = self.takeCommand()

                    if cont == "":
                        self.speak("to " + recipient)
                        self.speak("whats the content, Sir? ")
                        cont = self.takeCommand()

                    self.mail(recipient, cont)

                elif 'exit' in query:
                    self.speak("Goodbye Sir")
                    sys.exit()

                else:
                    self.speak("please try again sir")
                    
            except Exception as e:
                print(e)
            

    def chng_voice(self,):
        
        if self.CRNT_VOICE=="female":
            self.engine.setProperty('voice',self.MALE_VOICE)
            self.CRNT_VOICE='male'
        else:
            self.engine.setProperty('voice',self.FEMALE_VOICE)
            self.CRNT_VOICE='female'
        self.speak("Voice had been succesfully changed to "+self.CRNT_VOICE)


    def speak(self,audio):
        print(audio)
        self.engine.say(audio)
        self.engine.runAndWait()


    def wishMe(self):
        hour = int(datetime.datetime.now().hour)
        str = "Good"
        if hour >= 0 and hour < 12:
            str += " Morning "
        elif hour >= 12 and hour <= 18:
            str += " evening "
        else:
            str += " Evening "

        str += f" {self.NAME}!. How may I help you?"
        self.speak(str)


    def takeCommand(self):  # FOR TAKING AUDIO INPUT FROM MIC 
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


    def wiki_srch(self,query):

        query = query.replace("wikipedia", "")
        self.speak("Searching query on wikipedia..")
        try:
            return wikipedia.summary(query, sentences=3)
        except Exception:
            return "Sorry Sir, didn't found any results .Please try again"


    def tellTime(self,query):
        str_time = datetime.datetime.now().strftime("%H:%M")
        self.speak(f"Sir, the time is {str_time}")


    def mail(self,recipient, cont):
        try:
            server = smtplib.SMTP(self.SMTP_URL,self.SMTP_PORT_TO_USE)
            server.ehlo()
            server.starttls()
            server.login(self.EMAIL_TO_USE, self.MAIL_ACC_PASSWORD)
            server.sendmail(self.EMAIL_TO_USE, recipient, cont)
            server.quit()
            self.speak("msg mailed to " + recipient)
        except Exception as ex:
            self.speak("Failed to send the mail, Sorry sir..")
            print(ex)


if __name__ == "__main__":
    AIAsst()
    

   