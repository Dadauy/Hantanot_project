import telebot
import datetime

from messages import default_messages_user, keyboards_user
from database import db_session
from database.programma import Programma


def programma_menu(bot: telebot.TeleBot, message, db_sess):

    '''
    speakers = db_sess.query(Programma).all()
    for speaker in speakers:
        # Создаём клавиатуру для инфы про спикеров
        keyb = telebot.types.InlineKeyboardMarkup()
        data = "speaker_number:" + str(speaker.id)
        btn = telebot.types.InlineKeyboardButton(text="Узнать больше",
                                                 callback_data=data)
        keyb.add(btn)
        description = default_messages_user.small_speaker_description(speaker)
        bot.send_message(message.chat.id,
                         description,
                         reply_markup=keyb)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("speaker_number:"))
    def get_speaker_info(call):
        pass
    '''