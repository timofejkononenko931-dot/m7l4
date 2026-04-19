import sounddevice as sd
import random
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from translate import Translator
import time

text = """
 d8888b. db    db  .d88b.  db      d888888b d8b   db  d8888b.  .d88b. 
 88  `8D 88    88 .8P  Y8. 88        `88'   888o  88 88  `8D .8P  Y8.
 88   88 88    88 88    88 88         88    88V8o 88 88   88 88    88
 88   88 88    88 88    88 88         88    88 V8o88 88   88 88    88
 88  .8D 88b  d88 `8b  d8' 88booo.   .88.   88  V888 88  .8D `8b  d8'
 Y8888D' ~Y8888P'  `Y88P'  Y88888P Y888888P VP   V8P Y8888D'  `Y88P' 

                          on Python

"""

print(text)
print("Игра загружается...\n\n")

time.sleep(3)

HEALTH = 3
BALL = 0

print("Привет! Давай сыграем в игру, я вывожу слово а ты должен его сказать на английском языке,\n а я его распознаю и скажу правильно ли ты его произнёс, у тебя 3 попыти")
print("чтобы победить нужно набрать 5 очков")
print("Если ты готов, то поехали!")
print("Выбери уровень сложности: easy, medium, hard")
level = input("Уровень сложности: ").lower()

print("\n\n\n")

words_by_level = {
    "easy": ["кот", "собака", "яблоко", "молоко", "солнце"],
    "medium": ["банан", "школа", "друг", "окно", "жёлтый"],
    "hard": ["технология", "университет", "информация", "произношение", "воображение"]
}

while HEALTH > 0 and BALL < 5:
    if level == "easy":
        word = random.choice(words_by_level["easy"])
        print(word)
    elif level == "medium":
        word = random.choice(words_by_level["medium"])
        print(word)
    elif level == "hard":
        word = random.choice(words_by_level["hard"])
        print(word)
    else:
        print("Неверный уровень сложности. Выбираю easy по умолчанию.\n\n")
        word = random.choice(words_by_level["easy"])
        print(word)

    duration = 5  # секунды записи
    sample_rate = 44100

    print("Говори...")
    recording = sd.rec(
      int(duration * sample_rate), # длительность записи в сэмплах
      samplerate=sample_rate,      # частота дискретизации
      channels=1,                  # 1 — это моно
      dtype="int16")               # формат аудиоданных
    sd.wait()  # ждём завершения записи

    wav.write("output.wav", sample_rate, recording)
    print("Запись завершена, теперь распознаём...\n")

    recognizer = sr.Recognizer()
    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)  # читаем аудиофайл



    try:
        text = recognizer.recognize_google(audio, language="en-US")  # распознаём с помощью Google API
        print("Ты сказал:", text)

    except sr.UnknownValueError:             # - если Google не понял речь (шум, молчание)
        print("Не удалось распознать речь.")
    except sr.RequestError as e:             # - если нет интернета или API недоступен
        print(f"Ошибка сервиса: {e}")

    translator = Translator(to_lang='en')  # указываем язык, на который хотим перевести
    translated = translator.translate(word)  # здесь 'en' — это английский

    if translated.lower() == text.lower():
        print("Правильно! Ты молодец!")
        BALL += 1
        print(f"Твой счёт: {BALL}")
    if translated.lower() != text.lower():
        HEALTH -= 1
        print(f"Неправильно! Осталось попыток: {HEALTH}\n")

if HEALTH <= 0:
    print("Игра окончена, ты проиграл! Твой итоговый счёт:\n", BALL)
elif BALL >= 5:
    print("Игра окончена, ты победил! Твой итоговый счёт:\n", BALL)