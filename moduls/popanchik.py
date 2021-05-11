#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random
import re
import time
from moduls.start_hour import startHour
from moduls.read_from_livescore import load_obj

MIN_COEF = 1.40
MAX_COEF = 1.75
MIN_COEF_EXPRESS = 2.5


def returnMatchesForPopanchik(matches, mink=MIN_COEF, maxk=MAX_COEF, hour=startHour()):
    '''выбираются матчи с кефом на фаворита между MIN_COEF и MAX_COEF, начнутся через 2 и более часов, не женских и не юниорских команд.'''
    popanmatches = [] 
    for line in matches:
        if all([(mink <= line["kw1"] <= maxk or mink <= line["kw2"] <= maxk),
                (int(line["time"][0:2]) >= hour),
                not ((re.search(r"(\(Ж\))|(U\d{2})", line["team1"])) or (re.search(r"(\(Ж\))|(U\d{2})", line["team2"]))),
                not (re.search(r"(товар)|(убок)|(рофей)", line["country"]))]):
            popanmatches.append(line)
    return popanmatches


def getPopanPress(minCoefOfExpress, minCoefOfMatch, maxCoefOfMatch):
    popanmatches, day = get_popan_matches_list(minCoefOfMatch, maxCoefOfMatch)
    coef = 1
    usedmatches = []
    press = []
    while coef < minCoefOfExpress:
        if (len(popanmatches) - len(usedmatches) == 0):
            return 
        i = random.randint(0, len(popanmatches) - 1)
        if popanmatches[i] not in usedmatches:
            usedmatches.append(popanmatches[i])
            if popanmatches[i]["kw1"] < popanmatches[i]["kw2"]:
                press.append(f'\
{popanmatches[i]["country"]} \
{popanmatches[i]["time"]} \
{popanmatches[i]["team1"]} - \
{popanmatches[i]["team2"]} П1 кф. \
{popanmatches[i]["kw1"]}')
                coef *= popanmatches[i]["kw1"]
            else:
                press.append(f'\
{popanmatches[i]["country"]} \
{popanmatches[i]["time"]} \
{popanmatches[i]["team1"]} - \
{popanmatches[i]["team2"]} П2 кф. \
{popanmatches[i]["kw2"]}')
                coef *= popanmatches[i]["kw2"]
    
    press.append(f"Итоговый кф {round(coef, 2)}")
    return press


def get_popan_matches_list(minCoefOfMatch, maxCoefOfMatch):
    day = 'today'
    matches_dict = load_obj(day)
    popmatches = returnMatchesForPopanchik(matches_dict, minCoefOfMatch, maxCoefOfMatch)
    popmatches = sorted(popmatches, key=lambda k: k['time']) 
    if len(popmatches) < 3:
        hour = 0
        day = 'tomorrow'
        matches_dict = load_obj(day)
        popmatches = returnMatchesForPopanchik(matches_dict, minCoefOfMatch, maxCoefOfMatch)
        popmatches = sorted(popmatches, key=lambda k: k['time'])
    return popmatches, day


def popan_press_bot(minCoefOfExpress = MIN_COEF_EXPRESS, minCoefOfMatch = MIN_COEF, maxCoefOfMatch = MAX_COEF):
    msg = f'Собираем экспресс с минимальным коэфициентом {minCoefOfExpress}\n\
Матчи с коэфициентами на фаворита от {minCoefOfMatch} до {maxCoefOfMatch} \n\n'
    popmatches, day = get_popan_matches_list(minCoefOfMatch, maxCoefOfMatch)
    if day == 'tomorrow':
        msg += f'На сегодня с матчами туго, давай посмотрим матчи на завтра\n\
Всего "попанских" матчей: {len(popmatches)}\n'
    else: msg += f'Всего "попанских" матчей на сегодня {len(popmatches)}\n'
    if len(popmatches) >= 3:
        press = getPopanPress(minCoefOfExpress, minCoefOfMatch, maxCoefOfMatch)
        if len(press) < 1:
            msg += ('Возможно произошла ошибка при загрузке матчей, она повторяется каждые 10 минут')
        else:
            msg += ("Случчайный пресс от Попанчика:\n\n")
            for i in press:
                msg += (f'{i} \n')
    else: msg = f'На сегодня и завтра с матчами совсем туго. Загляни попозже, может кефы изменятся и я что-то подберу\n\n'
        
    msg += ('\nПоддержка и благодарность:\nhttps://www.tinkoff.ru/sl/76v8PDLRznk\n\n\
И заглядывай к нам в группу в ВК:\nvk.com/probitybets\n\n')

    return msg, press


def popan_list_bot(minCoefOfMatch=MIN_COEF, maxCoefOfMatch=MAX_COEF):
    if minCoefOfMatch >= maxCoefOfMatch:
        raise ValueError('Минимальный коэфициент не может быть больше или равен максимальному')
    elif minCoefOfMatch > 5 or maxCoefOfMatch > 5:
        raise ValueError('Таких коэффициентов на фаворита обычно не бывает')
    popmatches, day = get_popan_matches_list(minCoefOfMatch, maxCoefOfMatch)
    msg = [f'Собираем список матчей с кефами на фаворита от {minCoefOfMatch} до {maxCoefOfMatch} \n\n']
    i = 0
    if day == 'tomorrow':
        msg[i] += f'На сегодня с матчами туго, давай посмотрим матчи на завтра\n\
Всего матчей на завтра: {len(popmatches)}\n'
    else: msg[i] += f'Всего матчей на сегодня: {len(popmatches)}\n\n'
    for ind, match in enumerate(popmatches):
        if match["kw1"] < match["kw2"]:
            msg[i] += (f'{match["time"]} {match["country"]} {match["team1"]} - {match["team2"]} П1 кф. {match["kw1"]} \n\n')
        else:
            msg[i] += (f'{match["time"]} {match["country"]} {match["team1"]} - {match["team2"]} П2 кф. {match["kw2"]} \n\n')
        if len(msg[i]) > 3800:
            i += 1
            msg.append('')
    msg[i] += ('\nПоддержка и благодарность:\nhttps://www.tinkoff.ru/sl/76v8PDLRznk\n\n\
И заглядывай к нам в группу в ВК:\nvk.com/probitybets\n\n')
    return msg


def contest_press_bot():
    if str(time.asctime())[:3] == "Sat":
        msg =  'Сегодня уже суббота. Давай дождемся результатов сегодняшнего конкурса и потом начнем новый.'
        return msg, []
    day = 'contest'
    hour = 0
    matches_dict = load_obj(day)
    popmatches = returnMatchesForPopanchik(matches_dict, hour, MIN_COEF, MAX_COEF)
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

if __name__ == '__main__':
    pass