#! /usr/bin/python3
# -*- coding: utf-8 -*-



import random
from time import asctime 

from telebot import TeleBot
from moduls.secret import TOKEN
from moduls.popanchik import popan_press_bot
from moduls.popanchik import popan_list_bot
from moduls.popanchik import contest_press_bot
from moduls.popanchik import returnMatchesForPopanchik
from moduls.start_hour import startHour

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
для этого  напиши команду /press или /matches.\n\
Для участия в конкурсе напиши команду /contest')

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
    def popan_press(message):
        
        msg, press = popan_press_bot()
        bot.reply_to(message, msg)

        name = get_name(message)

        log('history.log', f'{asctime()} {name} спросил пресс\n')
        msg = str()
        for line in press:
            msg += line + '\n'
        log('history.log', msg + "\n")


    @bot.message_handler(commands=['contest'])
    def contest_press(message):

        msg, press = contest_press_bot()
        bot.reply_to(message, msg)

        name = get_name(message)

        log('contest.log', f'{asctime()} {name} спросил КОНКУРСНЫЙ пресс\n')
        msg = str()
        for line in press:
            msg += line + '\n'
        log('contest.log', msg + "\n")



    @bot.message_handler(commands=['matches'])
    def matches_list(message):

        msg = popan_list_bot()
        bot.reply_to(message, msg)

        name = get_name(message)
        log('history.log', f'{asctime()} {name} спросил список матчей\n')

    # Обрабатывается текстовые  сообщения
    @bot.message_handler(content_types=['text'])
    def handle_voice(message):
        bot.reply_to(message, f'Извини, {message.chat.first_name}, но я пока не могу свободно общаться.\n\
Чтобы получить прогнозы или список матчей нужно вводить команды:\n\
/press - чтобы получить случайный попанский экспресс\n\n\
/matches - чтобы получить список всех попанский матчей\n\n\
/contest - чтобы получить экспресс для конкурса')

        name = get_name(message)
        log('history.log', f'{asctime()} {name} написал какую-то херню\n')



    bot.polling()
