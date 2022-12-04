import telebot
from messages.default_messages_moder import HELLO_MODER
from messages.keyboards_moder import yes_or_no, answer
from database import db_session
from database.quests import Quest


def moder(bot: telebot.TeleBot, message):
    bot.send_message(message.chat.id, HELLO_MODER, reply_markup=yes_or_no())

    @bot.callback_query_handler(func=lambda call: call.data == 'yes')  # есть ли вопросы
    def answer_callback(call):
        db_session.global_init("db/db_forum.db")
        db_sess = db_session.create_session()
        res = db_sess.query(Quest).first()
        if res is None:
            bot.send_message(message.chat.id, "Вопросов нет")
            moder(bot, message)
        else:
            bot.send_message(message.chat.id, res.quest, reply_markup=answer())

            @bot.callback_query_handler(func=lambda call: call.data == 'answer')  # есть ли вопросы
            def answer_callback(call):
                bot.send_message(message.chat.id, "Отвечай на вопрос")

                @bot.message_handler()
                def handle_message(message):
                    bot.send_message(res.chat_id, f"Ответ на вопрос:{res.quest}?:\n{message.text}")
                    db_sess.delete(res)
                    db_sess.commit()
                    moder(bot, message)
