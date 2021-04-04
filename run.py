#! /usr/bin/python3
# -*- coding: utf-8 -*-

import time
from threading import Thread

from bot import bot
from moduls.read_from_livescore import load_matches


def loader():
    while True:
        try:
            load_matches()
            time.sleep(1000)
        except:
            time.sleep(1)

run_bot = Thread(target=bot)
run_bot.start()
#print('бот стартовал')
run_reader = Thread(target=loader)
run_reader.start()
#print('читалка стартовал')

while True:
    if not run_bot.is_alive():
        #print('бот сломался')
        run_bot.join()
        run_bot = Thread(target=bot)
        run_bot.start()
        #print('бот перезапущен')
    if not run_reader.is_alive():
        #print('читалка сломалась')
        run_reader.join()
        run_reader = Thread(target=loader)
        run_reader.start()
        #print('читалка перезапустилась')

