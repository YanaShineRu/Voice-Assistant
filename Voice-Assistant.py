import speech_recognition as sr
import requests
import os
import webbrowser
import threading
import pyttsx3

def open_website(url):
    webbrowser.open(url)

def main():
    active = False  # Флаг активации помощника
    activation_keywords = ["Яна", "яна", "янчка", "янчик", "янусь"]  # Кодовые слова для активации

    engine = pyttsx3.init()
    engine.setProperty('voice', "voice[1].id")
    engine.setProperty('rate', 140)
    engine.runAndWait()

    while True:
        if not active:
            activation_phrase = recognize_speech().lower()
            if any(keyword in activation_phrase for keyword in activation_keywords):
                active = True
                speak(engine, "Помощник Яна активирована. Говорите команду.")
            else:
                # Запускаем таймер отсчета до перехода в режим ожидания
                timer = threading.Timer(10, handle_timeout)
                timer.start()
        else:
            command = recognize_speech()
            if command.lower() == "выключить":
                speak(engine, "До свидания!")
                active = False  # Сброс флага активации
            elif command.lower().startswith("открыть сайт"):
                url = command[12:]  # Получить URL из команды
                open_website(url)
            else:
                perform_action(command)

def handle_timeout():
    global active
    speak(engine, "Режим ожидания. Активируйте помощника, произнеся кодовое слово.")
    active = False

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)  # Настройка уровня шума
        print("Говорите...")
        try:
            audio = r.listen(source, timeout=10)  # Ожидание команды пользователя в течение 10 секунд
            text = r.recognize_google(audio, language="ru")
            print("Распознано: " + text)
            return text
        except sr.UnknownValueError:
            print("Не удалось распознать речь")
            return ""
        except sr.WaitTimeoutError:
            print("Превышено время ожидания команды")
            return ""

def speak(engine, text):
    engine.say(text)
    engine.runAndWait()

def run_program(program_name):
    program_name = program_name.lower()  # Привести команду к нижнему регистру для сравнения
    if program_name in ["открой браузер", "открыть браузер","запусти хром", "открыть гугл хром", "открыть google chrome"]:
        os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
    elif program_name == "музыкальный плеер":
        os.startfile("C:\\Путь\\к\\музыкальному_плееру.exe")
    else:
        print("Не удалось найти программу.")

def perform_action(action):
    if action.lower() == "перезагрузить":
        os.system("shutdown /r /t 0")  # Перезагрузить компьютер
        speak("Перезагружаю компьютер")  # Голосовое оповещение о перезагрузке
    elif action.lower() == "выключить":
        os.system("shutdown /s /t 0")  # Выключить компьютер
        speak("Выключаю компьютер")  # Голосовое оповещение о выключении
    elif action.lower() == "отложенное отключение":
        delay = input("Укажите задержку перед отключением (в минутах): ")
        os.system(f"shutdown /s /t {int(delay) * 60}")  # Отложенное отключение
        speak(f"Отключаю компьютер через {delay} минут")  # Голосовое оповещение об отключении
    else:
        print("Неизвестная команда.")

if __name__ == "__main__":
    main()
