import logging
from telegram.ext import Application, filters
from telegram.ext import CommandHandler, MessageHandler

import commands
import data


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
analyzer = data.Question_analyzer()

async def algorithm(update, context):
    reply_msg = analyzer.analyze(update.message.text)
    answer = ['Вот что мне удалось найти:',]
    num = 1
    for names in reply_msg.keys():
        answer.append(f'{num}) ' + names + ' --> ' + reply_msg[names])
        num += 1
    if len(answer) == 1:
        answer = ['К сожалению, я ничего не нашел.(']
    await update.message.reply_text('\n'.join(answer))


def main():
    application = Application.builder().token('6214335284:AAHU-Qi0INPRfcWAW9Di6mehqGzCd1j0KPU').build()

    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, algorithm)
    application.add_handler(text_handler)
    # commands:
    application.add_handler(CommandHandler("start", commands.start))
    application.add_handler(CommandHandler("close", commands.close_keyboard))
    application.add_handler(CommandHandler("open_keyboard", commands.open_keyboard))
    application.add_handler(CommandHandler("help", commands.help_command))
    application.add_handler(CommandHandler("commands", commands.commands_list))
    application.add_handler(CommandHandler("developers", commands.dev))
    

    application.run_polling()


if __name__ == '__main__':
    main()
