import telebot
import random
from config import bot_token

bot = telebot.TeleBot(bot_token)

DIGITS = [str(x) for x in range(10)]
my_number = ''

@bot.message_handler(commands=['start', 'game'])
def start_game(message):
    digits = DIGITS.copy()
    global my_number
    my_number = ''
    for pos in range(4):
        if pos:
            digit = random.choice(digits)
        else: 
            digit = random.choice(digits[1:])
        my_number += digit
        digits.remove(digit)
    print(my_number)
    bot.reply_to(message, 'Гра "Бики й корови"\n'
        f'Я загадав 4-значне число. Спробуй відгадати, {message.from_user.first_name}!')

@bot.message_handler(content_types=['text'])
def bot_answer(message):
    text = message.text
    if len(text) == 4 and text.isnumeric() and len(text) == len(set(text)):
        cows, bulls = 0, 0
        for i in range(4):
            if text[i] in my_number:
                if text[i] == my_number[i]:
                    bulls += 1
                else:
                    cows += 1
        if bulls == 4:
            response = 'Ти вгадав!'
        else:
            response = f'Бики: {bulls} | Корови : {cows}'
    else:
        response = 'Прийшли мені 4-значне число з різними цифрами!'
    bot.send_message(message.from_user.id, response)

if __name__ == '__main__':
    bot.polling(non_stop=True)