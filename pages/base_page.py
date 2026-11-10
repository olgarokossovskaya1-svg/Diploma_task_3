from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    @allure.step("Поиск элемента {locator}")
    def find_element(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(
            EC.presence_of_element_located(locator),
            f"Элемент {locator} не найден за {time} секунд"
        )

    @allure.step("Клик по элементу {locator}")
    def click_element(self, locator, time=10):
        element = WebDriverWait(self.driver, time).until(
            EC.element_to_be_clickable(locator),
            f"Элемент {locator} не кликабелен за {time} секунд"
        )
        element.click()

    @allure.step("Ввод текста '{text}' в элемент {locator}")
    def send_keys_to_element(self, locator, text, time=10):
        element = self.find_element(locator, time)
        element.clear()
        element.send_keys(text)

    @allure.step("Получение текста из элемента {locator}")
    def get_text_from_element(self, locator, time=10):
        return self.find_element(locator, time).text

    @allure.step("Проверка отображения элемента {locator}")
    def is_element_displayed(self, locator, time=5):
        try:
            return self.find_element(locator, time).is_displayed()
        except TimeoutException:
            return False

    @allure.step("Ожидание видимости элемента {locator}")
    def wait_for_visibility(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(
            EC.visibility_of_element_located(locator),
            f"Элемент {locator} не видим за {time} секунд"
        )

    @allure.step("Ожидание кликабельности элемента {locator}")
    def wait_for_clickable(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(
            EC.element_to_be_clickable(locator),
            f"Элемент {locator} не кликабелен за {time} секунд"
        )

    @allure.step("Ожидание невидимости элемента {locator}")
    def wait_for_invisibility(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(
            EC.invisibility_of_element_located(locator),
            f"Элемент {locator} все еще видим за {time} секунд"
        )

    @allure.step("Ожидание, что текст элемента {locator} не равен {text}")
    def wait_for_element_text_not_equal(self, locator, text, time=10):
        def text_not_equal(driver):
            element_text = self.get_text_from_element(locator, 1)
            return element_text != text
        return WebDriverWait(self.driver, time).until(
            text_not_equal,
            f"Текст элемента {locator} все еще равен '{text}' через {time} секунд"
        )

    @allure.step("Ожидание изменения значения счетчика")
    def wait_for_counter_change(self, get_counter_func, initial_value, time=10):
        def counter_changed(driver):
            return get_counter_func() != initial_value
        return WebDriverWait(self.driver, time).until(
            counter_changed,
            f"Счетчик не изменился за {time} секунд"
        )

    @allure.step("Ожидание выполнения условия")
    def wait_for_condition(self, condition_func, message, time=10):
        return WebDriverWait(self.driver, time).until(
            lambda driver: condition_func(),
            message
        )

    @allure.step("Получение атрибута {attribute} элемента {locator}")
    def get_element_attribute(self, locator, attribute, time=10):
        element = self.find_element(locator, time)
        return element.get_attribute(attribute)

    @allure.step("Проверка наличия текста на странице")
    def is_text_present_on_page(self, text):
        return text in self.driver.page_source

    @allure.step("Получение текущего URL")
    def get_current_url(self):
        return self.driver.current_url

    @allure.step("Выполнение JavaScript скрипта")
    def execute_script(self, script, *args):
        return self.driver.execute_script(script, *args)

    @allure.step("Скролл к элементу")
    def scroll_to_element(self, element):
        self.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

    @allure.step("Удаление overlay для Firefox")
    def remove_overlay_for_firefox(self, overlay_locator=None, link_locator=None, time=5):
        """
        Удаляет overlay для Firefox с использованием явных ожиданий.
        
        Args:
            overlay_locator: локатор overlay (если None, используется скрипт удаления)
            link_locator: локатор ссылки для ожидания кликабельности
            time: таймаут ожидания
        """
        if 'firefox' in self.driver.capabilities['browserName'].lower():
            self.execute_script("""
                var overlays = document.querySelectorAll('[class*="Modal_modal_overlay"]');
                overlays.forEach(function(el) { el.remove(); });
            """)
            if overlay_locator:
                try:
                    self.wait_for_invisibility(overlay_locator, time)
                except:
                    pass
            if link_locator:
                try:
                    self.wait_for_clickable(link_locator, time)
                except:
                    pass
        return self

    @allure.step("Ожидание стабильности страницы")
    def wait_for_page_stability(self, overlay_locator=None, time=5):
        if overlay_locator:
            try:
                self.wait_for_invisibility(overlay_locator, time)
            except:
                pass
        return self     

    @allure.step("Ожидание изменения атрибута элемента")
    def wait_for_attribute_change(self, locator, attribute, expected_value, time=10):
        """Ожидает изменения атрибута элемента до ожидаемого значения."""
        def attribute_changed():
            current_value = self.get_element_attribute(locator, attribute)
            return expected_value in current_value if expected_value else current_value
        return self.wait_for_condition(attribute_changed, f"Атрибут {attribute} не изменился", time)  

    @allure.step("Ожидание стабилизации страницы")
    def wait_for_page_ready(self, timeout=5):
        """Ожидает готовности страницы (все AJAX запросы завершены, DOM стабилен)."""
        
        script = """
            return document.readyState === 'complete' && 
                !window.jQuery?.active && 
                !document.querySelector('[class*="Modal_modal_overlay"]');
        """
        
        def page_ready():
            return self.execute_script(script)
        
        self.wait_for_condition(page_ready, "Страница не готова", timeout)
        return self 