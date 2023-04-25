import os
import logging
from telegram.ext import Application, filters
from telegram.ext import CommandHandler, MessageHandler

import commands
import data

BOT_TOKEN = os.environ.get('BOT_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
analyzer = data.Question_analyzer()

async def algorithm(update, context):
    #gif
    with open('load.gif', 'rb') as img:
        await context.bot.send_animation(
            update.message.chat_id, img, caption='ищу что-то по вашему запросу!'
            )
    # redky msg analyzing
    reply_msg = analyzer.analyze(update.message.text)
    answer = ['Вот что мне удалось найти:',]
    num = 1
    try:
        for names in reply_msg.keys():
            answer.append(f'{num}) ' + names + ' --> ' + reply_msg[names])
            num += 1
        if len(answer) == 1:
            answer = ['К сожалению, я ничего не нашел.(']
        await update.message.reply_text('\n'.join(answer))
    except:
        if reply_msg:
            await update.message.reply_text(reply_msg)
        else:
            await update.message.reply_text('Хватит баловаться!')



def main():
    application = Application.builder().token(BOT_TOKEN).build()

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
