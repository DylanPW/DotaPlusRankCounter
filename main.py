#Created by DylanPW 2018

import requests
import json
import operator
from operator import attrgetter 

#list of heroes in the game and a counter for conveniences sake
heroList = []
heroCount = 0


#class containing the hero
class Hero:
    def __init__(self, heroid, heroName):
        self.heroName = heroName
        self.heroid = heroid

    def add(self, playerCount):
        self.playerCount = playerCount

#function that gets the list of heroes
def getHeroes():
    print("Gathering list of heroes... ", end = '')
    r = requests.get("https://api.stratz.com/api/v1/Hero")
    r_json=json.loads(r.text)    
    for key, value in r_json.items():
        heroList.append(Hero(str(r_json[key]['id']), str(r_json[key]['displayName'])))
    global heroCount
    heroCount = len(heroList)
    print("Done!")
        
#function that gets the number of master tier players for a given hero ID
def getDotaPlusRanks(id):
    for i in range (0, len(heroList)):
        if heroList[i].heroid == id:
            index = i
            break
    
    print("Finding number for " + heroList[index].heroName + " (Hero " + str(index + 1) + " of " + str(heroCount) + ")... ", end = '')
    count = 0
    master = True
    currentCount = 0
    # repeatedly calls the API with incrementing values to skip as a maximum of 100 results can be retrieved at a time from the API.
    while master == True:
        r = requests.get("https://api.stratz.com/api/v1/Player/dotaPlusLeaderboard?heroId={0}&orderBy=level&take=100&skip={1}".format(id, currentCount))
        r_json=json.loads(r.text)
        r_len = len(r_json['players'])
        for i in range (0, r_len):
            if int(r_json['players'][i]['level']) == 25:
                count += 1
            elif int(r_json['players'][i]['level'] != 25):
                master = False
                break

        currentCount += 100

    for i in range (0, len(heroList)):
        if heroList[i].heroid == id:
            heroList[i].playerCount = count
            
    print("Done!")

#main function, gets the list of heroes, then the number of master tier players and outputs it in alphabetical order
def getAllHeroes():
    getHeroes()
    for i in range (0, len(heroList)):
        getDotaPlusRanks(heroList[i].heroid)
    heroList.sort(key=attrgetter('heroName'))

    print("\n\n{:20}\t{:25}".format("Hero:", "Number of Master Tiers:\n"))
    for i in range (0, len(heroList)):
        print("{:20}\t{:4}".format(str(heroList[i].heroName), str(heroList[i].playerCount)))    


getAllHeroes()
