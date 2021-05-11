#! /usr/bin/python3
# -*- coding: utf-8 -*-


import random
import os


from time import asctime
from typing import Text 
from telebot import TeleBot
from moduls.popanchik import popan_press_bot
from moduls.popanchik import popan_list_bot


COMMANDS_EXPRESS = 'экспресс *минимальный коэфициент экспресса* *миннимальный коэффициент матча* *максимальный коэффициент матча*\n\
экспресс *минимальный коэфициент экспресса*\
или просто слово "экспресс" для попанского экспресса\n\n'
COMMANDS_MATCHES = 'матчи *миннимальный коэффициент матча* *максимальный коэффициент матча* - чтобы получить список всех попанский матчей\n\
или просто слово "матчи" для списка матчей с коэфициентами по умолчанию'
TOKEN = os.getenv('TOKEN')


def log(file, msg):
    with open(file, 'a', encoding='UTF-8') as file:
        file.write(msg)


def get_name(message):
    if message.chat.username is None:
        name = f'name {message.chat.first_name} {message.chat.last_name}'
    else:
        name = f'username {message.chat.username}'
    return name


def bot():
    bot = TeleBot(TOKEN)
    #Ответ на команды /start и /help
    @bot.message_handler(commands=['start', 'help'])
    def handle_start_help(message):
        bot.reply_to(message, f'Привет {message.chat.first_name}\nЯ Пробити Кот и я могу дать тебе попанский пресс или список всех попанских матчей на сегодня\
для этого  напиши команду:{COMMANDS_EXPRESS}{COMMANDS_MATCHES}')

    # Обрабатывается голосовые сообщения
    @bot.message_handler(content_types=['voice'])
    def handle_voice(message):
        bot.reply_to(message, f'У тебя очень красивый голос, {message.chat.first_name}, но я не могу распозновать голосовые сообщения')

    #Обработка картиночек
    @bot.message_handler(content_types=['photo'])
    def handle_photos(message):
        answers = ['Ха ору :D', ')))', 'Давай еще :D']
        bot.reply_to(message, f'{random.choice(answers)}')


    @bot.message_handler(func=lambda message: 'прес' in message.text.lower(), content_types=['text'])
    def popan_press(message):
        name = get_name(message)
        log('history.log', f'{asctime()} {name} спросил экспресс - {message.text}\n')     
        try:
            if (len(message.text.split()) == 4): # 4 arguments command, minCoefOfExpress, minCoefOfMatch, maxCoefOfMatch 
                minCoefOfExpress = float(message.text.split()[1].replace(',', '.'))
                minCoefOfMatch = float(message.text.split()[2].replace(',', '.'))
                maxCoefOfMatch = float(message.text.split()[3].replace(',', '.'))
                msg, press = popan_press_bot(minCoefOfExpress, minCoefOfMatch, maxCoefOfMatch)
            elif (len(message.text.split()) == 2): # 2 arguments command and minCoefOfExpress
                    minCoefOfExpress = float(message.text.split()[1].replace(',', '.'))
                    msg, press = popan_press_bot(minCoefOfExpress)
            elif (len(message.text.split()) == 1):
                msg, press = popan_press_bot()
            else:
                raise ValueError('Ошибка в количестве аргументов')
        except ValueError as error_msg:
            msg = f"{error_msg}\n\nВведите команду в формате:\n{COMMANDS_EXPRESS}"
            press = [f"Не удалось собрать экспресс по заданным параметрам {error_msg}"]
        finally:
            bot.reply_to(message, msg)
        
        
        log('history.log', f'{asctime()} пресс отправлен\n')
        logMsg = str()
        for line in press:
            logMsg += line + '\n'
        log('history.log', logMsg + "\n")
        
            


    # @bot.message_handler(commands=['contest'])
    # def contest_press(message):
    #     name = get_name(message)
    #     log('contest.log', f'{asctime()} {name} спросил КОНКУРСНЫЙ пресс\n')
    #     msg, press = contest_press_bot()
    #     bot.reply_to(message, msg)

    #     log('contest.log', f'{asctime()} пресс выдан\n')
    #     msg = str()
    #     for line in press:
    #         msg += line + '\n'
    #     log('contest.log', msg + "\n")



    @bot.message_handler(func=lambda message: 'матчи' in message.text.lower(), content_types=['text'])
    def matches_list(message):
        name = get_name(message)
        log('history.log', f'{asctime()} {name} спросил список матчей\n')
        try:
            if len(message.text.split()) == 3: # 3 arguments command, minCoefOfMatch, maxCoefOfMatch
                minCoefOfMatch = float(message.text.split()[1].replace(',', '.'))
                maxCoefOfMatch = float(message.text.split()[2].replace(',', '.'))
                msg = popan_list_bot(minCoefOfMatch, maxCoefOfMatch)
            elif len(message.text.split()) < 3:
                msg = popan_list_bot()
        except ValueError as error_msg:
            msg = [f'Не удалось собрать матчи по данным параметрам\n{error_msg}\n\n{COMMANDS_MATCHES}']
            
        if len(msg) == 1:
            bot.reply_to(message, msg[0])
        else:
            for i in range(len(msg)):
                part = f'Часть {i+1} из {len(msg)}\n' + msg[i]
                bot.reply_to(message, part)
        name = get_name(message)
        log('history.log', f'{asctime()} список для {name} выдан\n')


    # Обрабатывается текстовые  сообщения
    @bot.message_handler(content_types=['text'])
    def handle_text(message):
        bot.reply_to(message, f'Извини, {message.chat.first_name}, но я пока не могу свободно общаться.\n\
Чтобы получить прогнозы или список матчей нужно вводить команды:\n\
{COMMANDS_EXPRESS}{COMMANDS_MATCHES}')

        name = get_name(message)
        log('history.log', f'{asctime()} {name} написал:\n {message.text}\n\n')



    bot.polling()
