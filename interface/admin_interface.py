import telebot
from messages import default_messages_admin, keyboards_admin
from database.best_questions import BestQuestion
from database.all_users import AllUsers
from database import db_session


def admin(bot: telebot.TeleBot, message):
    bot.send_message(message.chat.id, default_messages_admin.HELLO_MESSAGE,
                     reply_markup=keyboards_admin.func_data())

    """Добавялем"""

    @bot.callback_query_handler(func=lambda call: call.data == 'add')  # добавить
    def callback_about(call):
        bot.send_message(message.chat.id, default_messages_admin.HELLO_MESSAGE,
                         reply_markup=keyboards_admin.data())

        """Добавляем админа"""

        @bot.callback_query_handler(func=lambda call: call.data == 'admin')  # admin
        def callback_about(call):
            bot.send_message(message.chat.id, "Введите данные админа по шаблону\n<chat.id>")

            @bot.message_handler()
            def menu(message):
                db_session.global_init("db/db_forum.db")
                db_sess = db_session.create_session()
                org = AllUsers(
                    chat_id=message.text,
                    law=1
                )
                db_sess.add(org)
                db_sess.commit()
                bot.send_message(message.chat.id, "Админ добавлен!")
                admin(bot, message)

        """Добавляем организатора"""

        @bot.callback_query_handler(func=lambda call: call.data == 'org')  # org
        def callback_about(call):
            bot.send_message(message.chat.id, "Введите данные организатора по шаблону\n<chat.id>")

            @bot.message_handler()
            def menu(message):
                db_session.global_init("db/db_forum.db")
                db_sess = db_session.create_session()
                org = AllUsers(
                    chat_id=message.text,
                    law=2
                )
                db_sess.delete(org)
                db_sess.commit()
                bot.send_message(message.chat.id, "Организатор добавлен!")
                admin(bot, message)

        """Добавляем вопрос"""

        @bot.callback_query_handler(func=lambda call: call.data == 'quest')  # quest
        def callback_about(call):
            bot.send_message(message.chat.id, "Введите вопрос по шаблону\n<Вопрос>#<Ответ>")

            @bot.message_handler()
            def menu(message):
                db_session.global_init("db/db_forum.db")
                db_sess = db_session.create_session()
                q_ans_r = message.text.split("#")
                best_quest = BestQuestion(
                    quest=q_ans_r[0],
                    response=q_ans_r[1]
                )
                db_sess.add(best_quest)
                db_sess.commit()
                bot.send_message(message.chat.id, "Вопрос добавлен!")
                admin(bot, message)

    """Удаляем"""

    @bot.callback_query_handler(func=lambda call: call.data == 'delete')  # удалить
    def callback_about(call):
        @bot.callback_query_handler(func=lambda call: call.data == 'admin')  # admin
        def callback_about(call):
            bot.send_message(message.chat.id, "Введите данные админа по шаблону\n<chat.id>")

            @bot.message_handler()
            def menu(message):
                db_session.global_init("db/db_forum.db")
                db_sess = db_session.create_session()
                org = AllUsers(
                    chat_id=message.text,
                    law=1
                )
                db_sess.delete(org)
                db_sess.commit()
                bot.send_message(message.chat.id, "Админ удален!")
                admin(bot, message)

        """Удаляем организатора"""

        @bot.callback_query_handler(func=lambda call: call.data == 'org')  # org
        def callback_about(call):
            bot.send_message(message.chat.id, "Введите данные организатора по шаблону\n<chat.id>")

            @bot.message_handler()
            def menu(message):
                db_session.global_init("db/db_forum.db")
                db_sess = db_session.create_session()
                org = AllUsers(
                    chat_id=message.text,
                    law=2
                )
                db_sess.delete(org)
                db_sess.commit()
                bot.send_message(message.chat.id, "Организатор удален!")
                admin(bot, message)

        """Удаляем вопрос"""

        @bot.callback_query_handler(func=lambda call: call.data == 'quest')  # quest
        def callback_about(call):
            bot.send_message(message.chat.id, "Введите вопрос по шаблону\n<Вопрос>#<Ответ>")

            @bot.message_handler()
            def menu(message):
                db_session.global_init("db/db_forum.db")
                db_sess = db_session.create_session()
                q_ans_r = message.text.split("#")
                best_quest = BestQuestion(
                    quest=q_ans_r[0],
                    response=q_ans_r[1]
                )
                db_sess.add(best_quest)
                db_sess.commit()
                bot.send_message(message.chat.id, "Вопрос добавлен!")
                admin(bot, message)

    @bot.callback_query_handler(func=lambda call: call.data == 'interview')  # создать опрос
    def callback_about(call):
        bot.send_message(message.chat.id, "hello")
