import telebot
from messages import default_messages_admin, keyboards_admin


def admin(bot: telebot.TeleBot, message):
    bot.send_message(message.chat.id, default_messages_admin.HELLO_MESSAGE,
                     reply_markup=keyboards_admin.func_data())

    @bot.callback_query_handler(func=lambda call: call.data == 'add')  # добавить
    def add_callback(call):
        """Добавяляем"""
        bot.send_message(message.chat.id, default_messages_admin.FUNC_MESSAGE,
                         reply_markup=keyboards_admin.data_add())

        @bot.callback_query_handler(func=lambda call: call.data == 'program')  # мероприятие
        def add_party_callback(call):
            """Добавляем мероприятие"""

            bot.send_message(message.chat.id,
                             "Отправь excel файл по шаблону:\n""(<назание><о мероприятии><начало><конец><место><спикеры><модераторы><темы>)")

            @bot.message_handler(content_types=['document'])
            def handle_file(message):
                from tools_admin.add_party import add_party
                add_party(bot, message)
                bot.send_message(message.chat.id, "Вся программа из excel добавлена!")
                admin(bot, message)

        @bot.callback_query_handler(func=lambda call: call.data == 'program_reg')  # мероприятие
        def add_party_callback(call):
            """Добавляем мероприятия с регистрацией"""

            bot.send_message(message.chat.id,
                             "Отправь excel файл по шаблону:\n""(<начало><содержание><максимальное количество человек>)")

            @bot.message_handler(content_types=['document'])
            def handle_file(message):
                from tools_admin.add_party import add_party
                add_party(bot, message)
                bot.send_message(message.chat.id, "Вся программа из excel добавлена!")
                admin(bot, message)

        @bot.callback_query_handler(func=lambda call: call.data == 'admin')  # админ
        def add_admin_callback(call):
            """Добавляем админа"""
            bot.send_message(message.chat.id, default_messages_admin.WORK_WAY,
                             reply_markup=keyboards_admin.ways())

            @bot.callback_query_handler(func=lambda call: call.data == 'excel')  # excel
            def add_admin_excel_callback(call):
                bot.send_message(message.chat.id, "Отправь excel файл(одна колонка с <chat_id>)")

                @bot.message_handler(content_types=['document'])
                def handle_file(message):
                    from tools_admin.add_admin_excel import add_admin_excel
                    add_admin_excel(bot, message)
                    bot.send_message(message.chat.id, "Все админы из excel добавлены!")
                    admin(bot, message)

            @bot.callback_query_handler(func=lambda call: call.data == 'work')  # вручную
            def add_admin_work_callback(call):
                bot.send_message(message.chat.id, "Введите данные админа по шаблону\n<chat.id>")

                @bot.message_handler()
                def handle_message(message):
                    from tools_admin.add_admin_work import add_admin_work
                    add_admin_work(message)
                    bot.send_message(message.chat.id, "Админ добавлен!")
                    admin(bot, message)

        """Добавляем организатора"""

        @bot.callback_query_handler(func=lambda call: call.data == 'org')  # org
        def add_org_callback(call):
            bot.send_message(message.chat.id, default_messages_admin.WORK_WAY,
                             reply_markup=keyboards_admin.ways())

            @bot.callback_query_handler(func=lambda call: call.data == 'excel')  # excel
            def add_org_excel_callback(call):
                bot.send_message(message.chat.id, "Отправь excel файл(одна колонка с <chat_id>)")

                @bot.message_handler(content_types=['document'])
                def handle_file(message):
                    from tools_admin.add_org_excel import add_org_excel
                    add_org_excel(bot, message)
                    bot.send_message(message.chat.id, "Все организаторы из excel добавлены!")
                    admin(bot, message)

            @bot.callback_query_handler(func=lambda call: call.data == 'excel')  # вручную
            def add_org_work_callback(call):
                bot.send_message(message.chat.id, "Введите данные организатора по шаблону\n<chat.id>")

                @bot.message_handler()
                def handle_message(message):
                    from tools_admin.add_org_work import add_org_work
                    add_org_work(message)
                    bot.send_message(message.chat.id, "Организатор добавлен!")
                    admin(bot, message)

        """Добавляем вопрос"""

        @bot.callback_query_handler(func=lambda call: call.data == 'quest')  # quest
        def add_quest_callback(call):
            bot.send_message(message.chat.id, "Введите вопрос по шаблону\n<Вопрос>#<Ответ>")

            @bot.message_handler()
            def handle_message(message):
                from tools_admin.add_quest import add_quest
                add_quest(message)
                bot.send_message(message.chat.id, "Вопрос добавлен!")
                admin(bot, message)

    @bot.callback_query_handler(func=lambda call: call.data == 'delete')  # удалить
    def delete_callback(call):
        """Удаляем"""
        bot.send_message(message.chat.id, default_messages_admin.FUNC_MESSAGE,
                         reply_markup=keyboards_admin.data_delete())

        @bot.callback_query_handler(func=lambda call: call.data == 'admin')  # admin
        def delete_admin_callback(call):
            """Удаляем Админа"""
            bot.send_message(message.chat.id, "Введите данные админа по шаблону\n<chat.id>")

            @bot.message_handler()
            def menu(message):
                from tools_admin.delete_admin import delete_admin
                delete_admin(message)
                bot.send_message(message.chat.id, "Админ удален!")
                admin(bot, message)

        @bot.callback_query_handler(func=lambda call: call.data == 'org')  # org
        def callback_about(call):
            """Удаляем организатора"""
            bot.send_message(message.chat.id, "Введите данные организатора по шаблону\n<chat.id>")

            @bot.message_handler()
            def menu(message):
                from tools_admin.delete_org import delete_org
                delete_org(message)
                bot.send_message(message.chat.id, "Организатор удален!")
                admin(bot, message)

        """Удаляем вопрос"""

        @bot.callback_query_handler(func=lambda call: call.data == 'quest')  # quest
        def callback_about(call):
            bot.send_message(message.chat.id, "Введите вопрос по шаблону\n<Вопрос>#<Ответ>")

            @bot.message_handler()
            def menu(message):
                from tools_admin.delete_quest import delete_quest
                delete_quest(message)
                bot.send_message(message.chat.id, "Вопрос добавлен!")
                admin(bot, message)
