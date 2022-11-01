# добавляем класс-родитель
from handlers.handler import Handler

# Наследуемся от него
class HanderCommands(Handler):
    """
    Класс будет обрабатывать входящие команды:
    /start
    /help
    """

    def __init__(self, bot):
        super().__init__(bot)

    # обработка /start
    def pressed_btn_start(self, message):

        self.bot.send_message(message.chat.id,
                              f' Ты продрал глаза в номере портового барделя, в руке ты обнаруживаешь початую бутылку с виски. Пошатываясь ты выходишь на улицу',
                              reply_markup=self.keybords.start_menu())

    def handle(self):
        #Обработчик сообщений, который обрабатывает входящие /start сообщения
        @self.bot.message_handler(commands = ['start'])
        def handle(message):
            print(message)
            if message.text == '/start':
                self.pressed_btn_start(message)







