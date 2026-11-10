import allure
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.recovery_password_page import RecoveryPasswordPage
from data.user_data import UserData

@allure.feature("Восстановление пароля")
class TestRecoveryPassword:
    @allure.title("Переход на страницу восстановления по кнопке 'Восстановить пароль'")
    def test_go_to_recovery_page_by_link(self, driver):
        main_page = MainPage(driver)
        main_page.click_on_personal_account()
        LoginPage(driver).click_recovery_password_link()
        recovery_page = RecoveryPasswordPage(driver)
        assert recovery_page.is_recovery_button_displayed()

    @allure.title("Ввод почты и клик по кнопке 'Восстановить'")
    def test_email_input_and_recovery_click(self, driver):
        main_page = MainPage(driver)
        main_page.click_on_personal_account()
        LoginPage(driver).click_recovery_password_link()
        recovery_page = RecoveryPasswordPage(driver)
        recovery_page.enter_email_and_click_recovery(UserData.EXISTING_USER_EMAIL)
        assert recovery_page.is_password_input_displayed()

    @allure.title("Клик по кнопке показать/скрыть пароль делает поле активным")
    def test_show_hide_password_button_highlights_field(self, driver):
        main_page = MainPage(driver)
        main_page.click_on_personal_account()
        LoginPage(driver).click_recovery_password_link()
        recovery_page = RecoveryPasswordPage(driver)
        recovery_page.enter_email_and_click_recovery(UserData.EXISTING_USER_EMAIL)
        recovery_page.click_show_hide_password_button()
        recovery_page.wait_for_password_field_active() 
        assert recovery_page.is_password_field_active()