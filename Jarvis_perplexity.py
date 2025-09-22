import speech_recognition as sr        # pip inatll speech_recognition
import webbrowser           # pip inatll webbrowser 
import pyttsx3              # pip inatll pyttsx3
import music_library
import requests             # pip inatll requests 
from openai import OpenAI   # pip inatll OpenAI
import os 

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "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"  # get newsapi from google

def aiprocess(command):
    
    # Set up the API endpoint and headers
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": "Bearer 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",  # Replace with your actual API key
        "Content-Type": "application/json"
    }

    # Define the request payload
    payload = {
        "model": "sonar-pro",
        "messages": [
            {"role": "user", "content": "What were the results of the 2025 French Open Finals?"}
        ]
    }

    # Make the API call
    response = requests.post(url, headers=headers, json=payload)

    # Print the AI's response
    print(response.json()) # replace with print(response.json()["choices"][0]['message']['content']) for just the content


def speak(text):
    engine.say(text)
    engine.runAndWait()
   

def processcommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open spotify" in c.lower():
        webbrowser.open("https://spotify.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open gmail" in c.lower():
        webbrowser.open("https://gmail.com")
    elif c.lower().startwith("play"):
        song = c.lower().split(" ")[1]
        link = music_library.music(song)
        webbrowser.open(link)

    elif " news " in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&&apiKey={newsapi}")
        if r.status_code == 200:

            data = r.json()   # Convert response to Python dict
            
            articles = data.get("articles", []) # extract the articles 

            # Print only the headlines
            for article in articles:
                 speak(article.get("title"))
    else :
        # let open Ai handel the request
        output = aiprocess(c)
        speak(output)
    

                

    
if __name__ == "__main__":
    speak("Initilizating jarvis....")
    while True:

    # listen for the wake word jarvis
    # obtain audio from microphone
        r = sr.Recognizer()
        print("recognizing...")
       
        try:
            with sr.Microphone() as source:
                print("listening...")
                audio = r.listen(source , timeout=2 , phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower == "jarvis"):
                speak("yeh")
                # listen for command
                with sr.Microphone() as source:
                    print("jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processcommand(command)

        except Exception as e:
            print(f"error; {e}")
            
            
