import speech_recognition as sr
from plyer import tts

recognizer = sr.Recognizer()
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True


def listen():
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.4)
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=7)
        return recognizer.recognize_google(audio, language="ru-RU").lower()
    except Exception as e:
        print("listen err:", e)
        return ""


def speak(text):
    print("JARVIS:", text)
    try:
        tts.speak(text)
    except Exception as e:
        print("tts err:", e)
