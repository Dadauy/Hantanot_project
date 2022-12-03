from interface import user_interface, admin_interface
from database import db_session
from settings.config import BOT_TOKEN
import telebot
from database.all_users import AllUsers

# init
bot = telebot.TeleBot(BOT_TOKEN)


# message handlers
@bot.message_handler(commands=['start'])  # Вывод приветственной клавиатуры
def start_hello(message):
    db_session.global_init("db/db_forum.db")
    db_sess = db_session.create_session()
    res = db_sess.query(AllUsers).filter(AllUsers.chat_id == message.chat.id).first()  # данные о юзере
    if res is None:
        user = AllUsers(
            chat_id=message.chat.id,
            law=0
        )
        db_sess.add(user)
        db_sess.commit()
        user_interface.user(bot, message, db_sess)
    elif res.law == 1:  # если админ
        admin_interface.admin(bot, message)
    elif res.law == 2:
        pass


bot.enable_save_next_step_handlers(delay=1)
bot.load_next_step_handlers()
bot.infinity_polling()
