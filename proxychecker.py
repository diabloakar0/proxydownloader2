import requests
import re
import threading
import os
import time
from colorama import Fore

gelen_dosya = "https://akarguard.net/urls.txt"
cikan_dosya = "output.txt"
calisan_proxyler_dosyasi = "calisan_proxyler.txt"  # Changed the variable name

os.system("cls")

adasahillerinde = '''
    ___    __ __ ___    ____  _________    _   ________
   /   |  / //_//   |  / __ \/ ____/   |  / | / / ____/
  / /| | / ,<  / /| | / /_/ / / __/ /| | /  |/ / / __  
 / ___ |/ /| / ___ |/ _, _/ /_/ / ___ |/ /|  / /_/ /  
/_/  |_/_/ |_/_/  |_/_/ |_|\____/_/  |_/_/ |_/\____/   
                                                       
               Proxyler çekiliyor...
'''

print(Fore.YELLOW + adasahillerinde)

def get_proxies(url):
    proxies = []
    try:
        response = requests.get(url, timeout=10)
        pattern = re.compile(r"\d+\.\d+\.\d+\.\d+:\d+")
        proxies = pattern.findall(response.text)
    except:
        print(Fore.RED + f"Error: Proxyler alınamadı {url}")
    return proxies

def save_proxies(proxies, cikan_dosya):
    with open(cikan_dosya, "a") as file:
        file.writelines("\n".join(proxies) + "\n")
    print(Fore.BLUE + f"{len(proxies)} adet proxy buraya keydedildi {cikan_dosya}")
    time.sleep(2)

def check_proxy(proxy, working_proxies):  # Added working_proxies as an argument
    proxy = proxy.strip()
    try:
        response = requests.get("https://www.google.com/", proxies={"http": proxy, "https": proxy}, timeout=10)
        if response.status_code == 200:
            working_proxies.append(proxy)
            print(Fore.GREEN + "[  Calisiyor ]  " + Fore.WHITE + f"{proxy}")
        else:
            print(Fore.LIGHTMAGENTA_EX + "[ Cekilemedi ]  " + Fore.WHITE + f"{proxy}")
    except:
        print(Fore.RED + "[ Calismiyor ]  " + Fore.WHITE + f"{proxy}")

urls = []
try:
    response = requests.get(gelen_dosya, timeout=10)
    urls = response.text.splitlines()
except:
    print(Fore.RED + f"Error: URL listesi alınamadı {gelen_dosya}")

proxies = []
for url in urls:
    proxies += get_proxies(url)

save_proxies(proxies, cikan_dosya)

with open(cikan_dosya, "r") as file:
    proxies = file.readlines()

working_proxies = []  # Renamed to avoid conflict

threads = []
for proxy in proxies:
    thread = threading.Thread(target=check_proxy, args=(proxy, working_proxies))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

with open(calisan_proxyler_dosyasi, "w") as file:
    file.writelines("\n".join(working_proxies))

print(Fore.CYAN + f"PROXYLER KAYDEDILDI {calisan_proxyler_dosyasi}")
