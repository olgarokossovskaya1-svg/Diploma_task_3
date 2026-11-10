import allure, time
from pages.main_page import MainPage
from pages.login_page import LoginPage
from selenium.webdriver.common.by import By
@allure.feature("Конструктор")
class TestConstructor:
    @allure.title("Переход по клику на 'Конструктор'")
    def test_go_to_constructor(self, driver):
        main_page = MainPage(driver)
        main_page.click_on_order_feed()
        main_page.click_on_constructor()
        assert main_page.is_text_present_on_page("Соберите бургер")

    @allure.title("Переход по клику на 'Лента заказов'")
    def test_go_to_order_feed(self, driver):
        main_page = MainPage(driver)
        main_page.click_on_order_feed()
        assert "feed" in main_page.get_current_url()

    @allure.title("Клик на ингредиент открывает всплывающее окно с деталями")
    def test_ingredient_modal_appears(self, driver):
        main_page = MainPage(driver)
        main_page.click_on_ingredient()
        main_page.wait_for_visibility_of_modal()
        assert main_page.is_modal_window_displayed()

    @allure.title("Всплывающее окно закрывается кликом по крестику")
    def test_modal_closes_by_cross(self, driver):
        main_page = MainPage(driver)
        main_page.click_on_ingredient()
        main_page.wait_for_visibility_of_modal()
        main_page.close_modal_window()
        main_page.wait_for_invisibility_of_modal()
        assert not main_page.is_modal_window_displayed()

    @allure.title("При добавлении ингредиента в заказ увеличивается каунтер")
    def test_ingredient_counter_increases(self, driver, registered_user):
        main_page = MainPage(driver)
        main_page.click_login_button_on_main()
        LoginPage(driver).login(registered_user['email'], registered_user['password'])
        main_page = MainPage(driver)
        initial_count = main_page.get_ingredient_counter_js()
        if 'firefox' in driver.capabilities['browserName'].lower():
            main_page.drag_ingredient_by_index(2)
            main_page.wait_for_counter_js_increase(initial_count, 15)
            new_count = main_page.get_ingredient_counter_js()
        else:
            main_page.drag_ingredient_by_index(1)
            main_page.wait_for_counter_change(initial_count, 20)
            new_count = main_page.get_ingredient_counter_js()
        assert new_count > initial_count

    @allure.title("Залогиненный пользователь может оформить заказ")
    def test_create_order_with_bun_and_meat(self, driver, registered_user):
        main_page = MainPage(driver)
        main_page.click_login_button_on_main()
        LoginPage(driver).login(registered_user['email'], registered_user['password'])
        main_page = MainPage(driver)
        main_page.wait_for_ingredients_to_load(15)
        main_page.add_bun_to_constructor("top")
        main_page.drag_ingredient_by_index(10)
        main_page.click_place_order_button()
        main_page.wait_for_order_appearance(20)
        order_id = main_page.get_order_id_from_popup()
        assert order_id.isdigit()