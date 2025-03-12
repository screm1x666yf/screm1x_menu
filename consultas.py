import os
import sys
import subprocess

required_packages = ["requests", "beautifulsoup4", "pillow"]

for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"Instalando {package}...")
        subprocess.run([sys.executable, "-m", "pip", "install", package])

print("Todas as dependências foram verificadas e instaladas.")

import requests
from bs4 import BeautifulSoup
import smtplib
import time
from PIL import Image, ExifTags
from fractions import Fraction
import re

class Painel:
    @staticmethod
    def menu():
        print("[1] Bomber email\n[2] EXIF tool\n[3] Sherlock")
        print()
        return int(input("<< [@xy1thal] >> "))
    
    @staticmethod
    def solicitar_dados():
        raise NotImplementedError("Este método deve ser sobrescrito pelas subclasses")

class BuscarUsuario:
    social_networks = [
        "instagram.com", 
        "twitter.com", 
        "linkedin.com", 
        "facebook.com",
        "youtube.com",
        "tiktok.com",
        "kwai.com",
        "pinterest.com",
        "twitch.com",
        "github.com",
        "snapchat.com",
        "OnlyFans.com",
        "Reddit.com",
        "Truth Social.com",
        "Yubo.com",
        "Threads.com",
        "Rumble.com",
        "VK.com",
        "Gitlab.com",
        "BitBucket.com",
        "Codewars.com",
        "Discogs.com",
        "Replit.com",
        "Myspace.com",
        "Keybase.com"
    ]

    def search_in_google(self, query: str, network: str) -> str:
        try:
            url = f"https://www.google.com/search?q={query}+site:{network}"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                return response.text
            else:
                print(f"[ERRO] Status Code {response.status_code} ao acessar o Google para {network}.")
                return ""
        except requests.exceptions.Timeout:
            print(f"[ERRO] Timeout ao acessar {network}. Tente novamente.")
            return ""
        except requests.exceptions.RequestException as e:
            print(f"[ERRO] Erro de requisição para {network}: {e}")
            return ""
        except Exception as e:
            print(f"[ERRO] Erro desconhecido ao acessar {network}: {e}")
            return ""

    def extract_links(self, html: str, network: str) -> None:
        if not html:
            print(f"[ERRO] Nenhum conteúdo HTML encontrado para {network}.")
            return

        try:
            soup = BeautifulSoup(html, "html.parser")
            found = False

            for link in soup.find_all("a", href=True):
                href = link["href"]
                if network in href:
                    print(f"[+] Link encontrado: {href}")
                    found = True

            if not found:
                print(f"[-] Nenhum link encontrado para {network}.")
        except Exception as e:
            print(f"[ERRO] Erro ao processar o HTML para {network}: {e}")

    def buscar_nome(self, query: str) -> None:
        if not query or query.strip() == "":
            print("[ERRO] A busca não pode ser vazia. Por favor, insira um nome ou username válido.")
            return

        for network in self.social_networks:
            print(f"Buscando {query} no {network}...")
            html = self.search_in_google(query, network)
            if html:
                self.extract_links(html, network)
            time.sleep(1)

    @staticmethod
    def solicitar_dados() -> str:
        return input("Digite o nome ou username a ser buscado: ").strip()

class MetaDados(Painel):
    def __init__(self, imagem):
        self.imagem = imagem

    def extrair_gps(self, gps_info):
        """Extrai e formata as coordenadas GPS"""
        try:
            if gps_info:
                # Latitude (chave 2) e Longitude (chave 4)
                latitude = gps_info.get(2)
                longitude = gps_info.get(4)

                if latitude and longitude:
                    # Função para converter IFDRational para float
                    def ifd_rational_to_float(value):
                        if isinstance(value, tuple):
                            num, denom = value
                            return float(Fraction(num, denom))
                        return float(value)

                    # Convertendo para float os valores de Latitude e Longitude
                    lat_deg, lat_min, lat_sec = latitude
                    lon_deg, lon_min, lon_sec = longitude

                    # Convertendo os valores de GPS de IFDRational para float
                    lat_deg = ifd_rational_to_float(lat_deg)
                    lat_min = ifd_rational_to_float(lat_min)
                    lat_sec = ifd_rational_to_float(lat_sec)
                    lon_deg = ifd_rational_to_float(lon_deg)
                    lon_min = ifd_rational_to_float(lon_min)
                    lon_sec = ifd_rational_to_float(lon_sec)

                    # Formatação final das coordenadas GPS
                    latitude_formatada = f"{lat_deg}° {lat_min}' {lat_sec:.6f}\" {'N' if gps_info.get(1) == 'N' else 'S'}"
                    longitude_formatada = f"{lon_deg}° {lon_min}' {lon_sec:.6f}\" {'E' if gps_info.get(3) == 'E' else 'W'}"

                    return f"Latitude: {latitude_formatada}, Longitude: {longitude_formatada}"

            return "GPS não disponível ou inválido."

        except Exception as e:
            print(f"Erro ao processar GPS: {e}")
            return "Erro ao processar GPS."

    def meta_dados(self):
        try:
            imagem = Image.open(self.imagem)
            exift_data = imagem._getexif()

            if exift_data is not None:
                exift = {ExifTags.TAGS[chave]: valor for chave, valor in exift_data.items() if chave in ExifTags.TAGS}

                for chave, valor in exift.items():
                    print(f"{chave}: {valor}")
                
                # Chama a função de extrair e formatar GPS
                gps_info = exift.get('GPSInfo')
                if gps_info:
                    gps_formatado = self.extrair_gps(gps_info)
                    print(gps_formatado)

            else:
                print("Essa imagem não possui metadados EXIF.")
        except FileNotFoundError:
            print(f"Erro: O arquivo {self.imagem} não foi encontrado.")
        except IsADirectoryError:
            print(f"Erro: '{self.imagem}'é um diretório, não um arquivo de imagem.")
        except OSError:
            print(f"Erro: O formato da imagem {self.imagem} não é suportado ou está corrompido.")
        except Exception as e:
            print(f"Erro inesperado ao acessar os metadados EXIF: {e}")

    @staticmethod
    def solicitar_dados():
        return input("Caminho da imagem: ")

class SpamEmail(Painel):
    def __init__(self, email, senha):
        self.email = email
        self.senha = senha

    @staticmethod
    def validar_email(email: str) -> bool:
        padrao_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.fullmatch(padrao_email, email):
            return True
        else:
            return False

    def spam_email(self, alvo, mensagem="Você está morto", assunto="Morte"):
        try:
            if not self.validar_email(self.email):
                print(f"[ERRO] O e-mail {self.email} é inválido.")
                return

            if not self.validar_email(alvo):
                print(f"[ERRO] O e-mail de destino {alvo} é inválido.")
                return

            with smtplib.SMTP("smtp.gmail.com", 587) as smtpserver:
                smtpserver.ehlo()
                smtpserver.starttls()
                smtpserver.login(self.email, self.senha)
                texto = f"Subject: {assunto}\n\n{mensagem}"

                for qtd in range(500):
                    smtpserver.sendmail(self.email, alvo, texto)
                    print(f"[+] Enviado {qtd + 1} e-mails")
                    if qtd >= 6:
                        time.sleep(2)
        except smtplib.SMTPAuthenticationError:
            print("Erro: Falha na autenticação do e-mail. Verifique seu e-mail e senha.")
        except smtplib.SMTPException as e:
            print(f"Erro no envio de e-mails: {e}")
        except Exception as e:
            print(f"Erro inesperado ao enviar e-mails: {e}")

    @staticmethod
    def solicitar_dados():
        email = input("Seu e-mail: ").strip()
        senha = input("Senha do app: ")
        return email, senha
def main():
    while True:
        try:
            opcao = Painel.menu()
            if opcao == 1:
                email, senha = SpamEmail.solicitar_dados()
                spam = SpamEmail(email, senha)
                alvo = input("Alvo: ").strip()
                mensagem = input("Mensagem (opcional): ").strip()
                assunto = input("Assunto (opcional): ").strip()
                spam.spam_email(alvo, mensagem, assunto)
            elif opcao == 2:
                imagem = MetaDados.solicitar_dados()
                MetaDados(imagem).meta_dados()
            elif opcao == 3:
                usuario = BuscarUsuario.solicitar_dados()
                BuscarUsuario().buscar_nome(usuario)
            elif opcao==4:
                pass
            else:
                print("Opção inválida!")
        except (ValueError, TypeError):
            print("Erro: Insira um número válido para a opção.")
        except Exception as e:
            print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    main()
