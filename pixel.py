# -*- coding: utf-8 -*-
import logging
import os
import sys
from datetime import datetime

import requests
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from parsel import Selector


load_dotenv()

store_link = "https://store.google.com/de/config/pixel_3a"
r = requests.get(store_link)
if r.status_code != 200:
    logging.error("Non-200 response")
    sys.exit(1)

sel = Selector(text=r.text)
el = sel.xpath('//div[@data-backend-docid="_pixel_phone_3a_white_64gb_unlocked"]')

prod_name = el.xpath("./@data-title").get()
price = el.xpath("./@data-price-v3").get()

print(prod_name, price)

bot = telebot.TeleBot(os.getenv("TOKEN"))

today = datetime.now().strftime("%d.%m.%Y")
msg = f"{today}\n\n{prod_name} - *{price}*"
kbd = InlineKeyboardMarkup()
kbd.add(InlineKeyboardButton("open store", url=store_link))
bot.send_message(os.getenv("CHAT_ID"), msg, parse_mode="markdown", reply_markup=kbd)
