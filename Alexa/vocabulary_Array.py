# -*- coding: utf-8 -*-
import csv
import os
import sys
import codecs

"""
Programm mit der Entsprechenden csv (encoding utf-8) aufrufen, um aus der Tabelle das javascript Array bauen zu lassen.

Nimmt die Tabelle und baut daraus das Array
"""

def rightKey(key):
    return key.split(";")[0]

verben = {}
nomen = {}
adjektive = {}
verbenKeys = []
nomenKeys = []
adjektiveKeys = []
verbenFinished = False
nomenFinished = False

# Hole die verschiedenen Wortarten aus der csv und teile sie auf
with codecs.open(sys.argv[1], encoding="utf-8") as cee:
    smartreader = csv.reader(cee, quotechar='|')
    for row in smartreader:
        key = rightKey(row[0])
        if not (row == ["﻿Verben;"] or row == ['ï»¿Verben;'] or row == ['Verben;']) and (not verbenFinished): # Verben reinpacken
            if row != ['Nomen;']:
                verbenKeys.append(key)
                verben[key] = [row[0].split(";")[1]] # shitty key einmal abhandeln
                for word in row[1:]: # values dazupacken
                    verben[key].append(word.strip())
            else:
                verbenFinished = True
        elif verbenFinished and (not nomenFinished): # Nomen reinpacken
            if row != ['Adjektive;']:
                nomenKeys.append(key)
                nomen[key] = [row[0].split(";")[1]] # shitty key einmal abhandeln
                for word in row[1:]: # values dazupacken
                    nomen[key].append(word.strip())
            else:
                nomenFinished = True
        else: # Adjektive reinpacken
            if (key != '\ufeffVerben'):
                adjektiveKeys.append(key)
                adjektive[key] = [row[0].split(";")[1]] # shitty key einmal abhandeln
                for word in row[1:]: # values dazupacken
                   adjektive[key].append(word.strip())



"""
Durchlaufe die Dictionarys und packe die Values mit den Keys in einem array zusammen
array = [
    ["key1", ["value1","value2"]], Adjektiv
    ["key2", ["value1","value2"]], Nomen
    ["key3", ["value1","value2"]], Verb
    ["key4", ["value1","value2"]] Adjektiv
    ...
]
"""
# Baue das Array aus den verschiedenen Wortarten
file = open("array.txt","a")

file.write("var vocabulary = [ \n\n")
counter = 0
while (counter < len(nomen) or counter < len(verben) or counter < len(adjektive)):
    try:
        key = verbenKeys[counter]
        file.write("[\'"+key+"\', "+str(verben[key]).lower()+"],\n")
    except:
        print("Alle Verben drin")
        pass
    try:
        key = nomenKeys[counter]
        file.write("[\'"+key+"\', "+str(nomen[key]).lower()+"],\n")
    except:
        print("Alle Nomen drin")
        pass
    try:
        key = adjektiveKeys[counter]
        file.write("[\'"+key+"\', "+str(adjektive[key]).lower()+"],\n")
    except:
        print("Alle Adjektive drin")
        pass
    counter +=1
file.write("[\"ende\", [\"\"]]")
print("Fertig!")
file.write("\n];")
print(str(len(nomen))+" Nomen")
print(str(len(adjektive))+" Adjektive")
print(str(len(verben))+" Verben")