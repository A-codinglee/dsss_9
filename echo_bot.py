import requests
import telebot

bot = telebot.TeleBot("7252388314:AAHFz7n2EE0ybo2SXZR1SaXukacV8wXNC3I", parse_mode=None)

# Endpoint for your locally running LLM backend
LLM_BACKEND_URL = "http://127.0.0.1:5000/chat"
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Ask me anything.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user_input = message.text
    try:
        # Send user input to LLM backend
        response = requests.post(LLM_BACKEND_URL, json={"message": user_input})
        if response.status_code == 200:
            llm_reply = response.json().get("response", "Sorry, I couldn't process that.")
        else:
            llm_reply = "Error: Unable to connect to the AI backend."
    except Exception as e:
        llm_reply = f"An error occurred: {str(e)}"

    # Send LLM's response back to the user
    bot.reply_to(message, llm_reply)

bot.infinity_polling()
