"""
FileBot
-----------------
Telegram based Bot for edit files (copy, move and rename) remotely.



Created by J.G.Aguado
25/02/2018
"""

#Import modules and libraries
import os
import time
import json
import pandas as pd

import logging
import telegram
from telegram.ext import Updater, CommandHandler

#Editable variables
session = json.load(open(r'session.txt'))

refresh_time = 10
path_2_check = session['CHECK_FOLDER']
log_path = r'log.txt'
file_extensions = ['avi', 'mkv', 'mp4']
status = ['File found', 'Processing', 'Processed', 'User notified', 'Action received', 'Testing']

update_id = None
my_user_id = session['CHAT_ID']
TOKEN = session['TOKEN']

def telegram_init():
    global update_id
    # Telegram Bot Authorization Token
    bot = telegram.Bot(TOKEN)

    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    return bot


def move(bot, update, id):
    pass

# def rename(bot, update, id):
#     pass
#
# def rename_and_move(bot, update, id):
#     rename(bot, update, id)
#     move(bot, update, id)

def echo(bot):
    """Echo the message the user sent."""
    global update_id
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

        if update.message:  # your bot can receive updates without messages
            # Reply to the message
            update.message.reply_text(update.message.text)
            print(update.message.text)


def checker():
    check = False
    file_path = []
    for path, _, files in os.walk(path_2_check):
        # print(path, files)
        for file in files:
            extension = file.split('.')[-1]
            if extension in file_extensions:
                check = True
                file_path.append(path + '\\' + file)
    return check, file_path

def read_log():
    return pd.read_csv(log_path, index_col=0)


def write_log(log, ID=None, st=None, Input=None, Output=None):
    if ID is None:
        ID = len(log.axes[0])

    Date = time.strftime("%H:%M:%S-%d/%m/%Y")

    log.loc[ID] = [Date, st, Input, Output]
    log.to_csv(log_path)
    return log

def status_selection(input):
    for file in input:
        if file in log.Input.values:
            index = [i for i, x in enumerate(file == log.Input.values) if x][-1]
            if log.Status[index] == status[0]:
                print(log.Status[index])
            elif log.Status[index] == status[1]:
                print(log.Status[index])
            elif log.Status[index] == status[2]:
                print(log.Status[index])
        else:
            print('File not found in log')

def new_file(log, input):
    for file in input:
        if file not in log.Input.values:
            write_log(log, st=status[0], Input=file)

def st_file_found(log, bot):
    if (log.Status.values==status[0]).max():
        msg = ["Hi dude, I have found <b>new files</b>:"]
        index = [i for i, x in enumerate(log.Status.values == status[0]) if x]
        for ii in index:
            msg.append("    -File " + str(ii) + ': ' + log.Input[ii])

        msg.append("Want to /Move(id, path) or /Rename_and_move(id, new_name, path) ? ")
        msg = "\n \n".join(msg)
        bot.sendMessage(my_user_id, msg, parse_mode='HTML')

if __name__ == '__main__':
    bot = telegram_init()

    while True:
        echo(bot)
        log = read_log()
        check, files = checker()

        if check:
            new_file(log, files)

        st_file_found(log, bot)

        time.sleep(refresh_time)
