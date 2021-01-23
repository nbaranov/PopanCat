#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random
import re
from moduls.ends import ends


def returnMatchesForRandomchik(matches, hour):
	randomMathches = []
	minkf = 2
	for match in matches:
		if (match["kw1"] > minkf) and (match["kw2"] > minkf) and int(match["time"][0:2]) >= hour:
			randomMathches.append(match)
	print(f'''Найден{ends(len(randomMathches), "", "о", "о")} \
{len(randomMathches)} матч{ends(len(randomMathches), "", "а", "ей")} для Рандомчика''')
	return randomMathches


def randomchik(matches, hour):
	randomMathches = []
	matches = returnMatchesForRandomchik(matches, hour)

	if len(matches) < 2:
		print("У рандомчика матчей нет")
		return  randomMathches
	elif len(matches) > 5:
		count = random.randint(2,3)
	else:
		count = random.randint(2,len(matches))

	for _ in range(count): 
		i = random.randint(0, len(matches)-1)
		chanceW1 = int (100 / matches[i]["kw1"])
		chanceX = int (100 / matches[i]["kx"])
		chanceW2 = int (100 / matches[i]["kw2"])
		fullChance = chanceW1 + chanceX + chanceW2
		stavka = random.randint(50,100)
		result = random.randint(0, fullChance)
		if result <= chanceW1:
			randomMathches.append(f'{matches[i]["country"]} {matches[i]["time"]} {matches[i]["team1"]} - {matches[i]["team2"]}\tПобеда1\tсумма\t{stavka}\tкф.\t{matches[i]["kw1"]}') 
		elif result <= chanceW1 + chanceX:
			randomMathches.append(f'{matches[i]["country"]} {matches[i]["time"]} {matches[i]["team1"]} - {matches[i]["team2"]}\tНичья\tсумма\t{stavka}\tкф.\t{matches[i]["kx"]}')
		else:
			randomMathches.append(f'{matches[i]["country"]} {matches[i]["time"]} {matches[i]["team1"]} - {matches[i]["team2"]}\t Победа2\tсумма\t{stavka}\tкф.\t{matches[i]["kw2"]}')
		matches.pop(i)
	return randomMathches
