# -*- coding: utf-8 -*-
import logging
import os
import sys
from datetime import datetime

import requests
from requests.models import Request
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from parsel import Selector
from collections import namedtuple


load_dotenv()

Product = namedtuple("Product", "name price")


def pixel_3a(r: Request):
    sel = Selector(text=r.text)
    el = sel.xpath('//div[@data-backend-docid="_pixel_phone_3a_white_64gb_unlocked"]')

    prod_name = el.xpath("./@data-title").get()
    price = el.xpath("./@data-price-v3").get()

    return Product(prod_name, price)


def pixel_4a(r: Request):
    sel = Selector(text=r.text)
    el = sel.xpath('//div[@data-test-product-card="Pixel\xa04a"]')

    prod_name = el.xpath(".//h2/text()").get().replace("\xa0", " ")
    price = el.xpath('.//div[@data-test="main-price0"]/span/text()').get().replace("\xa0", " ")

    return Product(prod_name, price)


def send_notification(product: Product):
    bot = telebot.TeleBot(os.getenv("TOKEN"))

    today = datetime.now().strftime("%d.%m.%Y")
    msg = f"{today}\n\n{product.name} - *{product.price}*"
    kbd = InlineKeyboardMarkup()
    kbd.add(InlineKeyboardButton("open store", url=store_link))
    bot.send_message(os.getenv("CHAT_ID"), msg, parse_mode="markdown", reply_markup=kbd)


# store_link = "https://store.google.com/de/config/pixel_3a"
store_link = "https://store.google.com/de/config/pixel_4a"

r = requests.get(store_link)
if r.status_code != 200:
    logging.error("Non-200 response")
    sys.exit(1)

# product = pixel_3a(r)
product = pixel_4a(r)

print(product)

send_notification(product)
