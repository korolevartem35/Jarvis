import os
import subprocess

IS_TERMUX = os.path.exists("/data/data/com.termux")

recognizer = None
if not IS_TERMUX:
    try:
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = 300
        recognizer.dynamic_energy_threshold = True
    except Exception as e:
        print("speech_recognition недоступен:", e)


def listen():
    if IS_TERMUX:
        return _listen_termux()
    if recognizer:
        return _listen_sr()
    return ""


def _listen_termux():
    try:
        subprocess.run(
            ["termux-microphone-record", "-f", "/sdcard/jarvis_voice.m4a", "-l", "5"],
            timeout=10
        )
        result = subprocess.run(
            ["termux-speech-to-text"],
            capture_output=True, text=True, timeout=15
        )
        return result.stdout.strip().lower()
    except Exception as e:
        print("termux listen err:", e)
        return ""


def _listen_sr():
    try:
        import speech_recognition as sr
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.4)
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=7)
        return recognizer.recognize_google(audio, language="ru-RU").lower()
    except Exception as e:
        print("sr listen err:", e)
        return ""


def speak(text):
    print("JARVIS:", text)
    if IS_TERMUX:
        try:
            subprocess.run(["termux-tts-speak", text], timeout=15)
        except Exception as e:
            print("termux tts err:", e)
        return
    try:
        from plyer import tts
        tts.speak(text)
    except Exception as e:
        print("tts err:", e)
