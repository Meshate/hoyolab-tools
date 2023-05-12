import queue
import threading

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from config import TG_TOKEN
from utils import log
from hoyolab import StarRail, Genshin
from template import *
import schedule, time, asyncio

create_func = {
    '1': StarRail,
    '2': Genshin
}

funcs = [
    StarRail,
    Genshin
]

user_datas = []

q = queue.Queue()

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

# async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     if len(context.args) < 2:
#         await update.effective_message.reply_text(text=register_template_error_cmd)
#     log.debug(context.user_data)
#     fun = create_func.get(context.args[0])
#     if fun:
#         context.user_data[f'{context.args[0]}_{context._user_id}'] = fun(''.join(context.args[1:]))
#         await update.effective_message.reply_text(text=register_template_success)
#     else:
#         await update.effective_message.reply_text(text=register_template_error_game)

async def register_new(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 1:
        await update.effective_message.reply_text(text=register_template_error_cmd)
        return
    user_data = {
        'clients': [],
        'context': context
    }
    for f in funcs:
        user_data['clients'].append(f(''.join(context.args)))
    # datas = []
    if not q.empty():
        datas = q.get()
        datas.append(user_data)
    else:
        datas = [user_data]
    q.put(datas)
    # user_datas.append(user_data)
    await update.effective_message.reply_text(text=register_template_success)

async def check_in():
    if not q.empty():
        datas = q.get()
        for data in datas:
            for c in data['clients']:
                m = c.sign()
                if not m:
                    await data['context'].bot.send_message(chat_id=data['context']._chat_id, text=check_in_template_error_msg)
                else:
                    await data['context'].bot.send_message(chat_id=data['context']._chat_id, text=check_in_template_msg.format(m))
        q.put(datas)

def run_async_task():
    asyncio.run(check_in())

def loop():
    # schedule.every().day.at("00:01").do(check_in)
    schedule.every().minute.do(run_async_task)
    while True:
        schedule.run_pending()
        log.debug('starting looping-----------------------------------')
        time.sleep(5)

async def check_in2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 1:
        await update.effective_message.reply_text(text=register_template_error_cmd)
        return
    client = context.user_data.get(f'{context.args[0]}_{context._user_id}')
    if client == None:
        await update.effective_chat.send_message(text=check_in_template_error_no_register)
    else:
        msg = client.sign()
        await update.effective_chat.send_message(text=check_in_template_msg.format(msg))

class BotProcess(object):
    def __init__(self, token: str = None):
        self.sessions = []
        self.application = ApplicationBuilder().token(token).build()

    def start(self):
        self.application.add_handler(CommandHandler('echo', echo))
        self.application.add_handler(CommandHandler('echo2', echo2))
        self.application.add_handler(CommandHandler('echo3', echo3))
        self.application.add_handler(CommandHandler('echo4', echo4))
        self.application.add_handler(CommandHandler(['reg', 'register'], register_new))
        self.application.add_handler(CommandHandler(['check_in', 'c'], check_in2))

        self.application.run_polling()

if __name__ == '__main__':
    thread = threading.Thread(target=loop)
    thread.start()
    bot = BotProcess(TG_TOKEN)
    bot.start()
    thread.join()