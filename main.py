import openai  # Importa o módulo openai para interagir com a API GPT-3
import pyttsx3  # Importa o módulo pyttsx3 para converter texto em fala
import speech_recognition as sr  # Importa o módulo speech_recognition para transcrever áudio em texto
import os  # Importa o módulo os para interagir com o sistema operacional
import json  # Importa o módulo json para trabalhar com dados em formato JSON
import time  # Importa o módulo time para lidar com operações relacionadas ao tempo
import re  # Importa o módulo re para realizar correspondência de padrões com expressões regulares


class ChatApp:
    def __init__(self, model="gpt-3.5-turbo", load_file=''):
        # Inicializa a classe ChatApp com as configurações fornecidas
        # model: O modelo de linguagem a ser usado (padrão: "gpt-3.5-turbo")
        # load_file: O arquivo JSON contendo mensagens anteriores (opcional)

        openai.api_key = os.environ["OPENAI_API_KEY"]
        self.model = model  # Define o modelo de linguagem a ser usado
        self.messages = []  # Lista para armazenar as mensagens da conversa

        # Adiciona a mensagem de sistema inicial à lista de mensagens
        self.messages.append({"role": "system", "content": role})

        if load_file != '':
            self.load(load_file)  # Carrega mensagens anteriores do arquivo, se fornecido

    def chat(self, message):
        # Realiza a interação entre o usuário e o assistente de chat
        # message: A mensagem do usuário

        if message == "sair":
            self.save()  # Salva as mensagens em um arquivo antes de sair
            os._exit(1)  # Sai do programa

        elif message == "salvar":
            self.save()  # Salva as mensagens em um arquivo
            return "(salvo)"  # Retorna uma mensagem indicando que as mensagens foram salvas com sucesso

        self.messages.append({"role": "user", "content": message})  # Adiciona a mensagem do usuário à lista de mensagens

        # Faz uma solicitação para a API GPT-3 para obter uma resposta
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
            temperature=0.5,
            max_tokens=4000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            n=1
        )

        self.messages.append({"role": "assistant", "content": response["choices"][0]["message"].content})  # Adiciona a resposta do assistente à lista de mensagens

        return response["choices"][0]["message"]["content"]  # Retorna a resposta do assistente

    def save(self):
        try:
            ts = time.time()  # Obtém o timestamp atual
            json_object = json.dumps(self.messages, indent=4)  # Converte a lista de mensagens para JSON
            filename_prefix = self.messages[0]['content'][0:30]  # Obtém o prefixo do nome do arquivo a partir da primeira mensagem
            filename_prefix = re.sub('[^0-9a-zA-Z]+', '-', f"{filename_prefix}_{ts}")  # Formata o prefixo do nome do arquivo
            with open(f"código/chat_model_{filename_prefix}.json", "w") as outfile:
                outfile.write(json_object)  # Salva o JSON no arquivo
        except:
            os._exit(1)  # Sai do programa em caso de erro

    def load(self, load_file):
        with open(load_file) as f:
            data = json.load(f)  # Carrega o JSON a partir do arquivo
            self.messages = data  # Atualiza a lista de mensagens com os dados carregados


def transcrever_audio_to_text(filename):
    recognizer = sr.Recognizer()  # Inicializa o objeto Recognizer do SpeechRecognition
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)  # Lê o áudio do arquivo
    try:
        return recognizer.recognize_google(audio, language=lang)  # Transcreve o áudio para texto usando a API do Google
    except:
        print('Skipping unknown error')  # Ignora erros desconhecidos durante a transcrição


def speak_text(text):
    engine.say(text)  # Converte o texto em fala
    engine.runAndWait()  # Executa a fala


os.environ["OPENAI_API_KEY"] = "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"  # Define a chave da API do OpenAI
engine = pyttsx3.init()  # Inicializa o mecanismo de fala do pyttsx3
lang = 'pt-br'  # Define o idioma para reconhecimento de fala como português brasileiro
key_word = 'café'  # Palavra-chave para iniciar a gravação da pergunta
role = "You are a helpful assistant, answer in pt-br"  # Papel do assistente na conversa


def main():
    app = ChatApp("gpt-3.5-turbo")  # Cria uma instância da classe ChatApp com o modelo especificado
    recognizer = sr.Recognizer()  # Inicializa o objeto Recognizer do SpeechRecognition

    while True:
        print(f"Diga {key_word} para iniciar a gravação da sua pergunta.")
        with sr.Microphone() as source:
            audio = recognizer.listen(source)  # Escuta o áudio do microfone
            try:
                transcription = recognizer.recognize_google(audio, language=lang, show_all=False)  # Transcreve o áudio para texto
                if transcription.lower() == key_word:
                    filename = "input.wav"  # Define o nome do arquivo de áudio
                    print("Diga a sua pergunta")
                    with sr.Microphone() as source:
                        source.pause_threshold = 2
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)  # Escuta o áudio da pergunta
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())  # Salva o áudio no arquivo

                    text = transcrever_audio_to_text(filename)  # Transcreve o áudio para texto
                    if text:
                        print(f"Você disse: {text}")
                        response = app.chat(text)  # Interage com o assistente de chat
                        print(f"GPT disse: {response}")
                        speak_text(response)  # Converte a resposta do assistente em fala
                 

            except Exception as e:
                print("Ocorreu um erro: {}".format(e))  # Manipula erros durante a transcrição ou interação com o assistente


if __name__ == "__main__":
    main()  # Executa a função principal do programa
