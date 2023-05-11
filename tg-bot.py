from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from config import TG_TOKEN
from utils import log
from hoyolab import StarRail, Genshin
from template import *

user_info = {}

create_func = {
    '1': StarRail,
    '2': Genshin
}

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = ''.join(context.args)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def echo2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = ''.join(context.args)
    await update.message.reply_text(text=text)

async def echo3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = ''.join(context.args)
    await update.effective_message.reply_text(text=text)

async def echo4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = ''.join(context.args)
    await update.effective_chat.send_message(text=text)

async def userdata(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_chat.send_message(text=f'userid={context._user_id}')

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.effective_message.reply_text(text=register_template_error_cmd)
    log.debug(context.user_data)
    fun = create_func.get(context.args[0])
    if fun:
        context.user_data[f'{context.args[0]}_{context._user_id}'] = fun(''.join(context.args[1:]))
        await update.effective_message.reply_text(text=register_template_success)
    else:
        await update.effective_message.reply_text(text=register_template_error_game)

async def check_in(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 1:
        await update.effective_message.reply_text(text=register_template_error_cmd)
        return
    client = context.user_data.get(f'{context.args[0]}_{context._user_id}')
    if client == None:
        await update.effective_chat.send_message(text=check_in_template_error_no_register)
    else:
        msg = client.sign()
        await update.effective_chat.send_message(text=check_in_template_msg.format(msg))

class BotSession(object):
    def __int__(self, cookie: str, type: int):
        self.cookie = cookie
        self.client = None

class BotProcess(object):
    def __init__(self, token: str = None):
        self.sessions = []
        self.application = ApplicationBuilder().token(token).build()

    def start(self):
        self.application.add_handler(CommandHandler('echo', echo))
        self.application.add_handler(CommandHandler('echo2', echo2))
        self.application.add_handler(CommandHandler('echo3', echo3))
        self.application.add_handler(CommandHandler('echo4', echo4))
        self.application.add_handler(CommandHandler('me', userdata))
        self.application.add_handler(CommandHandler(['reg', 'register'], register))
        self.application.add_handler(CommandHandler(['check_in', 'c'], check_in))

        self.application.run_polling()

if __name__ == '__main__':
    bot = BotProcess(TG_TOKEN)
    bot.start()