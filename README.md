# Ferramenta Termux - [screm1x_menu]

Este projeto contém uma coleção de ferramentas úteis que podem ser executadas diretamente no Termux. São funções que permitem realizar atividades como busca de usuários nas redes sociais, análise de metadados EXIF de imagens e envio de e-mails em massa.

## Funcionalidades

### 1. **Bomber Email**
   - Envia uma quantidade especificada de e-mails para um destinatário.
   - Permite configurar o assunto e a mensagem.
   - Requer um e-mail do Gmail e a senha de um aplicativo para login (não a senha da sua conta Google).

### 2. **EXIF Tool**
   - Extrai metadados EXIF de imagens.
   - Inclui a extração de coordenadas GPS se estiverem disponíveis nos metadados da imagem.

### 3. **Sherlock**
   - Pesquisa um nome de usuário nas principais redes sociais e retorna os links encontrados.

## Requisitos

Certifique-se de que o `requirements.txt` seja instalado corretamente para que o programa funcione sem erros. Execute o seguinte comando no Termux para instalar as dependências:

```bash
pkg install libjpeg-turbo
git clone https://github.com/screm1x666yf/screm1x_menu.git
cd screm1x_menu
python3 consultas.py

