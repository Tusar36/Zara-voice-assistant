import speech_recognition as sr
import pyttsx3
import webbrowser
import requests
import google.generativeai as genai
import pywhatkit
import subprocess
import time

recognizer = sr.Recognizer()
engine = pyttsx3.init("espeak")
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[11].id) 

genai.configure(api_key='AIzaSyDk04pktgLIRJfPX9UuamcYxpkzS4ubKx8')
model = genai.GenerativeModel('gemini-1.5-flash')

wake = False

chatStr =""

sites = [['facebook','https://www.facebook.com/'],
                 ['youtube','https://www.youtube.com/'],
                 ['instagram','https://www.instagram.com/'],
                 ['reddit','https://www.reddit.com/'],
                 ['linkedin','https://www.linkedin.com/'],
                 ['twitter','https://twitter.com/'],
                 ['wikipedia','https://www.wikipedia.com/']]

def listen():
    with sr.Microphone() as source:
        print("Adjusting for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        return text
    
    except sr.UnknownValueError:

        return "Could not understand the audio"
    
    except sr.RequestError as e:
        return 'internal error occured'

def speak(text):    
        engine.say(text)
        engine.runAndWait()

#underdevelopment 
def fetchData_wolframalpha(query,url,app_id):
    params = {
        'input': query,
        'format': 'plaintext',  # Choose the format you need (e.g., plaintext, image, etc.)
        'output': 'JSON',       # Output format can be XML or JSON
        'app_id': app_id         # Your WolframAlpha API key
    }
    response = requests.get(url, params=params)

#underdevelopment
def ask(question):
    app_id = "JXR6R8-87KK6QKV57"
    url =f'http://api.wolframalpha.com/v2/query?appid={app_id}'

def search_youtube(query):
    search_query = '+'.join(query.split())
    url = f"https://www.youtube.com/results?search_query={search_query}"
    print(url)
    return url

def play_video(search_item):
    pywhatkit.playonyt(search_item)

#under development
def get_weather(city):

    unix_timestamp = int(time.time())    
    details = get_longi_and_lati(city)

    weather_api_key = 'b42da287a99bd54c397ba152ced27357'

    url = f'https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={details['Latitude']}&lon={details['Longitude']}&dt={unix_timestamp}&appid={weather_api_key}'

    res = requests(url)

    print(res)


def get_longi_and_lati(city):
    url = f'https://api.api-ninjas.com/v1/geocoding?city={city}&country='
    key = 'SpPlYy9FTM2N4Tiw7nKqQg==46fOKKl1b10tWwHb'
    response = requests.get(url + city, headers={'X-Api-Key': f'{key}'})
    output = response.json()
    latitude = output[0]["latitude"]
    longitude = output[0]["longitude"]
    return {'Latitude':latitude,'Longitude':longitude}


def get_news(category):
    key = 'b0a71354d08d4c1394c5aa9ea8148e43'
    if 'top headlines' in category.lower():
        res = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey=b0a71354d08d4c1394c5aa9ea8148e43&pageSize=5")
        des = []
        for news in res.json()['articles']:
            des.append(news['title'])
        return(des)
    else:
        res = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey=b0a71354d08d4c1394c5aa9ea8148e43&pageSize=5&category={category}")
        des = []
        for news in res.json()['articles']:
            des.append(news['title'])
        return(des)

#under development
def get_stock_exchange():
    pass

def chat(query,question=True):

    global chatStr

    if question:
        response = model.generate_content(f'Your are Zara ai you are developed in python by tusar and work as an ai assistant answer this no special character like * or :,\n{query}')
        print(response.text)
        return response.text
    else:  
        chatStr=chatStr+''+ f"\n User:{query}"

        response = model.generate_content(f"Your are Zara ai you are developed in python by tusar and work as an ai assistant and here is your description 'Powered by Python and Arduino, I can help with tasks like opening YouTube, playing music, answering questions, and chatting with you. Currently, my physical movements are limited to moving my hands and head, but I can be enhanced to include more features like home automation and advanced tasks with Arduino. Essentially, I use Python to understand and execute your voice commands, while Arduino controls my physical movements, making me a versatile and interactive assistant.' if you asked to open any app or play music say 'you are in chat mode to execute that function exit chat mode, no emojis, no special characters no bodl characters, respond to this promot:\n {chatStr} ")

        chatStr=chatStr+''+f"\n User:{response.text}"

        return response.text

if __name__ == '__main__':
    while True:
        if not wake:
            command = listen()
            if 'wake up'.lower() in command.lower():
                speak('Starting Zara AI')
                speak('Listning')
                wake = True

        if wake:
            while(1):
                input = listen().lower()

                if "hello".lower() in input.lower():
                    speak('Hello there, I am zara at your service')

                # description
                elif 'describe yourself' in input.lower():
                    speak('Hello! I’m Zara, your AI voice assistant designed by Tusar to make your life easier. Powered by Python and Arduino, I can help with tasks like opening YouTube, playing music, answering questions, and chatting with you. Currently, my physical movements are limited to moving my hands and head, but I can be enhanced to include more features like home automation and advanced tasks with Arduino. Essentially, I use Python to understand and execute your voice commands, while Arduino controls my physical movements, making me a versatile and interactive assistant.')  

                # ai promt 
                elif "answer this".lower() in input.lower():

                    speak("What is the question?")

                    while True:
                        question = listen()

                        if question.lower() == 'Could not understand the audio'.lower():
                            speak('unable to understand your question try again')    
                        else:
                            output = chat(question)
                            speak(output)

                #Youtube video palyer
                elif 'play'.lower() in input.lower():
                    search_term = input.split("play")[-1]
                    speak(f'Playing {search_term}')
                    play_video(search_term)
                    
                #open chrome (under development)  
                elif 'open chrome' in input.lower():
                    subprocess.run('google-chrome')
                
                # opening site
                elif 'open'.lower() in input.lower():
                    found_site = False
                    for site in sites:
                        if f"Open {site[0]}".lower() in input.lower():
                            speak(f'Opening  {site[0]}')
                            webbrowser.open(site[1])
                            found_site = True
                    if found_site == False:
                            search_term = input.split("open")[-1]
                            url = f"https://google.com/search?q={search_term}"
                            webbrowser.get().open(url)
                            speak(f'Here is what I found for {search_term} on google')  

                #searching for items on google
                elif "search for".lower() in input.lower():
                    search_term = input.split("for")[-1]
                    url = f"https://google.com/search?q={search_term}"
                    webbrowser.get().open(url)
                    speak(f'Here is what I found for {search_term} on google')

                # for wikipedia information
                elif 'summarise'.lower() in input.lower():
                    search_term = input.split("summarise")[-1]
                    speak(chat('summarise '+search_term))

                #ai chatting system 
                elif 'start chat'.lower() in input.lower():
                    speak("Chat Mode started, you can ask questions, doubts or simply chat")
                    while True:
                        query = listen()
                        if query.lower() == 'Could not understand the audio'.lower():
                            speak('unable to understand your question try again')
                            continue
                        elif 'exit chat mode' in query.lower():
                            speak('exiting chat mode, you chat records will be cleared')
                            chatStr="" 
                            break
                        elif 'clear chat' in query.lower():
                            speak('chat history cleared')
                            chatStr=""
                            break
                        else:
                            res = chat(query,question=False)
                            speak(res)
               
                #get news
                elif 'get news'.lower() in input.lower():
                    query = input.lower().replace('get news','')
                    res = get_news(query)
                    if len(res) == 0:
                        speak('no news found')
                    else:
                        for i in res:
                            speak(i)    
                           
                #exit command
                elif 'exit'.lower() in input.lower():
                    speak('Exiting Zara Ai')
                    wake = False
                    break

                else:
                    speak(input)    
                