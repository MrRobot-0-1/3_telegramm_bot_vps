import requests
from datetime import datetime, timedelta
import telebot
from auth_data import token
from background import keep_alive


def get_data():
    req = requests.get("https://yobit.net/api/3/ticker/btc_usd")
    response = req.json()
    sell_price = response["btc_usd"]["sell"]
    print(f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\nЦена продажи BTC: {sell_price}")


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start_massage(massage):
        bot.send_message(massage.chat.id, "Привет, друг! Напишите 'price', чтобы узнать стоимость BTC!")

    @bot.message_handler(content_types=["text"])
    def send_text(massage):
        if massage.text.lower() == "price":
            try:
                req = requests.get("https://yobit.net/api/3/ticker/btc_usd")
                response = req.json()
                sell_price = response["btc_usd"]["sell"]
                bot.send_message(
                    massage.chat.id,
                    f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\nЦена продажи BTC: {sell_price}"
                )
            except Exception as ex:
                print(ex)
                bot.send_message(
                    massage.chat.id,
                    "Упс...Что-то пошло не так..."
                )
        else:
            bot.send_message(massage.chat.id, "Что это??? Проверь команду, чувак!")

    bot.polling()


keep_alive()
if __name__ == '__main__':
    # get_data()
    telegram_bot(token)