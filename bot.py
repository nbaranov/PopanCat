#! /usr/bin/python3
# -*- coding: utf-8 -*-

MINKF = 1.40
MAXKF = 1.75

import random
from time import asctime 

from telebot import TeleBot
from moduls.secret import TOKEN
from moduls.popanchik import popanchik
from moduls.popanchik import returnMatchesForPopanchik
from moduls.read_from_livescore import load_obj
from moduls.start_hour import startHour

def log(msg):
    with open('history.log', 'a', encoding='UTF-8') as file:
        file.write(msg)

def bot():
    bot = TeleBot(token())
    #Ответ на команды /start и /help
    @bot.message_handler(commands=['start', 'help'])
    def handle_start_help(message):
        bot.reply_to(message, f'Привет {message.chat.first_name}\nЯ Пробити Кот и я могу дать тебе попанский пресс или список всех попанских матчей на сегодня\
    для этого  напиши команду /press или /matches.')

    # Обрабатывается голосовые сообщения
    @bot.message_handler(content_types=['voice'])
    def handle_voice(message):
        bot.reply_to(message, f'У тебя очень красивый голос, {message.chat.first_name}, но я не могу распозновать голосовые сообщения')

    #Обработка картиночек
    @bot.message_handler(content_types=['photo'])
    def handle_photos(message):
        answers = ['Nice meme xD', 'Ха ору :D', ')))', 'Давай еще :D']
        bot.reply_to(message, f'{random.choice(answers)}')


    @bot.message_handler(commands=['press'])
    def handle_start_help(message):
        hour, day = startHour()
        matches_dict = load_obj(day)
        popmatches = returnMatchesForPopanchik(matches_dict, hour, MINKF, MAXKF)
        if day == 'tomorrow':
            msg = f'На сегодня с матчами туго, давай посмотрим матчи на завтра\n\
Всего "попанских" матчей: {len(popmatches)}\n'
        else:
            msg = f'Всего "попанских" матчей на сегодня {len(popmatches)}\n'
        popanpress = popanchik(popmatches)
        if message.chat.username is None:
            name = f'name {message.chat.first_name} {message.chat.last_name}'
        else:
            name = f'username {message.chat.username}'    
        if len(popanpress) < 1:
            msg += ('Возможно произошла ошибка при загрузке матчей, она повторяется каждые 10 минут')
        elif len(popanpress) > 1:
            msg += ("Прессы от Попанчика:\n")
            count = 0
            for press in popanpress:
                count += 1
                msg += (f"\nПресс {count}.\n")
                for i in press:
                    msg += (f'{i} \n')
        else:
            msg += ("Пресс от Попанчика:\n\n")
            for press in popanpress:
                for i in press:
                    msg += (f'{i} \n')
        msg += ('\nПоддержка и благодарность:\nhttps://vk.com/app6887721_-93234960\n\n\
И заглядывай к нам в группу в ВК:\nvk.com/probitybets\n\n')

        bot.reply_to(message, msg)
        log(f'{asctime()} {name} спросил пресс\n')
        msg = str()
        for line in popanpress[0]:
            msg += line + '\n'
        log(msg + "\n")

    @bot.message_handler(commands=['matches'])
    def handle_start_help(message):
        hour, day = startHour()
        matches_dict = load_obj(day)
        popmatches = returnMatchesForPopanchik(matches_dict, hour, MINKF, MAXKF)
        if day == 'tomorrow':
            msg = (f'Все "попанcкие" матчи на завтра. \nВсего их {len(popmatches)}, выбирай любой и грузи хату!\n\n')
        else:
            msg = (f'Все "попанcкие" матчи на сегодня. Всего их {len(popmatches)}, выбирай любой и грузи хату!\n\n')
        if message.chat.username is None:
            name = f'name {message.chat.first_name} {message.chat.last_name}'
        else:
            name = f'username {message.chat.username}'
        for ind, match in enumerate(popmatches):
            if match["kw1"] < match["kw2"]:
                msg += (f'{ind+1}. {match["country"]} {match["time"]} {match["team1"]} - {match["team2"]} П1 кф. {match["kw1"]} \n\n')
            else:
                msg += (f'{ind+1}. {match["country"]} {match["time"]} {match["team1"]} - {match["team2"]} П2 кф. {match["kw2"]} \n\n')
        msg += ('\nПоддержка и благодарность:\nhttps://vk.com/app6887721_-93234960\n\n\
    И заглядывай к нам в группу в ВК:\nvk.com/probitybets\n\n')

        bot.reply_to(message, msg)
        log(f'{asctime()} {name} спросил список матчей\n')


    bot.polling(none_stop=True)
