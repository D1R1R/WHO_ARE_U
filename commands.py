from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup


reply_keyboard = [
        ['/commands', '/developers'],
        ['/help', '/start'],
        ['/close']
        ]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    
async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я бот который поможет тебе найти любого человека. Попробуй написать /commands мне и я выведу список команд.",
        reply_markup=markup
    )

async def commands_list(update, context):
    await update.message.reply_text(
        "1) Поиск по семье: 'Семья: позиция полное имя'\n2) Поиск по работе: 'Работа: работа в страна'\n3) Поиск по месту: 'Место: страна'",
        reply_markup=markup
    )

async def dev(update, context):
    await update.message.reply_text(
        "Введите сообщение с четким описанием проблемы. Для удобства пожалуйста скопируйте ваше сообщение и ответ бота, так проблема будет яснее. Спасибо за ваше участие в развитии бота.",
        reply_markup=markup
    )


async def help_command(update, context):
    await update.message.reply_text(" Попробуй написать /commands мне и я выведу список команд. Если что-то не работает, то обратись к разработчику командой /developers")


async def close_keyboard(update, context):
    await update.message.reply_text(
        "Чтобы вернуть клавиатуру напишите /open_keyboard",
        reply_markup=ReplyKeyboardRemove()
    )


async def open_keyboard(update, context):
    await update.message.reply_text(
        """Чтобы закрыть клавиатуру напишите /close или нажмите соответсятвующую кнопку""",
        reply_markup=markup
    )
