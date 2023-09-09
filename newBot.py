import sys
import requests
import random
import os
import time
import urllib.request
from PIL import Image

URL = "https://raw.githubusercontent.com/appinfosapienza/so-un-bot/main/Domande%20SO1.txt"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def download(url:str,filename:str):
    try:
        res = requests.get(url)
        response = res.text
    except Exception as e:
        raise Exception(f"{bcolors.FAIL}Impossibile connettersi a {url}\n{e}\n\n{bcolors.ENDC}")
    return response


def parse(questions):
    qu = []
    ins = {
        "q":"",
        "a":[],
        "r":0
    }
    quest = True
    i = 0
    while i < len(questions):
        if quest and (not questions[i][:2] == "v " and not questions[i][:2] == "> "):
            ins["q"] += questions[i]
        if questions[i][:2] == "v ":
            quest = False
            ins["r"] = len(ins["a"])
            ins["a"].append(questions[i][2:])
        if questions[i][:2] == "> ":
            quest = False
            ins["a"].append(questions[i][2:])
        if questions[i] == "\n":
            qu.append(ins)
            ins = {
                "q":"",
                "a":[],
                "r":0
            }
            quest = True
        i += 1
    return qu

def saveFile(filename,data):
    with open(filename,"w") as wr:
        wr.write(data)


def showImage(que:str):
    u = que.find("%")
    url = que[4:u]
  
    urllib.request.urlretrieve(
    url,
    "tmp.png")
    
    img = Image.open("tmp.png")
    img.show()


def test(domande):
    rounds = 0
    points = 0
    while domande:
        rounds += 1
        chs = random.randint(0,len(domande)-1)
        if domande[chs]["q"] == "":
            continue
        # DOMANDA
        # img=https://i.imgur.com/
        if domande[chs]["q"][:24] == "img=https://i.imgur.com/" and len(sys.argv)>1 and sys.argv[1] == "img":
            showImage(domande[chs]["q"])
        print(domande[chs]["q"])
        # RISPOSTE
        for i in range(len(domande[chs]["a"])):
            print(f"{i+1}) {domande[chs]['a'][i].strip()}")
        
        # Prova
        inp = int(input(f"\n{bcolors.BOLD}[*]> {bcolors.ENDC}"))
        if inp == domande[chs]["r"]+1:
            print(f"{bcolors.OKGREEN}Corretto!{bcolors.ENDC}")
            points += 1
        else:
            print(f"{bcolors.FAIL}Sbagliato!{bcolors.ENDC}",end="\t")
            print(f"{bcolors.UNDERLINE}Soluzione{bcolors.ENDC}: {bcolors.BOLD}{domande[chs]['r']+1} {bcolors.ENDC}")
        domande.pop(chs)
        print(f"{bcolors.OKCYAN}Score: {format((points/rounds)*100, '.2f')}%\nRound: {rounds}{bcolors.ENDC}")
        print(f"Punti: {bcolors.WARNING}{points}{bcolors.ENDC}\n")
        

        


def main():
    filename = URL.split("/")[-1]
    try:
        if os.path.isfile(filename):
            timeFile = os.path.getmtime(filename)
            if time.time() - timeFile < 60*60*24:
                raise Exception(f"{bcolors.FAIL}Already downloaded\n{bcolors.ENDC}")
        res = download(URL,filename)
        saveFile(filename,res)
    except Exception as e:
        print(e)
        if not os.path.isfile(filename):
            return
    
    op = open(filename).readlines()
    domande = parse(op)
    test(domande)

main()
    


