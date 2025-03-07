from flask import Flask, request
import telebot
from openai import OpenAI
import { Analytics } from "@vercel/analytics/react"
app = Flask(__name__)
bot = telebot.TeleBot("7259483767:AAHHOlf8GvucCs9d7f8leXvzI0o7TjQrjHE")
client = OpenAI(api_key="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")

# 텔레그램 메시지 핸들러
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message.text}]
    )
    bot.reply_to(message, response.choices[0].message.content)

# Flask 서버 설정 (Vercel 호환용)
@app.route('/')
def home():
    return "AI ChatBot Running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'OK', 200

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url="https://my-aiz-bot.vercel.app/webhook")
    app.run()
