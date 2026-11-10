import allure
from pages.base_page import BasePage
from locators.locators import RecoveryPageLocators as RPL
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

class RecoveryPasswordPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Ввод email и клик по кнопке 'Восстановить'")
    def enter_email_and_click_recovery(self, email):
        self.send_keys_to_element(RPL.EMAIL_INPUT, email)
        self.click_element(RPL.RECOVERY_BUTTON)
        self.wait_for_visibility(RPL.PASSWORD_INPUT)

    @allure.step("Клик по кнопке показать/скрыть пароль")
    def click_show_hide_password_button(self):
        """Кликает по кнопке, убирая оверлей и используя dispatchEvent."""
        # 1. Удаляем оверлеи
        self.execute_script("""
            var overlays = document.querySelectorAll('[class*="Modal_modal_overlay"]');
            overlays.forEach(function(el) { el.remove(); });
        """)
        # 2. Находим элемент через Selenium (работает с XPath)
        button = self.find_element(RPL.SHOW_HIDE_PASSWORD_BUTTON)
        # 3. Кликаем через JS dispatchEvent (триггерит React)
        self.execute_script("""
            arguments[0].dispatchEvent(new MouseEvent('click', {
                view: window,
                bubbles: true,
                cancelable: true,
                button: 0
            }));
        """, button)

    @allure.step("Проверка активности поля пароля")
    def is_password_field_active(self):
        """Проверяет, что поле пароля активно (подсвечено)."""
        try:
            password_field = self.find_element(RPL.PASSWORD_INPUT, 3)
            field_type = password_field.get_attribute("type")
            return field_type == "text"
        except:
            return False

    @allure.step("Ожидание активности поля пароля")
    def wait_for_password_field_active(self, time=5):
        """Ожидает, что поле пароля станет активным (тип изменится на text)."""
        def field_active():
            return self.is_password_field_active()
        self.wait_for_condition(field_active, "Поле пароля не стало активным", time)
        
    @allure.step("Проверка отображения кнопки восстановления")
    def is_recovery_button_displayed(self):
        return self.is_element_displayed(RPL.RECOVERY_BUTTON)

    @allure.step("Проверка отображения поля пароля")
    def is_password_input_displayed(self):
        return self.is_element_displayed(RPL.PASSWORD_INPUT)

    @allure.step("Подготовка к клику по кнопке показа пароля")
    def prepare_for_show_password(self):
        """Подготавливает страницу к клику по кнопке показа пароля."""
        self.remove_overlay_for_firefox(
            overlay_locator=RPL.MODAL_OVERLAY,
            link_locator=RPL.SHOW_HIDE_PASSWORD_BUTTON
        )
        return self    