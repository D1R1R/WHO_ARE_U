from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
import smtplib
from email.message import EmailMessage


reply_keyboard = [
        ['/commands', '/developers'],
        ['/help', '/start'],
        ['/close']
        ]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    
async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"""
Привет, {user.mention_html()}! 😄
Я бот который поможет тебе найти любого человека. Попробуй написать /commands мне и я выведу список команд.""",
        reply_markup=markup
    )

async def commands_list(update, context):
    await update.message.reply_text(
        """
<!!> Возможности:
👉Спросите у бота о семье человека!
"Чей отец Иоганн Себастьян Бах?"
👉Узнай какие люди живут во Франции.
"Кто живет во Франции?"
👉Спроси про журналистов из России!
"Какие журанлисты есть в России?"

*Бот реагирует исключительно на вопросы.
        """,
        reply_markup=markup
    )

async def dev(update, context):
    await update.message.reply_text(
        """
👉Чат разработчиков: @otziv_who .
Зайдя в чат вы можете поучавствовать в развитии бота, отавив там свой отзыв!
Так же вы можете увидеть как развился и улучшился бот из-за отзывов.
Спасибо за ваше участие в развитии бота.""",
        reply_markup=markup
    )


async def help_command(update, context):
    await update.message.reply_text(
        """
Попробуй написать /commands мне и я выведу список команд.
Если что-то не работает, то обратись к разработчику командой /developers ✌️""",
        reply_markup=markup
    )


async def close_keyboard(update, context):
    await update.message.reply_text(
        "Чтобы вернуть клавиатуру напишите /open_keyboard",
        reply_markup=ReplyKeyboardRemove()
    )


async def open_keyboard(update, context):
    await update.message.reply_text(
        "Чтобы закрыть клавиатуру напишите /close или нажмите соответсятвующую кнопку",
        reply_markup=markup
    )
