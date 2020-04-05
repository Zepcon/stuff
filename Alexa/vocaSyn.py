import csv
import os
import sys

"""
Für Bulk Edit in Amazon developer die einzelnen Vokabeln mit Synonymen zusammenbasteln.
CSV muss immer in csv-UTF-8 Format gespeichert sein!
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

with open("smart.csv", newline="") as cee:  # Arrays von oben mit Werten füttern
    smartreader = csv.reader(cee, quotechar='|')
    for row in smartreader:
        key = rightKey(row[0])
        if (not (row == ["﻿Verben;"] or row == ['ï»¿Verben;'] or row == ['Verben;'])): # komisches Zeug was beim lesen passieren kann
            if (not verbenFinished): # Verben reinpacken
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
                adjektiveKeys.append(key)
                adjektive[key] = [row[0].split(";")[1]] # shitty key einmal abhandeln
                for word in row[1:]: # values dazupacken
                   adjektive[key].append(word.strip())


file = open("vocaSyn.txt","a")

builder = ""
temp = ""
print(adjektive)
for i in verbenKeys:
    temp = ""
    for j in verben[i]:
        temp += j + ","
    temp = temp[:-1]
    new = temp.split(",")
    new[0] += ","
    temp = ",".join(new)
    builder += temp + "\n"
for i in nomenKeys:
    temp = ""
    for j in nomen[i]:
        temp += j + ","
    temp = temp[:-1]
    new = temp.split(",")
    new[0] += ","
    temp = ",".join(new)
    builder += temp + "\n"
for i in adjektiveKeys:
    temp = ""
    for j in adjektive[i]:
        temp += j + ","
    temp = temp[:-1]
    new = temp.split(",")
    new[0] += ","
    temp = ",".join(new)
    builder += temp + "\n"

file.write(builder)