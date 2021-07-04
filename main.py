import requests
import datetime
from requests.api import post
import telebot
import pytz
import json
import traceback
import os

from telebot import types

from config import token,group_name,BOT_KEY

fresh_post = ''
#получение постов из ВК
def get_wallPost():
  url = f'https://api.vk.com/method/wall.get?owner_id={group_name}&count=2&access_token={token}&v=5.52'
  req = requests.get(url)
  src = req.json()
  post = src['response']['items']
  current_post = post[1]
  # print(post[1]['text'])
  # print(post[1]['attachments'][0]['poll']['question'])
  # print(post[1]['attachments'][0]['poll']['votes'], post[1]['attachments'][0]['poll']['answers'])
  if os.path.exists(f"{group_name}"):
    print(f"директория {group_name} уже есть")
  else:
    os.mkdir(group_name)

  with open(f"{group_name}/group_name.json", "w", encoding="utf-8") as file:
    json.dump(current_post, file, indent=4, ensure_ascii=False)
  return current_post
# get_wallPost()

# fresh_post = get_wallPost()
#инициализация бота
bot = telebot.TeleBot(BOT_KEY)



@bot.message_handler(commands = ['start'])
def start_command (message):
  keyboard = telebot.types.InlineKeyboardMarkup()
  keyboard.row (
    telebot.types.InlineKeyboardButton( 'Куда', callback_data='get_wallPost'),
    telebot.types.InlineKeyboardButton('Кто идет', callback_data='get_statisticks')
  )
  bot.send_message(
    message.chat.id,
    'Могу рассказать все что знаю о милонгах в Питере \n'+
    'Чтобы узнать, какие милонги сегодня есть нажмите /куда \n'+
    'Чтобы узнать подробнее нажмите ./кто идет \n',
    reply_markup=keyboard
  )
@bot.callback_query_handler(func=lambda callback:True)
def answer(callback):
  fresh_post = get_wallPost()
  chat_id = callback.message.chat.id
  current_votes = fresh_post['attachments'][0]['poll']['answers']
  keyboard = types.InlineKeyboardMarkup()
  keyboard.row (
    telebot.types.InlineKeyboardButton( 'Куда', callback_data='get_wallPost'),
    telebot.types.InlineKeyboardButton('Кто идет', callback_data='get_statisticks')
  )
  if callback.data == "get_wallPost":   
    bot.send_message(chat_id,fresh_post['text'], reply_markup=keyboard)
    start_command
  if callback.data == "get_statisticks":    
    for item in current_votes:
      bot.send_message(chat_id,
      f"{item['text']} идет :{item['votes']}  человек")
    start_command
bot.polling(none_stop=True)





