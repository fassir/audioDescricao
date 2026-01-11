# Como Obter sua Chave da OpenAI (API Key)

Para que o robô funcione, ele precisa de uma "senha" para conversar com os servidores da OpenAI. Siga estes passos:

1.  **Crie uma Conta (se não tiver)**
    *   Acesse: [https://platform.openai.com/signup](https://platform.openai.com/signup)
    *   Faça o cadastro ou login.

2.  **Adicione Créditos (Importante)**
    *   A API da OpenAI é um serviço pago (não é o mesmo que o ChatGPT Plus).
    *   Vá em **Settings (Engrenagem) > Billing**.
    *   Adicione um método de pagamento e coloque um valor mínimo (ex: 5 dólares).
    *   *Nota: Sem créditos, a chave geralmente não funciona ou tem limites muito baixos.*

3.  **Gere a Chave**
    *   Acesse: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
    *   Clique no botão **"Create new secret key"**.
    *   Dê um nome (ex: "ConversaBot").
    *   **COPIE A CHAVE IMEDIATAMENTE**. Você não poderá vê-la novamente. Ela começa com `sk-...`.

4.  **Coloque no Projeto**
    *   Volte para a pasta deste projeto.
    *   Crie um arquivo chamado `.env` (sem nome antes do ponto).
    *   Cole a chave dentro dele assim:
        ```
        OPENAI_API_KEY=sk-sua-chave-gigante-aqui...
        ```
    *   Salve o arquivo.

⚠️ **Segurança**: Nunca compartilhe essa chave com ninguém e não suba o arquivo `.env` para o GitHub (nós já configuramos o `.gitignore` para prevenir isso).
