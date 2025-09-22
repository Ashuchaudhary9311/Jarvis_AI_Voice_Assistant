import speech_recognition as sr      # pip install SpeechRecognition
import webbrowser
import pyttsx3                       # pip install pyttsx3
import music_library
import requests                      # pip install requests
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Replace this with your actual NewsAPI key
newsapi = "88cefd025106417b937725ae768576bd"


def aiprocess(c):
   
    # Sends user command to Perplexity AI and returns response text.
   
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer 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",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "sonar-pro",
        "messages": [
             {"role": "system", "content": "You are AI Assistant similer to alexa and Keep your response  short and only reponse answers."  
                            " Do not over-explain or give long answers"
                            " Reply casually and in a friendly tone"  
                            },
            {"role": "user", "content": c}
        ]
             
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            return "Sorry, I couldn't understand the response."
    else:
        return f"Error: {response.status_code}"


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
    elif c.lower().startswith("play"):
        try:
            song = c.lower().split(" ", 1)[0]
            link = music_library.music(song)
            webbrowser.open(link)
        except IndexError:
            print("Please specify a song name.")
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get("articles", [])
            for article in articles[:5]:  # Read only top 5 headlines
                print(article.get("title"))
        else:
            print("Failed to fetch news.")
    else:
        output = aiprocess(c)
        print(output)


if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source , timeout=3, phrase_time_limit=2)
            word = recognizer.recognize_google(audio)

            if word.lower() == "jarvis":
                print("Yes..")
                with sr.Microphone() as source:
                    print("Jarvis active, listening for command...")
                    audio = recognizer.listen(source, timeout=5)
                    command = recognizer.recognize_google(audio)
                    processcommand(command)

        except Exception as e:
            print(f"Error: {e}")
