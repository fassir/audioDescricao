<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:1F9BD4,50:2E75B6,100:16265F&height=200&section=header&text=audioDescricao&fontSize=46&fontColor=ffffff&fontAlignY=38&desc=Assistente%20de%20Voz%20Inteligente%20com%20IA%20%7C%20Acessibilidade%20%7C%20PDF&descAlignY=58&descSize=15&animation=fadeIn" />

<br/>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![Whisper](https://img.shields.io/badge/Whisper-Speech_to_Text-412991?style=for-the-badge&logo=openai&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-Interface_Moderna-1F9BD4?style=for-the-badge&logo=python&logoColor=white)

<br/>

[![GitHub forks](https://img.shields.io/github/forks/fassir/audioDescricao?style=flat-square&color=1F9BD4)](https://github.com/fassir/audioDescricao/network)
[![GitHub stars](https://img.shields.io/github/stars/fassir/audioDescricao?style=flat-square&color=2E75B6)](https://github.com/fassir/audioDescricao/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/fassir/audioDescricao?style=flat-square&color=16265F)](https://github.com/fassir/audioDescricao/issues)
[![License](https://img.shields.io/badge/license-MIT-1F9BD4?style=flat-square)](LICENSE)
[![Acessibilidade](https://img.shields.io/badge/Acessibilidade-A11Y-2E75B6?style=flat-square)](https://github.com/fassir/audioDescricao)

</div>

---

## 🎙️ Sobre o Projeto

**audioDescricao** é um assistente de voz inteligente que combina o poder da **Inteligência Artificial** com foco em **acessibilidade**. O assistente pode reconhecer sua voz, responder com inteligência via ChatGPT, ler e conversar sobre documentos **PDF**, e ainda descrever a interface graficamente — tudo isso com uma interface visual moderna em modo escuro.

O projeto também está disponível como **Conversa_bot**, com a mesma base de funcionalidades.

> 💡 Criado com foco em inclusão: pyttsx3 garante audiodescrição **instantânea da interface sem necessidade de internet**, enquanto Whisper e gTTS lidam com reconhecimento e síntese de voz via nuvem.

<details>
<summary>📋 Objetivos do Projeto</summary>
<br/>

- Criar um assistente de voz acessível e inteligente
- Integrar reconhecimento de voz (Whisper/OpenAI) com GPT-4
- Permitir conversação natural com documentos PDF
- Audiodescrever a interface para deficientes visuais sem internet
- Oferecer síntese de voz de alta qualidade via gTTS
- Construir interface moderna com CustomTkinter (dark mode)
- Manter a UI responsiva com Threading assíncrono

</details>

---

## 🧠 Como Funciona

```
┌────────────────────────────────────────────────────────────────┐
│                      FLUXO PRINCIPAL                           │
│                                                                │
│  🎤 Voz do Usuário                                             │
│         │                                                      │
│         ▼                                                      │
│  ┌─────────────────┐     ┌───────────────────────────────┐    │
│  │  Whisper (OpenAI│     │  pyttsx3 (Offline)            │    │
│  │  Speech-to-Text)│     │  Audiodescrição da Interface  │    │
│  └────────┬────────┘     └───────────────────────────────┘    │
│           │ texto                                              │
│           ▼                                                    │
│  ┌────────────────────────────────┐                           │
│  │   Contexto da conversa         │                           │
│  │   + Conteúdo do PDF (se aberto)│                           │
│  └────────────────┬───────────────┘                           │
│                   │                                            │
│                   ▼                                            │
│  ┌────────────────────────────────┐                           │
│  │   ChatGPT / OpenAI API         │                           │
│  │   (Inteligência da resposta)   │                           │
│  └────────────────┬───────────────┘                           │
│                   │ resposta                                   │
│                   ▼                                            │
│  ┌────────────────────────────────┐                           │
│  │   gTTS (Google Text-to-Speech) │                           │
│  │   Síntese de voz em português  │                           │
│  └────────────────┬───────────────┘                           │
│                   │ áudio                                      │
│                   ▼                                            │
│  🔊 Resposta falada ao usuário                                 │
└────────────────────────────────────────────────────────────────┘
```

| Componente | Biblioteca | Função | Internet |
|---|---|---|---|
| 🎤 **Entrada de Voz** | Whisper (OpenAI) | Converte fala em texto | ✅ Necessária |
| 🧠 **Inteligência** | ChatGPT / OpenAI API | Gera respostas inteligentes | ✅ Necessária |
| 🔊 **Síntese de Voz** | gTTS | Converte texto em fala (alta qualidade) | ✅ Necessária |
| ♿ **Audiodescrição** | pyttsx3 | Descreve interface em tempo real | ❌ Offline |
| 📄 **Leitura de PDF** | pypdf | Extrai texto de documentos PDF | ❌ Local |
| 🖥️ **Interface** | CustomTkinter | UI moderna dark mode | ❌ Local |
| ⚡ **Threading** | threading | Mantém UI responsiva | ❌ Local |
| 🎵 **Áudio** | FFmpeg | Processamento e reprodução de áudio | ❌ Local |

---

## 🧰 Stack de Tecnologias

<div align="center">

<a href="https://skillicons.dev">
  <img src="https://skillicons.dev/icons?i=python,openai,linux&theme=dark" />
</a>

<br/><br/>

![OpenAI](https://img.shields.io/badge/OpenAI-API-412991?style=flat-square&logo=openai&logoColor=white)
![Whisper](https://img.shields.io/badge/Whisper-Speech_Recognition-412991?style=flat-square&logo=openai&logoColor=white)
![gTTS](https://img.shields.io/badge/gTTS-Google_TTS-4285F4?style=flat-square&logo=google&logoColor=white)
![pyttsx3](https://img.shields.io/badge/pyttsx3-Offline_TTS-3776AB?style=flat-square&logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-Dark_Mode_UI-1F9BD4?style=flat-square&logo=python&logoColor=white)
![pypdf](https://img.shields.io/badge/pypdf-PDF_Reader-E94B3C?style=flat-square)
![FFmpeg](https://img.shields.io/badge/FFmpeg-Audio_Processing-007808?style=flat-square&logo=ffmpeg&logoColor=white)
![Threading](https://img.shields.io/badge/Threading-UI_Async-2E75B6?style=flat-square&logo=python&logoColor=white)

</div>

---

## 🚀 Como Executar

<details>
<summary>📦 Pré-requisitos do Sistema</summary>
<br/>

```bash
# Ubuntu/Debian — Instale o FFmpeg (dependência de áudio)
sudo apt update
sudo apt install -y ffmpeg portaudio19-dev python3-pyaudio

# macOS
brew install ffmpeg portaudio

# Windows
# Baixe o FFmpeg: https://ffmpeg.org/download.html
# Adicione ao PATH do sistema
```

</details>

<details>
<summary>⚙️ Instalação</summary>
<br/>

```bash
# Clone o repositório
git clone https://github.com/fassir/audioDescricao.git
cd audioDescricao

# Crie e ative o ambiente virtual
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
# .venv\Scripts\activate    # Windows

# Instale as dependências Python
pip install -r requirements.txt
```

</details>

<details>
<summary>🔑 Configurar Chave da API OpenAI</summary>
<br/>

```bash
# Crie o arquivo de variáveis de ambiente
cp .env.example .env

# Edite o arquivo e insira sua chave OpenAI
nano .env
```

```env
# .env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

> ⚠️ Nunca commite sua chave de API no repositório. O `.env` já está no `.gitignore`.

</details>

<details>
<summary>▶️ Executar o Assistente</summary>
<br/>

```bash
# Inicie o assistente de voz
python main.py

# A interface CustomTkinter abrirá automaticamente em modo escuro
# Clique em "Iniciar" ou pressione o botão de microfone para começar
```

</details>

---

## ✨ Funcionalidades

| Funcionalidade | Descrição | Modo |
|---|---|---|
| 🎤 **Reconhecimento de Voz** | Capta e transcreve sua fala com precisão via Whisper | Online |
| 🧠 **Respostas Inteligentes** | ChatGPT responde perguntas, explica e conversa naturalmente | Online |
| 📄 **Conversa com PDF** | Abre documentos PDF e responde perguntas sobre o conteúdo | Local |
| 🔊 **Síntese de Voz (gTTS)** | Lê as respostas em voz alta com qualidade Google | Online |
| ♿ **Audiodescrição da UI** | Descreve botões e elementos da interface (pyttsx3) | **Offline** |
| 🌙 **Interface Dark Mode** | Interface moderna com CustomTkinter em tema escuro | Local |
| ⚡ **Threading Assíncrono** | Interface nunca trava durante processamento de IA | Local |
| 💬 **Histórico de Conversa** | Mantém contexto da conversa para respostas coerentes | Local |

---

## 🎨 Interface

<details>
<summary>Layout da Interface CustomTkinter</summary>
<br/>

```
┌─────────────────────────────────────────────┐
│  🎙️ audioDescricao                    [─][□][×] │
├─────────────────────────────────────────────┤
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │  💬 Histórico da Conversa           │   │
│  │                                     │   │
│  │  Você: Olá, como funciona a IA?     │   │
│  │  Bot: Ótima pergunta! A IA...       │   │
│  │  Você: Pode ler meu PDF?            │   │
│  │  Bot: Claro! Carregue o arquivo...  │   │
│  │                                     │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  ┌──────────────────┐  ┌────────────────┐  │
│  │  📁 Abrir PDF    │  │  🎤 Falar      │  │
│  └──────────────────┘  └────────────────┘  │
│                                             │
│  Status: 🟢 Aguardando entrada de voz...    │
└─────────────────────────────────────────────┘
```

</details>

---

## 📂 Estrutura de Arquivos

```
audioDescricao/
├── 📄 main.py                  # Ponto de entrada — inicializa a UI e o assistente
├── 📁 core/
│   ├── assistant.py            # Lógica principal do assistente de voz
│   ├── speech_recognition.py   # Integração Whisper para captura de voz
│   ├── text_to_speech.py       # gTTS e pyttsx3 — síntese de voz
│   ├── openai_client.py        # Integração ChatGPT / OpenAI API
│   └── pdf_reader.py           # pypdf — extração e indexação de PDF
├── 📁 ui/
│   ├── app_window.py           # Janela principal CustomTkinter
│   ├── components.py           # Widgets reutilizáveis
│   └── theme.py                # Configuração do tema escuro
├── 📁 utils/
│   ├── audio_utils.py          # Processamento de áudio com FFmpeg
│   └── context_manager.py      # Gerenciamento do histórico de conversa
├── 📄 requirements.txt         # Dependências Python
├── 📄 .env.example             # Template de variáveis de ambiente
└── 📋 README.md                # Documentação do projeto
```

---

## 📦 Dependências Principais

```txt
# requirements.txt
openai>=1.0.0          # ChatGPT + Whisper API
gtts>=2.3.0            # Google Text-to-Speech (online)
pyttsx3>=2.90          # Text-to-Speech offline
customtkinter>=5.2.0   # Interface gráfica dark mode
pypdf>=3.0.0           # Leitura de arquivos PDF
pyaudio>=0.2.13        # Captura de áudio do microfone
python-dotenv>=1.0.0   # Variáveis de ambiente
```

> ⚠️ **Dependência de sistema**: FFmpeg deve estar instalado e disponível no PATH para o processamento de áudio funcionar corretamente.

---

## ♿ Acessibilidade

Este projeto foi desenvolvido com acessibilidade como prioridade:

- **pyttsx3** funciona **completamente offline** — audiodescreve a interface instantaneamente, sem latência de rede
- **Modo escuro** reduz fadiga visual e aumenta contraste
- **Navegação por voz** permite usar o assistente sem tocar no mouse ou teclado
- **Leitura de PDFs** permite que deficientes visuais acessem documentos através de conversação natural

---

## 👤 Autor

<div align="center">

**Fabio Piassi**

[![GitHub](https://img.shields.io/badge/GitHub-fassir-1F9BD4?style=for-the-badge&logo=github&logoColor=white)](https://github.com/fassir)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Fabio_Piassi-2E75B6?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/fabiopiassi)

*Apaixonado por tecnologia, dados e soluções inteligentes.*
*Formado em Física | Especialista em Ciência de Dados, DevSecOps e IA*
*Volta Redonda — RJ 🇧🇷*

</div>

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:16265F,50:2E75B6,100:1F9BD4&height=120&section=footer&fontSize=16&fontColor=ffffff&animation=fadeIn" />

*"Não é sobre ter ideias. É sobre fazer com que elas aconteçam."*

</div>
