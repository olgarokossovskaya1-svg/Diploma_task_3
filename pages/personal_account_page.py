import allure
from pages.base_page import BasePage
from locators.locators import PersonalAccountPageLocators as PAPL

class PersonalAccountPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Клик по ссылке 'История заказов'")
    def click_order_history_link(self):
        self.click_element(PAPL.ORDER_HISTORY_LINK)

    @allure.step("Клик по кнопке 'Выход'")
    def click_logout_button(self):
        self.click_element(PAPL.LOGOUT_BUTTON)

    @allure.step("Проверка отображения страницы профиля")
    def is_profile_page_displayed(self):
        return self.is_element_displayed(PAPL.PROFILE_LINK)
    
    @allure.step("Ожидание стабильности страницы")
    def wait_for_page_stability(self, time=5):
        """Ожидает исчезновения overlay на странице личного кабинета."""
        try:
            self.wait_for_invisibility(PAPL.MODAL_OVERLAY, time)
        except:
            pass
        return self

    @allure.step("Ожидание кликабельности кнопки выхода")
    def wait_for_clickable_logout_button(self, time=10):
        self.wait_for_clickable(PAPL.LOGOUT_BUTTON, time)

    @allure.step("Ожидание кликабельности ссылки 'История заказов'")
    def wait_for_clickable_order_history(self, time=10):
        self.wait_for_clickable(PAPL.ORDER_HISTORY_LINK, time)

    @allure.step("Подготовка к клику (ожидание стабильности и удаление overlay)")
    def prepare_for_click(self, link_locator):
        """Подготавливает страницу к клику."""
        self.wait_for_page_stability()
        self.remove_overlay_for_firefox(link_locator)
        self.wait_for_clickable(link_locator, 10)
        return self 
    
    @allure.step("Подготовка к клику (с учетом Firefox)")
    def prepare_for_click(self, link_locator):
        """Подготавливает страницу к клику: убирает overlay для Firefox."""
        self.wait_for_page_stability()
        self.remove_overlay_for_firefox(link_locator)
        return self
    
    @allure.step("Ожидание и клик по кнопке выхода")
    def wait_and_click_logout(self):
        """Ожидает стабильности страницы и кликает по кнопке выхода."""
        self.wait_for_page_stability()
        self.wait_for_clickable(PAPL.LOGOUT_BUTTON, 15)
        self.click_logout_button()


    @allure.step("Подготовка к клику по кнопке выхода")
    def prepare_for_logout(self):
        """Подготавливает страницу к выходу из аккаунта."""
        self.wait_for_page_stability()
        self.remove_overlay_for_firefox(
            overlay_locator=PAPL.MODAL_OVERLAY,
            link_locator=PAPL.LOGOUT_BUTTON
        )
        return self    
    
    @allure.step("Подготовка к переходу в личный кабинет")
    def prepare_for_account_entry(self):
        """Подготавливает страницу к переходу в личный кабинет."""
        self.wait_for_page_stability()
        if 'firefox' in self.driver.capabilities['browserName'].lower():
            self.remove_overlay_for_firefox(
                overlay_locator=PAPL.MODAL_OVERLAY,
                link_locator=PAPL.PROFILE_LINK
            )
        self.wait_for_clickable(PAPL.PROFILE_LINK, 10)
        return self