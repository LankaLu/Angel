from sklearn.feature_extraction.text import CountVectorizer     #pip install scikit-learn
from sklearn.linear_model import LogisticRegression
import sounddevice as sd    #pip install sounddevice
import vosk                 #pip install vosk

import json
import queue
import words 
from skills import *
import pyttsx3
import silero_advanced



q = queue.Queue()
speak_engine = pyttsx3.init()
s = silero_advanced.synthesis()

model = vosk.Model('model_small')       #голосовую модель vosk нужно поместить в папку с файлами проекта
                                        #https://alphacephei.com/vosk/
                                        #https://alphacephei.com/vosk/models

device = sd.default.device = 1,4  # <--- по умолчанию
                                #или -> sd.default.device = 1, 3, python -m sounddevice просмотр 
samplerate = int(sd.query_devices(device[1], 'input')['default_samplerate'])  #получаем частоту микрофона


def callback(indata, frames, time, status):
    '''0
    Добавляет в очередь семплы из потока.
    вызывается каждый раз при наполнении blocksize
    в sd.RawInputStream'''

    q.put(bytes(indata))


def recognize(data, vectorizer, clf):
    '''
    Анализ распознанной речи
    '''

    #проверяем есть ли имя бота в data, если нет, то return
    trg = words.TRIGGERS.intersection(data.split())
    if trg:
        try:
            #удаляем имя бота из текста
            data = data.replace(list(trg)[0], '')

            #получаем вектор полученного текста
            #сравниваем с вариантами, получая наиболее подходящий ответ
            text_vector = vectorizer.transform([data]).toarray()[0]
            answer = clf.predict([text_vector])[0]

            #получение имени функции из ответа из data_set
            func_name = words.func[data[1:]]

            #озвучка ответа из модели data_set

            speak_engine.say(answer.replace(func_name, ''))
            speak_engine.runAndWait()
            #s.synthesisAndPlay(answer.replace(func_name, ''))

            #запуск функции из skills
            exec(func_name + '()')
        except KeyError:
            speak_engine.say("Я вас не поняла.")
            speak_engine.runAndWait()


def main():
    '''
    Обучаем матрицу ИИ
    и постоянно слушаем микрофон
    '''

    #Обучение матрицы на data_set модели
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(words.data_set.keys()))
    
    clf = LogisticRegression()
    clf.fit(vectors, list(words.data_set.values()))

    del words.data_set

    #постоянная прослушка микрофона
    with sd.RawInputStream(samplerate=samplerate, blocksize = 30000, device=device[1], dtype='int16',
                                channels=1, callback=callback):

        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                if data.startswith('ангел'): #(Тригер)(Имя помощника)
                    recognize(data, vectorizer, clf)
                elif "ангел" in data:
                    data = data[data.find("ангел") : ]
                    recognize(data, vectorizer, clf)
                    
                else:
                  print(rec.PartialResult())


if __name__ == '__main__':
    main()
