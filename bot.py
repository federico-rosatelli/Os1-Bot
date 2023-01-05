import json
import sys
# import time
import random

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


def getNew():
    data = open("q_raw.txt").read()
    datadict = {}
    for i in range(1,103):
        ind = data[data.find(f"{i})"):data.find(f"{i+1})")]

        str = ind[:ind[4:].find("1)")]
        datadict[f"{i}"] = str

    data = open("sol.csv").readlines()
    soldict = {}
    for i in range(len(data)):
        data[i] = data[i].strip()
        spl = data[i].split(",")
        soldict[int(spl[0])] = spl[1]


    dataFull = {}
    for i in datadict:
        dataFull[i] = {
        "str":datadict[i],
        "ans":soldict[int(i)]
        }

    with open("OS1Data.json","w") as wr:
        json.dump(dataFull,wr, indent=4)

def exam():
    with open("OS1Data.json") as rd:
        datadict = json.load(rd)
    chs = ""
    points = 0
    rounds = 0
    quests = [i for i in datadict]
    while chs != "/q" and quests:

        rounds += 1
        r = random.choice(quests)
        if len(sys.argv) == 2:
            r = sys.argv[1]
        print("-"*(len(datadict[r]["str"][:datadict[r]["str"].index("\n")])+2))
        print(datadict[r]["str"])

        chs = input(f"{bcolors.BOLD}[*]> {bcolors.ENDC}")

        if chs == datadict[r]["ans"]:
            print(f"{bcolors.OKGREEN}Corretto!{bcolors.ENDC}")
            points += 1
        else:
            print(f"{bcolors.FAIL}Sbagliato!{bcolors.ENDC}",end="\t")
            print(f"{bcolors.UNDERLINE}Soluzione{bcolors.ENDC}: {bcolors.BOLD}{datadict[r]['ans']} {bcolors.ENDC}")
        quests.remove(r)
        print(f"{bcolors.OKCYAN}Score :{format((points/rounds)*100, '.2f')}%\nRound: {rounds}{bcolors.ENDC}")
        print(f"Errori:{bcolors.WARNING}{rounds-points}{bcolors.ENDC}\n")

def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--get-new":
        getNew()
    else:
        exam()