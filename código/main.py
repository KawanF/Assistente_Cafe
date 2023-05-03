import openai
import pyttsx3
import speech_recognition as sr
import os
import json

class ChatApp:
    def __init__(self, model="gpt-3.5-turbo", load_file=''):
        # Setting the API key to use the OpenAI API
        openai.api_key = "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"
        self.model = model
        self.messages = []
        if load_file != '':
            self.load(load_file)

    def chat(self, message):
        if message == "sair":
            self.save()
            os._exit(1)
        elif message == "salvar":
            self.save()
            return "(saved)"
        self.messages.append({"role": "user", "content": message})
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
            temperature=0.5,
            max_tokens=2000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            n=1
        )
        self.messages.append({"role": "assistant", "content": response["choices"][0]["message"].content})
        return response["choices"][0]["message"]["content"]
    def save(self):
        try:
            import time
            import re
            import json
            ts = time.time()
            json_object = json.dumps(self.messages, indent=4)
            filename_prefix=self.messages[0]['content'][0:30]
            filename_prefix = re.sub('[^0-9a-zA-Z]+', '-', f"{filename_prefix}_{ts}")
            with open(f"models/chat_model_{filename_prefix}.json", "w") as outfile:
                outfile.write(json_object)
        except:
            os._exit(1)

    def load(self, load_file):
        with open(load_file) as f:
            data = json.load(f)
            self.messages = data

os.environ["OPENAI_API_KEY"] = "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"

engine = pyttsx3.init()
lang = 'pt-BR'
key_word = 'café'  

def transcrever_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio, language=lang)
    except:
        print('Skipping unkown erro')

def generate_response(prompt):
      response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content":
            "You are a helpful assistant"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=2000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        n=1,
        stop=["\nUser:"]
    ) 
      return response["choices"][0]["message"]["content"]


def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    app = ChatApp(model="gpt-3.5-turbo")
    while True:
        print(f"Diga {key_word} para iniciar a gravar a sua pergunta.")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio, language=lang)
                if transcription.lower() == key_word:
                    filename = "input.wav"
                    print("Diga a sua pergunta")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename,"wb") as f:
                            f.write(audio.get_wav_data())
                        
                    
                    text = transcrever_audio_to_text(filename)
                    if text:
                        print(f"Você disse: {text}")

                        response = app.chat(text)
                        print(f"GPT disse: {response}")

                        speak_text(response)

            except Exception as e:
                print("Ocorreu um erro: {}".format(e))
                
                

if __name__ == "__main__":
    main()
