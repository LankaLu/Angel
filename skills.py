import os
import sys
import subprocess
import webbrowser
import pyttsx3
import requests

from dates import getDate, get_time, get_datetime

# запуск движка при старте
engine = pyttsx3.init()
engine.setProperty('rate', 180)  # скорость речи

def speaker(text):
    '''ОЗВУЧКА ТЕКСТА'''
    engine.say(text)
    engine.runAndWait()

def here():
    ()

def weather():
    ()

def offBot():
    exit()

def stop():
    ()

def browser():
    webbrowser.open('http://www.google.com')

def window():
    webbrowser.open('http://www.google.com')

def offpc():
    os.system('shutdown /s /t 0')

def restart():
    os.system('shutdown -r -t 0')

def video():
    webbrowser.open('http://www.youtube.com')

def vk():
    webbrowser.open('https://vk.com')

def tgveb():
    webbrowser.open('https://web.telegram.org')

def odnok():
    webbrowser.open('https://ok.ru')

def time():
    (get_time()[1])

def date():
    (getDate()[1])

def passive():
    pass
