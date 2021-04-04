#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pickle
import time
import requests
import re
import sys
import os


from bs4 import BeautifulSoup as bs

def save_obj(obj, name):
    try:
        with open('matches_obj/' + name + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
    except:
        time.sleep(0.1)
        save_obj(obj, name)


def load_obj(name):
    try:
        with open('matches_obj/' + name + '.pkl', 'rb') as f:
            return pickle.load(f)
    except:
        time.sleep(0.1)
        load_obj(name)



def load_matches():
 
    while True:
        try:
            today = requests.get('http://m.flashscore.ru/?s=5')
            today = today.text.replace('<br />', '\n')
            save_obj(html_to_dict(today), 'today')
            
            tomorrow = requests.get('http://m.flashscore.ru/?d=1&s=5')
            tomorrow = tomorrow.text.replace('<br />', '\n')
            save_obj(html_to_dict(tomorrow), 'tomorrow')
            
            break            
        except:
            continue


def html_to_dict(html):
    try:
        # with open('livescore.html', 'r', encoding="utf-8") as doc:
        #     html = doc.read()
        matches = []
        table = bs(html, 'html.parser').find('div', attrs={'id' : 'score-data'}).text.split('\n')
        table[0] = table[0].split('!')[1]
        
        for row in table:
            if (re.match('[А-ЯЁ]{3}', row)) and ('-:-' in row) and ('Перенесен' not in row):
                row = re.split("(\d{2}:\d{2})|(d+')", row)
                country = row[0]
                if ("-:-" in row[3]) and ('[' in row[3]) and (']' in row[3]):
                    time = row[1]
                    teams = row[3].split('-:-')[0].strip().split(' - ')
                    team1, team2 = teams[0], teams[1]
                    kf = row[3].split('[')[-1][:-1].split('|')
                    matches.append({
                        "country": country,
                        "time": time,
                        "team1": team1,
                        "team2": team2,
                        "kw1": float(kf[0].strip()),
                        "kx": float(kf[1].strip()),
                        "kw2": float(kf[2].strip())
                        })
            elif ("-:-" in row) and ('[' in row) and (']' in row) and ('Перенесен' not in row):
                time = row[:5]
                teams = row.split('-:-')[0][5:].strip().split(' - ')
                team1, team2 = teams[0], teams[1]
                kf = row.split('[')[-1][:-1].split('|')
                matches.append({
                    "country": country,
                    "time": time,
                    "team1": team1,
                    "team2": team2,
                    "kw1": float(kf[0].strip()),
                    "kx": float(kf[1].strip()),
                    "kw2": float(kf[2].strip())
                    })
        return matches
    except:
        time.sleep(0.1)
        #print("не удалось записать")
        return html_to_dict(html) 

if __name__ == '__main__':
    load_matches()
    matches = load_obj('today')
    print('today \n\n', matches)
    matches = load_obj('tomorrow')
    print('tomorrow \n\n',matches)
    