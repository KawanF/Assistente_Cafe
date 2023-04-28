import openai
import pyttsx3
import speech_recognition as sr

openai.api_key = "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"

engine = pyttsx3.init()
lang = 'pt-BR'

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
            "You are a helpful assistant for a 80 years old lady."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.5,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        n=1,
        stop=["\nUser:"],
    ) 
      return response["choices"][0]["message"]["content"]


def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        print("Diga 'GPT' para iniciar a gravar a sua pergunta.")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio, language=lang)
                if transcription.lower() == "gpt":
                    filename = "/input.wav"
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

                        response = generate_response(text)
                        print(f"GPT disse: {response}")

                        speak_text(response)

            except Exception as e:
                print("Ocorreu um erro: {}".format(e))

if __name__ == "__main__":
    main()