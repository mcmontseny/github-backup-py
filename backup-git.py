import requests
import os
import subprocess
from datetime import datetime

print('// ------ BACKUP GITHUB TOOL ------ //')

token = input('Introdueix el token de GitHub >> ')
while len(token)==0:
    token = input('[INPUT] Introdueix el teu token de GitHub >> ')

headers = {'Authorization': f'token {token}'}

print('Intentant connectar amb el compte de GitHub... ')
login = requests.get('https://api.github.com/user', headers=headers)

if login.status_code != 200:
    print(f'[ERROR] {login.json()}')
    print('[END] Execució finalitzada. Problema en connectar amb GitHub...')
    exit()

print('[OK] Connexió realitzada amb èxit.')

print('Intentant recuperar els repositoris...')
repos = requests.get('https://api.github.com/user/repos', headers=headers)

print(f'[OK] Quantitat de repositoris disponibles: {len(repos.json())} repositoris.')

if len(repos.json()) == 0:
    print('[END] Execució finalitzada. No hi ha cap repositori disponible per a descarregar...')
    exit()

print('Intentant crear el directori on es guardarà el backup...')

backup_date = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
path = f'./{backup_date}'

try:
    os.mkdir(path)
except OSError as error:
    print(f'[ERROR] {error}')
    print(f"[ERROR] No s'ha pogut crear el directori: {path}")
    print("[END] Execució finalitzada. No s'ha pogut crear el directori...")
    exit()

print(f"[OK] Directori creat correctament: {path}")

print(f"Començant a descarregar els repositoris a la carpeta: {path}")

try:
    i = 1
    for repo in repos.json():
        print(f'[INFO] ({i}/{len(repos.json())}) - Descarregant repositori {repo["name"]}...')
        subprocess.call(['git', 'clone', '--mirror', repo["ssh_url"]], cwd=path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f'[OK] ({i}/{len(repos.json())}) - Repositori: {repo["name"]} | Autor: {repo["owner"]["login"]} -- Repositori clonat correctament.')
        i += 1
except subprocess.CalledProcessError as error:
    print(f'[ERROR] {error}')
    print("[END] Execució finalitzada. No s'ha pogut clonar algun dels repositoris...")
    exit()

print(f"[END] Execució finalitzada correctament. S'ha guardat els {len(repos.json())} repositoris a {path}")