from settings.message import MESSAGES
from handlers.handler import Handler
from settings import config
from settings import utility

class HendlerAllText(Handler):
    #класс обрабатывает входящие текстовые сообщения от нажатия на кнопку


    def __int__(self, bot):
        super().__init__(bot)
        # шаг в заказе
        self.step = 0

    def pressed_btn_category(self, message):
        '''
        обработка сообщений от нажатия кнопки category
        '''
        self.bot.send_message(message.chat.id, 'Каталог категорий товара',
                              parse_mode="HTML",
                              reply_markup=self.keybords.remove_menu())
        self.bot.send_message(message.chat.id, 'Сделайте свой выбор',
                              parse_mode="HTML",
                              reply_markup=self.keybords.category_menu())


    def pressed_btn_info(self, message):
        '''
        обработка сообщений от нажатия кнопки info
        '''
        self.bot.send_message(message.chat.id, MESSAGES['onboard'],
                              parse_mode="HTML",
                              reply_markup=self.keybords.info_menu())


    def pressed_btn_settings(self, message):
        '''
        обработка сообщений от нажатия кнопки settings
        '''
        self.bot.send_message(message.chat.id, MESSAGES['settings'],
                              parse_mode="HTML",
                              reply_markup=self.keybords.settings_menu())

    def pressed_btn_back(self, message):
        '''
        обработка сообщений от нажатия кнопки back
        '''
        self.bot.send_message(message.chat.id, 'Вы вернулись назад',
                              parse_mode="HTML",
                              reply_markup=self.keybords.start_menu())

    def pressed_btn_product(self, message, product):
        '''
        обрабатывает нажатие на кнопки товаров
        '''
        self.bot.send_message(message.chat.id, 'Категория' + config.KEYBOARD[product],
                              reply_markup=self.keybords.set_select_cathegory(config.CATEGORY[product]))
        self.bot.send_message(message.chat.id, "Ok",
                              reply_markup=self.keybords.category_menu())

    def pressed_btn_order(self, message):
        '''
        обрабатывает нажатие на кнопку "Заказ"
        '''

        self.step = 0
        count = self.BD.select_all_product_id()
        quantity = self.BD.select_order_quantity(count[self.step])
        self.send_message_order(count[self.step], quantity, message)

    def send_message_order(self, product_id, quantity, message):
        """
        Отправляет ответ пользователю при выполнении различных действий
        """
        self.bot.send_message(message.chat.id,MESSAGES['order_number'].format(
            self.step+1), parse_mode="HTML")
        self.bot.send_message(message.chat.id,
                              MESSAGES['order'].
                              format(self.BD.select_single_product_name(
                                  product_id),
                                     self.BD.select_single_product_title(
                                         product_id),
                                     self.BD.select_single_product_price(
                                         product_id),
                                     self.BD.select_order_quantity(
                                         product_id)),
                              parse_mode="HTML",
                              reply_markup=self.keybords.orders_menu(
                                  self.step, quantity))

    def pressed_btn_up(self, message):
        count = self.BD.select_all_product_id()
        # количество товара в заказе
        quantity_order = self.BD.select_order_quantity(count[self.step])
        # количество товара на складе
        quantity_product = self.BD.select_single_product_quantity(count[self.step])

        if quantity_product > 0:
            quantity_order += 1
            quantity_product -= 1
            # вносим в БД
            self.BD.update_order_value(count[self.step], 'quantity', quantity_order)
            self.BD.update_product_value(count[self.step], 'quantity', quantity_product)
        self.send_message_order(count[self.step], quantity_order, message)

    def pressed_btn_down(self, message):
        count = self.BD.select_all_product_id()
        # количество товара в заказе
        quantity_order = self.BD.select_order_quantity(count[self.step])
        # количество товара на складе
        quantity_product = self.BD.select_single_product_quantity(count[self.step])

        if quantity_order > 0:
            quantity_order -= 1
            quantity_product += 1
            # вносим в БД
            self.BD.update_order_value(count[self.step], 'quantity', quantity_order)
            self.BD.update_product_value(count[self.step], 'quantity', quantity_product)
        self.send_message_order(count[self.step], quantity_order, message)

    def pressed_btn_x(self, message):
        count = self.BD.select_all_product_id()
        if count.__len__() > 0:
            quantity_order = self.BD.select_order_quantity(count[self.step])
            quantity_product = self.BD.select_single_product_quantity(count[self.step])
            quantity_product += quantity_order
            self.BD.del_order(count[self.step])
            self.BD.update_product_value(count[self.step], 'quantity', quantity_product)
            self.step -= 1
        count = self.BD.select_all_product_id()

        if count.__len__() > 0:
            quantity_order = self.BD.select_order_quantity(count[self.step])
            self.send_message_order(count[self.step], quantity_order, message)

        else:
            self.bot.send_message(message.chat.id, MESSAGES['no_orders'],
                                  parse_mode="HTML",
                                  reply_markup=self.keybords.category_menu())

    def pressed_btn_back_step(self, message):
        if self.step > 0:
            self.step -= 1
        # получим список всех  товаров в заказе
        count = self.BD.select_all_product_id()
        quantity = self.BD.select_order_quantity(count[self.step])
        # Отправим пользователю сооющение
        self.send_message_order(count[self.step], quantity, message)


    def pressed_btn_next_step(self, message):
        if self.step < self.BD.count_rows_order()-1:
            self.step += 1

        # получим список всех  товаров в заказе
        count = self.BD.select_all_product_id()
        quantity = self.BD.select_order_quantity(count[self.step])

        # Отправим пользователю сооющение
        self.send_message_order(count[self.step], quantity, message)

    def pressed_btn_apply(self, message):
        self.bot.send_message(message.chat.id, MESSAGES['apply'].format(utility.get_total_cost(self.BD), utility.get_total_quantity(self.BD)), parse_mode="HTML", reply_markup=self.keybords.category_menu())
        self.BD.delete_all_orders()






    def handle(self):
        '''
        обработчик (декоратор) сообщений
        обрабатывает входящии сообщения от нажатия кнопок
        '''
        @self.bot.message_handler(func=lambda message: True)
        def handle(message):
            # Меню

            if message.text == config.KEYBOARD['CHOOSE_GOODS']:
                self.pressed_btn_category(message)

            if message.text == config.KEYBOARD['INFO']:
                self.pressed_btn_info(message)

            if message.text == config.KEYBOARD['SETTINGS']:
                self.pressed_btn_settings(message)

            if message.text == config.KEYBOARD['<<']:
                self.pressed_btn_back(message)

            if message.text == config.KEYBOARD['ORDER']:
                #Если есть заказ

                if self.BD.count_rows_order() > 0:
                    self.pressed_btn_order(message)
                else:
                    self.bot.send_message(message.chat.id,
                                          MESSAGES['no_orders'],
                                          parse_mode="HTML",
                                          reply_markup=self.keybords.category_menu())



            # меню (категории товаров)

            if message.text == config.KEYBOARD['SEMIPRODUCT']:
                self.pressed_btn_product(message, 'SEMIPRODUCT')

            if message.text == config.KEYBOARD['GROCERY']:
                self.pressed_btn_product(message, 'GROCERY')

            if message.text == config.KEYBOARD['ICE_CREAM']:
                self.pressed_btn_product(message, 'ICE_CREAM')

            # Меню заказа

            if message.text == config.KEYBOARD['UP']:
                self.pressed_btn_up(message)

            if message.text == config.KEYBOARD['DOWN']:
                self.pressed_btn_down(message)

            if message.text == config.KEYBOARD['X']:
                self.pressed_btn_x(message)

            if message.text == config.KEYBOARD['BACK_STEP']:
                self.pressed_btn_back_step(message)


            if message.text == config.KEYBOARD['NEXT_STEP']:
                self.pressed_btn_next_step(message)

            if message.text == config.KEYBOARD['APPLY']:
                self.pressed_btn_apply(message)
            else: self.bot.send_message(message.chat.id, message.text)
