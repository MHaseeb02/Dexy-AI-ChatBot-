from main import get_responces, predict_class, intents
import pyttsx3
import speech_recognition as sr

#setting up the voice for voice command
r = sr.Recognizer()
v_engine = pyttsx3.init('sapi5')
voice = v_engine.getProperty('voices')
new_rate = 185
v_engine.setProperty('rate', new_rate)
v_engine.setProperty('voices',voice[1].id)

#function for voice output
def speak(message):
    v_engine.say(message)
    v_engine.runAndWait()

# for audio input and output (voice command)
while True:
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source,duration=0.2)
            print('listening...')
            audio= r.listen(source)
            text= r.recognize_google(audio)
            print("You: ",text)
            intent_list = predict_class(text)
            result = get_responces(intent_list,intents)
            print("Dexy:",result)
            speak(result)
    except sr.UnknownValueError:
        msg = "Oops! Didn't catch that"
        print(msg)
        speak(msg)
    except sr.RequestError:
        msg = "Oops! Something went wrong with the service"
        print(msg)
        speak(msg)