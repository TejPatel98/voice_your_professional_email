import speech_recognition as sr

def collect_speech():
    r = sr.Recognizer()
    mic = sr.Microphone()

    print('Listening...')
    with mic as source:
        try:
            audio = r.listen(source, timeout=5.0, phrase_time_limit=5.0)
        except:
            print('Error listening to audio!')
            return '[NO INPUT]'

    print('Parsing...')
    try :
        recognized_audio = r.recognize_google(audio)
    except:
        return '[NO INPUT]'
    return recognized_audio