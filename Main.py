from Server import keep_alive
# import pip
import telebot
import openai
import json

# pip.main(['install', 'pytelegrambotapi'])

bot = telebot.TeleBot('')

openai_api_key = ''

is_processing = False

with open('Info.json', 'r') as info_file:
    info_data = json.load(info_file)


def chat_with_gpt(prompt):
    openai.api_key = openai_api_key
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=150
    )
    return response.choices[0].text.strip()


@bot.message_handler(commands=['start'])
def start_handler(message):
    global is_processing
    is_processing = True
    bot.send_message(
        message.chat.id,
        "Hello! \nPlease write text to search...")


@bot.message_handler(func=lambda message: True)
def user_message(message):
    global is_processing
    if is_processing:
        try:
            user_text = message.text.lower()
            chat_prompt = f"Search for: '{user_text}'."
            gpt_response = chat_with_gpt(chat_prompt)
            if user_text in info_data:
                bot.send_message(message.chat.id, f"FIND SOME INFO: {info_data[user_text]}")
            else:
                bot.send_message(message.chat.id, "Sorry, no info.")
        except ValueError:
            bot.send_message(message.chat.id, "Error TEXT please try again")
        finally:
            bot.stop_polling()

    # send info from ChatGPT API
    bot.send_message(message.chat.id, f"ChatGPT says: {gpt_response}")


# @bot.message_handler(content_types=['text'])
# def text_handler(message):
#     global is_processing
#     if is_processing:
#         try:
#             distance, fuel_consumption, fuel_cost = map(float, message.text.split())
#             if distance <= 0 or fuel_consumption <= 0 or fuel_cost <= 0:
#                 raise ValueError
#             fuel_volume = distance / 100 * fuel_consumption
#             trip_cost = fuel_volume * fuel_cost
#             cost_third = (fuel_volume * fuel_cost) / 3
#             bot.send_message(message.chat.id, f"Результат: Загальна сумма {trip_cost} грн")
#             bot.send_message(message.chat.id, f"З кожного по: {cost_third:.2f} грн")
#         except ValueError:
#             bot.send_message(
#                 message.chat.id,
#                 "Error TEXT please try again")
#         finally:
#             bot.stop_polling()

if __name__ == "__main__":
    keep_alive()  # start flask server
    bot.polling(non_stop=True, interval=0)  # start bot
