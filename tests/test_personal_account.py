import allure
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.personal_account_page import PersonalAccountPage

@allure.feature("Личный кабинет")
class TestPersonalAccount:
    @allure.title("Переход в личный кабинет по клику на кнопку")
    def test_go_to_personal_account(self, driver, registered_user):
        main_page = MainPage(driver)
        main_page.click_login_button_on_main()
        LoginPage(driver).login(registered_user['email'], registered_user['password'])
        main_page = MainPage(driver)
        main_page.go_to_personal_account()
        account_page = PersonalAccountPage(driver)
        account_page.wait_for_page_stability()
        assert account_page.is_profile_page_displayed()

    @allure.title("Переход в раздел 'История заказов'")
    def test_go_to_order_history(self, driver, registered_user):
        main_page = MainPage(driver)
        main_page.click_login_button_on_main()
        LoginPage(driver).login(registered_user['email'], registered_user['password'])
        main_page = MainPage(driver)
        main_page.go_to_personal_account()
        account_page = PersonalAccountPage(driver)
        account_page.wait_for_page_stability()
        account_page.wait_for_clickable_order_history()
        account_page.click_order_history_link()
        assert "order-history" in account_page.get_current_url()

    @allure.title("Выход из аккаунта")
    def test_logout_from_account(self, driver, registered_user):
        main_page = MainPage(driver)
        main_page.click_login_button_on_main()
        LoginPage(driver).login(registered_user['email'], registered_user['password'])
        main_page = MainPage(driver)
        main_page.go_to_personal_account()
        account_page = PersonalAccountPage(driver)
        account_page.wait_for_page_stability()
        account_page.wait_for_clickable_logout_button()
        account_page.click_logout_button()
        login_page = LoginPage(driver)
        login_page.wait_for_login_button()
        assert login_page.is_login_button_displayed()