import subprocess

import speech_recognition as sr
import os
import webbrowser
import datetime
import random
import numpy as np
import win32com.client

speaker = win32com.client.Dispatch("SAPI.SPvoice")

chatStr = ""

import requests


def chat(query_gpt):
    try:
        response = f"Imagine you are Jarvis and this is the user query: {query_gpt}"
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key"
            "=******")
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": response
                        }
                    ]
                }
            ]
        }
        response = requests.post(url, json=payload)
        response_data = response.json()

        result = response_data["candidates"][0]["content"]["parts"][0]["text"]
        print(result)
        speaker.Speak(result)

    except Exception as e:
        print("Sorry - Something went wrong. Please try again!")


def ai(prompt, te_xt=None):
    response = f"Imagine you are Jarvis and this is the user query: {prompt}"
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=******")
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": response
                    }
                ]
            }
        ]
    }

    response = requests.post(url, json=payload)
    response_data = response.json()
    generated_text = response_data.get("contents", [{"parts": [{"text": ""}]}])[0]["parts"][0]["text"]

    if te_xt is None:
        te_xt = ""

    te_xt += generated_text
    print(generated_text)
    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
        f.write(generated_text)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold =  0.6
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Jarvis"


if __name__ == '__main__':
    print('Welcome to Jarvis A.I')
    speaker.Speak("Jarvis A.I")
    while True:
        print("Listening...")
        query = takeCommand()
        # todo: Add more sites
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
                 ["google", "https://www.google.com"], ["spotify", "https://www.spotify.com"],
                 ["mail", "https://www.gmail.com"], ["instagram", "https://www.instagram.com"],
                 ["whatsapp", "https://web.whatsapp.com/"], ]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                speaker.Speak(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
        # todo: Add a feature to play a specific song
        if "open music" in query:
            spotify_exe = r"C:\Users\dell\AppData\Roaming\Spotify\Spotify.exe"
            subprocess.Popen([spotify_exe])

        elif "open calculator" in query:
            calculator_exe = "calc.exe"
            subprocess.Popen(calculator_exe)

        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            speaker.Speak(f"Sir time is {hour} hours and {min} minutes")


        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)

        elif "Jarvis Quit".lower() in query.lower():
            speaker.Speak(f"exiting program sir")
            exit()

        elif None:
            speaker.Speak(f"Sorry I could not understand")

        elif "reset chat".lower() in query.lower():
            chatStr = ""

        else:
            print("Chatting...")
            chat(query)

