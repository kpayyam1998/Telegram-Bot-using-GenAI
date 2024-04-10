import os
import logging 
import openai
from aiogram import Bot,Dispatcher,executor,types
from dotenv import load_dotenv


load_dotenv()
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
TOKEN=os.getenv("TELEGRAM_BOT_TOKEN")

#loaded api key to openai
openai.api_key=OPENAI_API_KEY

MODEL_NAME="gpt-3.5-turbo"

#initialize bot token
bot=Bot(token=TOKEN)
dispatcher=Dispatcher(bot)

class Reference:
    def __init__(self) -> None:
        self.response=""
    
referece=Reference()

def clear_past():
    referece.response=""

# Clear past converstion
@dispatcher.message_handler(commands=['clear'])
async def clear(messge:types.Message):
    """
    This handler to clear the previous conversation and context

    """
    clear_past()
    await messge.reply("i have cleared the past conversation and context")


# Start conversation method
@dispatcher.message_handler(commands=['start'])
async def welcome(message:types.Message):
    """
    this handler receives the message with `/start` or `/help`
    
    args:

    message:types.Message): _description_
    """
    await message.reply("Hi \n i am a Chat bot ! Created  by kp. how can i assist you?")


@dispatcher.message_handler(commands=['help'])
async def helper(message:types.Message):
    """
    Handler will display help menu
    """

    help_command="""
    Hi there i am created by kp ! please follwing by this command
    /start -start the converstion
    /clear - clear the past converstion
    /help  -to get help from menu

    """
    await message.reply(help_command)

@dispatcher.message_handler()
async def main_bot(message:types.Message):
    """
        Handler to process the user 's input  and generate response using the openai  API
    """
    print(f">>> USER:\n \t {message.text}")

    response=openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=[
            {"role":"assistant","content":referece.response},# assistent role
            {"role":"user","content":message.text} #our query
        ]
    )
    
    referece.response=response['choices'][0]['message']['content']
    print(f">>>>Chat GBT:\n \t{referece.response}")

    await bot.send_message(chat_id=message.chat.id,text=referece.response)


if __name__=="__main__":
    executor.start_polling(dispatcher,skip_updates=True)


