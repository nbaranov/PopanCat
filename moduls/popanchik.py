#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random
import re
import time
from moduls.start_hour import startHour
from moduls.read_from_livescore import load_obj

MINKF = 1.40
MAXKF = 1.75


def returnMatchesForPopanchik(matches, hour, mink, maxk):
    '''выбираются матчи с кефом на фаворита между MINKF и MAXKF, начнутся через 2 и более часов, не женских и не юниорских команд.'''
    popanmatches = [] 
    for line in matches:
        if all([(mink <= line["kw1"] <= maxk or mink <= line["kw2"] <= maxk),
                (int(line["time"][0:2]) >= hour),
                not ((re.search(r"(\(Ж\))|(U\d{2})", line["team1"])) or (re.search(r"(\(Ж\))|(U\d{2})", line["team2"]))),
                not (re.search(r"(товар)|(убок)|(рофей)", line["country"]))]):
            popanmatches.append(line)
    return popanmatches


def getPopanPress(popanmatches):
    press = []
    coef = 1
    a = 0
    ligth_press = random.randint(2,3)
    if ligth_press > (len(popanmatches) - len(usedmatches)):
        return []

    while a < ligth_press:
        i = random.randint(0, len(popanmatches) - 1)
        if popanmatches[i] not in usedmatches:
            usedmatches.append(popanmatches[i])
            a += 1
            if popanmatches[i]["kw1"] < popanmatches[i]["kw2"]:
                press.append(f'{popanmatches[i]["country"]} {popanmatches[i]["time"]} \
{popanmatches[i]["team1"]} - {popanmatches[i]["team2"]} П1 кф. {popanmatches[i]["kw1"]}')
                coef *= popanmatches[i]["kw1"]
            else:
                press.append(f'{popanmatches[i]["country"]} {popanmatches[i]["time"]} \
{popanmatches[i]["team1"]} - {popanmatches[i]["team2"]} П2 кф. {popanmatches[i]["kw2"]}')
                coef *= popanmatches[i]["kw2"]

    press.append(f"Итоговый кф {round(coef, 2)}")
    usedmatches.clear()
    return press

def get_popan_matches_list():
    hour = startHour()
    day = 'today'
    matches_dict = load_obj(day)
    popmatches = returnMatchesForPopanchik(matches_dict, hour, MINKF, MAXKF)
    #print(popmatches)
    #print(len(popmatches))
    if len(popmatches) < 3:
        hour = 0
        day = 'tomorrow'
        matches_dict = load_obj(day)
        popmatches = returnMatchesForPopanchik(matches_dict, hour, MINKF, MAXKF)
        #print(popmatches)
        #print(len(popmatches))
    return popmatches, day


def popan_press_bot():
    popmatches, day = get_popan_matches_list()
    if day == 'tomorrow':
        msg = f'На сегодня с матчами туго, давай посмотрим матчи на завтра\n\
Всего "попанских" матчей: {len(popmatches)}\n'
    else: msg = f'Всего "попанских" матчей на сегодня {len(popmatches)}\n'
    if len(popmatches) >= 3:
        press = getPopanPress(popmatches)
        if len(press) < 1:
            msg += ('Возможно произошла ошибка при загрузке матчей, она повторяется каждые 10 минут')
        else:
            msg += ("Случчайный пресс от Попанчика:\n\n")
            for i in press:
                msg += (f'{i} \n')
    else: msg = f'На сегодня и завтра с матчами совсем туго. Загляни попозже, может кефы изменятся и я что-то подберу\n\n'
        
    msg += ('\nПоддержка и благодарность:\nhttps://vk.com/app6887721_-93234960\n\n\
И заглядывай к нам в группу в ВК:\nvk.com/probitybets\n\n')

    return msg, press


def popan_list_bot():
    popmatches, day = get_popan_matches_list()
    if day == 'tomorrow':
        msg = f'На сегодня с матчами туго, давай посмотрим матчи на завтра\n\
Всего "попанских" матчей на завтра: {len(popmatches)}\n'
    else: msg = f'Всего "попанских" матчей на сегодня: {len(popmatches)}\n\n'
    for ind, match in enumerate(popmatches):
        if match["kw1"] < match["kw2"]:
            msg += (f'{ind+1}. {match["country"]} {match["time"]} {match["team1"]} - {match["team2"]} П1 кф. {match["kw1"]} \n\n')
        else:
            msg += (f'{ind+1}. {match["country"]} {match["time"]} {match["team1"]} - {match["team2"]} П2 кф. {match["kw2"]} \n\n')
    msg += ('\nПоддержка и благодарность:\nhttps://vk.com/app6887721_-93234960\n\n\
И заглядывай к нам в группу в ВК:\nvk.com/probitybets\n\n')
    return msg


def contest_press_bot():
    if str(time.asctime())[:3] == "Sat":
        msg =  'Сегодня уже суббота. Давай дождемся результатов сегодняшнего конкурса и потом начнем новый.'
        return msg, []
    day = 'contest'
    hour = 0
    matches_dict = load_obj(day)
    popmatches = returnMatchesForPopanchik(matches_dict, hour, MINKF, MAXKF)
    msg = f'Всего "попанских" матчей на конкурс: {len(popmatches)}\n\n'
    if len(popmatches) >= 3:
        press = getPopanPress(popmatches)
        if len(press) < 1:
            msg += ('Возможно произошла ошибка при загрузке матчей, она повторяется каждые 10 минут')
        else:
            msg += ("Пресс для конкурса:\n\n")
            for i in press:
                msg += (f'{i} \n')
    else: msg = f'Сейчас с матчами совсем туго. Загляни попозже, может кефы изменятся и я что-то подберу\n\n'
        
    msg += ('\nНе забудь написать пресс в комментарии в группе:\nhttps://vk.com/probitybets\n\n')

    return msg, press


amt_preses = 1
usedmatches = []
