import allure
from pages.base_page import BasePage
from locators.locators import OrderFeedPageLocators as OFPL

class OrderFeedPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Клик по заказу")
    def click_on_order(self):
        self.click_element(OFPL.ORDER_ITEM)

    @allure.step("Проверка отображения модального окна заказа")
    def is_order_modal_displayed(self):
        return self.is_element_displayed(OFPL.ORDER_MODAL)

    @allure.step("Получение всех номеров заказов из ленты")
    def get_all_orders_numbers(self):
        elements = self.driver.find_elements(*OFPL.ORDER_NUMBERS)
        numbers = []
        for el in elements:
            text = el.text.strip()
            if text and text.replace('#', '').strip().isdigit():
                clean_text = text.replace('#', '').strip()
                numbers.append(clean_text)
        return numbers

    @allure.step("Получение счетчика 'Выполнено за всё время'")
    def get_completed_counter_all_time(self, timeout=20):
        self.wait_for_visibility(OFPL.COMPLETED_ALL_TIME_COUNTER, timeout)
        return int(self.get_text_from_element(OFPL.COMPLETED_ALL_TIME_COUNTER))

    @allure.step("Получение счетчика 'Выполнено за сегодня'")
    def get_completed_counter_today(self, timeout=20):
        self.wait_for_visibility(OFPL.COMPLETED_TODAY_COUNTER, timeout)
        return int(self.get_text_from_element(OFPL.COMPLETED_TODAY_COUNTER))

    @allure.step("Получение списка заказов в работе")
    def get_orders_in_work(self):
        elements = self.driver.find_elements(*OFPL.ORDERS_IN_WORK_LIST)
        orders = []
        for el in elements:
            text = el.text.strip()
            if text and text != "Все текущие заказы готовы!":
                orders.append(text)
        return orders

    @allure.step("Ожидание появления заказов в разделе 'В работе'")
    def wait_for_orders_in_work(self, timeout=15):
        def orders_not_empty():
            orders = self.get_orders_in_work()
            return len(orders) > 0
        self.wait_for_condition(orders_not_empty, "Заказы не появились в работе", timeout)

    @allure.step("Ожидание видимости номеров заказов")
    def wait_for_visibility_of_order_numbers(self, time=10):
        self.wait_for_visibility(OFPL.ORDER_NUMBERS, time)

    @allure.step("Ожидание изменения счетчика 'за всё время'")
    def wait_for_counter_all_time_change(self, initial_value, time=10):
        def counter_changed():
            return self.get_completed_counter_all_time() != initial_value
        self.wait_for_condition(counter_changed, "Счетчик 'за всё время' не изменился", time)

    @allure.step("Ожидание изменения счетчика 'за сегодня'")
    def wait_for_counter_today_change(self, initial_value, time=10):
        def counter_changed():
            return self.get_completed_counter_today() != initial_value
        self.wait_for_condition(counter_changed, "Счетчик 'за сегодня' не изменился", time)
    
    @allure.step("Ожидание видимости заказа в ленте")
    def wait_for_order_item_visible(self, timeout=15):
        """Ожидает появления заказа в ленте."""
        self.wait_for_visibility(OFPL.ORDER_ITEM, timeout)
        return self

    @allure.step("Ожидание видимости модального окна заказа")
    def wait_for_order_modal_visible(self, timeout=15):
        """Ожидает появления модального окна заказа."""
        self.wait_for_visibility(OFPL.ORDER_MODAL, timeout)
        return self