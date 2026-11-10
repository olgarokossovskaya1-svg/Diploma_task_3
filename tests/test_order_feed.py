import allure
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.order_feed_page import OrderFeedPage

@allure.feature("Лента заказов")
class TestOrderFeed:
    @allure.title("Клик на заказ открывает всплывающее окно с деталями")
    def test_order_modal_appears(self, driver, registered_user):
        main_page = MainPage(driver)
        main_page.click_login_button_on_main()
        LoginPage(driver).login(registered_user['email'], registered_user['password'])
        main_page = MainPage(driver)
        main_page.add_bun_to_constructor("top")
        main_page.add_ingredient_to_order() 
        main_page.click_place_order_button()
        main_page.wait_for_order_appearance()
        main_page.close_modal_if_present()
        main_page.go_to_order_feed() 
        order_feed_page = OrderFeedPage(driver)
        order_feed_page.wait_for_order_item_visible()
        order_feed_page.click_on_order()
        order_feed_page.wait_for_order_modal_visible()
        assert order_feed_page.is_order_modal_displayed()

    @allure.title("Заказы пользователя из раздела 'История заказов' отображаются на странице 'Лента заказов'")
    def test_user_orders_in_feed(self, driver, registered_user):
        main_page = MainPage(driver)
        main_page.click_login_button_on_main()
        LoginPage(driver).login(registered_user['email'], registered_user['password'])
        main_page = MainPage(driver)
        main_page.add_bun_to_constructor("top")
        main_page.add_ingredient_to_order() 
        main_page.click_place_order_button()
        main_page.wait_for_order_appearance()
        order_id = main_page.get_order_id_from_popup()
        main_page.close_modal_if_present()
        main_page.go_to_order_feed()
        order_feed_page = OrderFeedPage(driver)
        order_feed_page.wait_for_visibility_of_order_numbers()
        orders = order_feed_page.get_all_orders_numbers()
        assert order_id.lstrip('0') in [o.lstrip('0') for o in orders], (f"Заказ {order_id} не найден в ленте: {orders}")

    @allure.title("При создании нового заказа счётчик 'Выполнено за всё время' увеличивается")
    def test_completed_all_time_counter_increases(self, driver, registered_user):
        main_page = MainPage(driver)
        main_page.click_login_button_on_main()
        LoginPage(driver).login(registered_user['email'], registered_user['password'])

        main_page.go_to_order_feed()
        order_feed_page = OrderFeedPage(driver)
        counter_before = order_feed_page.get_completed_counter_all_time()

        main_page.click_on_constructor()
        main_page.wait_for_constructor_ready()
        main_page.add_bun_to_constructor("top")
        main_page.add_ingredient_to_order()
        main_page.click_place_order_button()
        main_page.wait_for_order_appearance()
        main_page.close_modal_if_present()

        main_page.go_to_order_feed()
        counter_after = order_feed_page.get_completed_counter_all_time()

        assert counter_after > counter_before, (
            f"Счётчик 'за всё время' не увеличился: было {counter_before}, стало {counter_after}"
        )


    @allure.title("При создании нового заказа счётчик 'Выполнено за сегодня' увеличивается")
    def test_completed_today_counter_increases(self, driver, registered_user):
        main_page = MainPage(driver)
        main_page.click_login_button_on_main()
        LoginPage(driver).login(registered_user['email'], registered_user['password'])

        main_page.go_to_order_feed()
        order_feed_page = OrderFeedPage(driver)
        counter_before = order_feed_page.get_completed_counter_today()

        main_page.click_on_constructor()
        main_page.wait_for_constructor_ready()
        main_page.add_bun_to_constructor("top")
        main_page.add_ingredient_to_order()
        main_page.click_place_order_button()
        main_page.wait_for_order_appearance()
        main_page.close_modal_if_present()

        main_page.go_to_order_feed()
        counter_after = order_feed_page.get_completed_counter_today()

        assert counter_after > counter_before, (
            f"Счётчик 'за сегодня' не увеличился: было {counter_before}, стало {counter_after}"
        )

    @allure.title("После оформления заказа его номер появляется в разделе 'В работе'")
    def test_order_number_appears_in_work(self, driver, registered_user):
        main_page = MainPage(driver)
        main_page.click_login_button_on_main()
        LoginPage(driver).login(registered_user['email'], registered_user['password'])
        main_page = MainPage(driver)
        main_page.add_bun_to_constructor("top")
        main_page.add_ingredient_to_order() 
        main_page.click_place_order_button()
        main_page.wait_for_order_appearance()
        order_id = main_page.get_order_id_from_popup()
        main_page.close_modal_if_present()
        main_page.go_to_order_feed()
        order_feed_page = OrderFeedPage(driver)
        order_feed_page.wait_for_orders_in_work()
        orders_in_work = order_feed_page.get_orders_in_work()
        assert order_id.lstrip('0') in [o.lstrip('0') for o in orders_in_work], (f"Заказ {order_id} не найден в 'В работе': {orders_in_work}")