import allure
from pages.base_page import BasePage
from locators.locators import LoginPageLocators as LPL

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Клик по ссылке 'Восстановить пароль'")
    def click_recovery_password_link(self):
        self.click_element(LPL.RECOVERY_PASSWORD_LINK)

    @allure.step("Вход в систему с email: {email}")
    def login(self, email, password):
        self.send_keys_to_element(LPL.EMAIL_INPUT, email)
        self.send_keys_to_element(LPL.PASSWORD_INPUT, password)
        self.click_element(LPL.LOGIN_BUTTON)
        self.wait_for_condition(
        lambda: "login" not in self.get_current_url(),
        "Не удалось войти в аккаунт: остались на странице логина",15)

    @allure.step("Проверка отображения кнопки входа")
    def is_login_button_displayed(self):
        return self.is_element_displayed(LPL.LOGIN_BUTTON)
    
    @allure.step("Ожидание видимости кнопки входа")
    def wait_for_visibility_of_login_button(self, time=10):
        self.wait_for_visibility(LPL.LOGIN_BUTTON, time)

    @allure.step("Ожидание кнопки входа")
    def wait_for_login_button(self, timeout=10):
        """Ожидает появления кнопки входа."""
        self.wait_for_visibility(LPL.LOGIN_BUTTON, timeout)
        return self    