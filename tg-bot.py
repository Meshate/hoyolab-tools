from .utils import log
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


if __name__ == '__main__':
    application = ApplicationBuilder().token('TOKEN').build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.run_polling()

class BotSession(object):
    def __int__(self, cookie: str, type: int):
        self.cookie = cookie
        self.client =

class BotProcess(object):
    def __int__(self):
        self.sessions = {}
