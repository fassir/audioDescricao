# Conversa Bot - Assistente de Voz com IA, Acessibilidade e Leitura de Documentos

Este é um projeto de assistente virtual inteligente capaz de conversar por voz, entender texto e ler documentos (como livros em PDF). Ele foi construído para ser moderno, acessível e fácil de usar.

O projeto utiliza **OpenAI (ChatGPT)** para inteligência, **Whisper** para ouvir você, e **gTTS** para falar de volta.

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
Antes de começar, você precisa ter instalado no seu computador:
1.  **Python 3**: A linguagem de programação usada.
2.  **FFmpeg**: Uma ferramenta essencial para trabalhar com áudio (necessária para o Whisper).
    -   *Windows*: `winget install ffmpeg`
3.  **Chave da OpenAI**: Um código secreto para usar o "cérebro" do ChatGPT.

### Instalação Passo a Passo

1.  **Baixe o código** (Clone ou Download).
2.  **Instale as "peças" necessárias (bibliotecas)**:
    Abra o terminal na pasta do projeto e digite:
    ```bash
    pip install -r requirements.txt
    ```
    Isso vai baixar tudo que o robô precisa para funcionar (cérebro, ouvidos, voz, interface, leitor de PDF).
3.  **Configure sua Chave**:
    Crie um arquivo chamado `.env` e coloque sua chave lá dentro assim:
    ```
    OPENAI_API_KEY=sk-sua-chave-aqui...
    ```

### ▶️ Iniciando a Interface (Recomendado)
Para abrir a janela visual moderna e em Português:
```bash
python gui.py
```

---

## 🛠️ Como este Projeto foi Construído (Guia Educativo)

Aqui explicamos **como** e **por que** adicionamos cada nova funcionalidade recente, de forma que qualquer pessoa possa entender a lógica por trás do código.

### 1. A Interface Visual (`gui.py`)
Inicialmente, o projeto rodava apenas em uma tela preta (terminal). Para torná-lo amigável:
*   **O que usamos**: Uma biblioteca chamada `customtkinter`. Ela permite criar janelas bonitas com botões coloridos e modo escuro, parecidos com apps modernos de celular.
*   **Como funciona**: Criamos uma "caixa" principal (`App`) e dentro dela colocamos "gavetas" (frames). Em uma gaveta fica o histórico da conversa, e na outra ficam os botões de Enviar e Gravar.
*   **O desafio**: Se a IA demorar para responder, a janela travaria. Para resolver isso, usamos **Threading** (fios paralelos). É como contratar um ajudante: enquanto o ajudante vai buscar a resposta da IA, a janela continua livre para você mexer.

### 2. Acessibilidade e Audiodescrição ♿
Queríamos que deficientes visuais pudessem saber o que cada botão faz apenas passando o mouse por cima.
*   **O problema**: O sistema de voz da IA (`gTTS`) depende da internet e é lento. Não serve para respostas rápidas de interface.
*   **A solução**: Usamos uma biblioteca diferente chamada `pyttsx3`. Ela usa a voz robótica que já vem instalada no seu Windows/Linux. Ela é **instantânea** e **não precisa de internet**.
*   **A mágica no código**: Usamos um "evento de hover" (pairar). No código, dissemos: *"Computador, quando o mouse entrar na área deste botão, use o pyttsx3 para falar 'Botão Gravar Áudio' imediatamente"*.

### 3. Leitor de Livros e Documentos (PDF) 📚
Adicionamos a capacidade de você "conversar" com um livro.
*   **O que usamos**: Uma biblioteca chamada `pypdf`. Ela funciona como um "abridor de cartas", tirando o texto de dentro do arquivo PDF.
*   **A lógica**:
    1.  Você clica no botão "📂 Doc" e escolhe um arquivo.
    2.  O sistema lê todo o texto do livro (extração).
    3.  **O segredo**: O sistema pega esse texto e envia para o ChatGPT "escondido" com uma instrução especial: *"Aqui está o conteúdo de um documento. Use-o para responder às perguntas do usuário a partir de agora"*.
    4.  Assim, quando você pergunta "O que o personagem fez?", a IA consulta o texto que acabamos de enviar para ela.

---

## 📂 Estrutura dos Arquivos (Para Desenvolvedores)

*   `gui.py`: **Coração visual**. Contém a janela, os botões e a integração da acessibilidade.
*   `bot.py`: **Cérebro**. Controla a conversa com a OpenAI, a audição (Whisper) e a fala (gTTS).
*   `document_utils.py`: **Bibliotecário**. Funções específicas apenas para abrir arquivos e limpar o texto.
*   `audio_utils.py`: **Técnico de Som**. Grava o microfone e toca os arquivos mp3.
*   `main.py`: Versão antiga (apenas texto/terminal), mantida para testes simples.
