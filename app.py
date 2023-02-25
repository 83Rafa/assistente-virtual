import speech_recognition as sr
import playsound
from gtts import gTTS
import random
import webbrowser
import pyttsx3
import os


class VirtualAssit():
    def __init__(self, assist_name, person):
        self.person = person
        self.assit_name = assist_name

        self.engine = pyttsx3.init()
        self.r = sr.Recognizer()

        self.voice_data = ''

    def engine_speak(self, text):
        # fala da assitente virtual
        text = str(text)
        self.engine.say(text)
        self.engine.runAndWait()

    def record_audio(self, fala=""):

        with sr.Microphone() as source:
            if fala:
                print('Olá! Estou ouvindo...')
                self.engine_speak(fala)

            audio = self.r.listen(source, 5, 5)  # pega dados de audio
            print('Estou procurando...')
            try:
                self.voice_data = self.r.recognize_google(audio)  # converte audio para texto

            except sr.UnknownValueError:
                self.engine_speak('Desculpe, eu não entendi. Pode repetir?')

            except sr.RequestError:
                self.engine_speak('Me perdoe, meu servidor está offline')  # recognizer is not connected

            print(">>>", self.voice_data.lower())  # imprime o que vc disse
            self.voice_data = self.voice_data.lower()

            return self.voice_data.lower()

    def engine_speech(self, audio_strig):
        audio_strig = str(audio_strig)
        tts = gTTS(text=audio_strig, lang='pt')
        r = random.randint(1, 10000)
        audio_file = 'audio' + str(r) + '.mp3'
        tts.save(audio_file)
        playsound.playsound(audio_file)
        print(self.assit_name + ':', audio_strig)
        os.remove(audio_file)

    def there_exist(self, terms):
        # função para identificar se o termo existe
        for term in terms:
            if term in self.voice_data:
                return True

    def respond(self, voice_data):
        if self.there_exist(['Bom dia Edite', 'Boa tarde Edite', 'Boa noite Edite', 'oi Edite', 'olá Edite']):
            greetigns = [f'Oi {self.person}, como vai? O que precisa?',
                         f'Olá {self.person} no que posso ajudar?',
                         f'Tudo bem {self.person}? Precisa de algo?']

            greet = greetigns[random.randint(0, len(greetigns) - 1)]
            self.engine_speak(greet)

        try:
            # google
            if self.there_exist(['pesquise por']) and 'youtube' not in voice_data:
                search_term = voice_data.split("for")[-1]
                url = "http://google.com/search?q=" + search_term
                webbrowser.get().open(url)
                self.engine_speak("Aqui está o que encontrei sobre " + search_term + 'no google')

            # youtube
            if self.there_exist(["busca no youtube"]):
                search_term = voice_data.split("no")[-1]
                url = "http://www.youtube.com/results?search_query=" + search_term
                webbrowser.get().open(url)
                self.engine_speak("Aqui está o que encontrei sobre " + search_term + 'no youtube')

            # apps
            if self.there_exist(['abre o word']):
                os.system("start Word.exe")
            elif self.there_exist(['abre o excel']):
                os.system("start Excel.exe")
        except sr.UnknownValueError:
            print('Desculpe, não entendi. Pode repetir?')
            self.engine_speak('Desculpe, não entendi. Pode repetir?')


if __name__ == '__main__':
    assistent = VirtualAssit('Edite', 'Rafael')

    while True:
        voice_data = assistent.record_audio('Olá! Estou ouvindo...')
        assistent.respond(voice_data)

        if assistent.there_exist(['não', 'até', 'tchau', 'vejo você depois', 'até mais']):
            assistent.engine_speak("Ok. Tenha um ótimo dia! Tchau!")
            break