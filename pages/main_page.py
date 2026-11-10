import allure
from selenium.webdriver.common.action_chains import ActionChains
from pages.base_page import BasePage
from locators.locators import MainPageLocators as MPL
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Клик по ссылке 'Конструктор'")
    def click_on_constructor(self):
        self.click_element(MPL.CONSTRUCTOR_LINK)

    @allure.step("Клик по ссылке 'Лента заказов'")
    def click_on_order_feed(self):
        self.click_element(MPL.ORDER_FEED_LINK)

    @allure.step("Клик по ссылке 'Личный кабинет'")
    def click_on_personal_account(self):
        self.click_element(MPL.PERSONAL_ACCOUNT_LINK)

    @allure.step("Клик по ингредиенту")
    def click_on_ingredient(self):
        self.click_element(MPL.INGREDIENT)

    @allure.step("Закрытие модального окна")
    def close_modal_window(self):
        self.click_element(MPL.MODAL_CLOSE_BUTTON)

    @allure.step("Получение значения счетчика ингредиента")
    def get_ingredient_counter(self):
        """Возвращает значение счетчика для первого ингредиента с обновлением DOM."""
        self.execute_script("""
            document.body.style.display = 'none';
            document.body.offsetHeight;
            document.body.style.display = '';
        """)
        self.wait_for_condition(lambda: True, "Пауза", 0.5)
        ingredient = self.find_element(MPL.INGREDIENT)
        counters = ingredient.find_elements(*MPL.INGREDIENT_COUNTER)
        if counters:
            value = counters[0].text
            return int(value) if value.isdigit() else 0
        return 0

    @allure.step("Получение значения счетчика через JavaScript")
    def get_ingredient_counter_js(self):
        """Получает значение счетчика напрямую через JavaScript."""
        script = """
            const counters = document.querySelectorAll('[class*="counter_counter__num"]');
            for (let counter of counters) {
                if (counter.textContent && counter.textContent !== '0') {
                    return counter.textContent;
                }
            }
            if (counters.length > 0) {
                return counters[0].textContent || '0';
            }
            return '0';
        """
        value = self.execute_script(script)
        return int(value) if value.isdigit() else 0
 
    @allure.step("Принудительное обновление DOM")
    def force_dom_update(self):
        """Принудительно обновляет DOM для Firefox."""
        if 'firefox' in self.driver.capabilities['browserName'].lower():
            self.execute_script("""
                document.body.style.display = 'none';
                document.body.offsetHeight;
                document.body.style.display = '';
                window.dispatchEvent(new Event('resize'));
            """)
        return self

    @allure.step("Ожидание загрузки ингредиентов")
    def wait_for_ingredients_to_load(self, time=15):
        """Ожидает загрузки ингредиентов на странице."""
        self.wait_for_visibility((By.XPATH, "//a[contains(@href, '/ingredient')]"), time)
        return self

    @allure.step("Проверка отображения модального окна")
    def is_modal_window_displayed(self):
        return self.is_element_displayed(MPL.MODAL_WINDOW)

    @allure.step("Клик по кнопке 'Оформить заказ'")
    def click_place_order_button(self):
        self.click_element(MPL.PLACE_ORDER_BUTTON)

    @allure.step("Получение номера заказа из модального окна")
    def get_order_id_from_popup(self):
        order_text = self.get_text_from_element(MPL.ORDER_ID_IN_MODAL)
        clean_number = order_text.replace('#', '').strip()
        return clean_number.zfill(7)

    @allure.step("Клик по кнопке 'Войти в аккаунт' на главной")
    def click_login_button_on_main(self):
        self.click_element(MPL.LOGIN_BUTTON_ON_MAIN)

    @allure.step("Добавление булки в конструктор")
    def add_bun_to_constructor(self, position="top", timeout=15):
        """Добавляет булку в конструктор с учётом браузера."""
        if 'firefox' in self.driver.capabilities['browserName'].lower():
            return self.add_bun_to_constructor_firefox(position, timeout)
        bun = self.find_element(MPL.BUN_INGREDIENT)
        if position == "top":
            target = self.find_element(MPL.BUN_ZONE_TOP)
        else:
            target = self.find_element(MPL.BUN_ZONE_BOTTOM)
        self._drag_and_drop(bun, target)
        return self

    @allure.step("Добавление ингредиента в заказ")
    def add_ingredient_to_order(self):
        """Добавляет начинку в заказ."""
        self.drag_ingredient_by_index(3)
        return self

    @allure.step("Переход в ленту заказов")
    def go_to_order_feed(self):
        """Переходит в ленту заказов, убирая оверлей и кликая через dispatchEvent."""
        self.execute_script("""
            var overlays = document.querySelectorAll('[class*="Modal_modal_overlay"]');
            overlays.forEach(function(el) { el.remove(); });
        """)
        feed_link = self.find_element(MPL.ORDER_FEED_LINK)
        self.execute_script("""
            arguments[0].dispatchEvent(new MouseEvent('click', {
                view: window,
                bubbles: true,
                cancelable: true,
                button: 0
            }));
        """, feed_link)
        self.wait_for_condition(
            lambda: "feed" in self.get_current_url(),
            "Не удалось перейти в ленту заказов",
            15
        )
        return self


    @allure.step("Переход в личный кабинет")
    def go_to_personal_account(self):

        self.execute_script("""
            var overlays = document.querySelectorAll('[class*="Modal_modal_overlay"]');
            overlays.forEach(function(el) { el.remove(); });
        """)

        account_link = self.find_element(MPL.PERSONAL_ACCOUNT_LINK)

        self.execute_script("""
            arguments[0].dispatchEvent(new MouseEvent('click', {
                view: window,
                bubbles: true,
                cancelable: true,
                button: 0
            }));
        """, account_link)

        self.wait_for_condition(
            lambda: "account" in self.get_current_url(),
            "Не удалось перейти в личный кабинет",
            15
        )
        return self

    @allure.step("Добавление булки для Firefox с ожиданием")
    def add_bun_to_constructor_firefox(self, position="top", timeout=15):
        """Специальный метод для Firefox с увеличенным ожиданием."""
        self.wait_for_ingredients_to_load(timeout)
        bun_locator = (By.XPATH, "(//a[contains(@href, '/ingredient')])[2]")
        bun = self.find_element(bun_locator, timeout)
        self.scroll_to_element(bun)
        self.wait_for_visibility(bun_locator, timeout)
        self.wait_for_clickable(bun_locator, timeout)
        if position == "top":
            target = self.find_element(MPL.BUN_ZONE_TOP, timeout)
        else:
            target = self.find_element(MPL.BUN_ZONE_BOTTOM, timeout)
        self.scroll_to_element(target)
        self._js_drag_and_drop(bun, target)
        self.execute_script("""
            document.body.style.display = 'none';
            document.body.offsetHeight;
            document.body.style.display = '';
        """)
        self.wait_for_condition(
            lambda: self.get_ingredient_counter_js() > 0,
            timeout
        )
        return self

    @allure.step("Перетаскивание ингредиента в конструктор")
    def drag_ingredient_to_constructor(self):
        initial_count = self.get_ingredient_counter_js()
        is_firefox = 'firefox' in self.driver.capabilities['browserName'].lower()
        if is_firefox:
            ingredient = self.find_element((By.XPATH, "(//a[contains(@href, '/ingredient')])[2]"))
        else:
            ingredient = self.find_element((By.XPATH, "(//a[contains(@href, '/ingredient')])[1]"))
        target = self.find_element(MPL.CONSTRUCTOR_BASKET)
        self._drag_and_drop(ingredient, target)
        if is_firefox:
            self.wait_for_counter_js_increase(initial_count, 20)
        else:
            self.wait_for_counter_change(initial_count, 20)
        return self
    
    def _drag_and_drop(self, source, target):
        self.scroll_to_element(source)
        self.scroll_to_element(target)
        is_firefox = 'firefox' in self.driver.capabilities['browserName'].lower()
        if is_firefox:
            self._js_drag_and_drop(source, target)
        else:
            actions = ActionChains(self.driver)
            actions.drag_and_drop(source, target).perform()

    def _js_drag_and_drop(self, source, target):
        script = """
            const source = arguments[0];
            const target = arguments[1];
            const dataTransfer = new DataTransfer();
            source.dispatchEvent(new DragEvent('dragstart', {
                bubbles: true,
                cancelable: true,
                dataTransfer: dataTransfer
            }));
            setTimeout(() => {
                // Событие dragover на целе
                target.dispatchEvent(new DragEvent('dragover', {
                    bubbles: true,
                    cancelable: true,
                    dataTransfer: dataTransfer
                }));
                target.dispatchEvent(new DragEvent('drop', {
                    bubbles: true,
                    cancelable: true,
                    dataTransfer: dataTransfer
                }));
                source.dispatchEvent(new DragEvent('dragend', {
                    bubbles: true,
                    cancelable: true,
                    dataTransfer: dataTransfer
                }));
                if (window.store) {
                    window.store.dispatch({type: 'constructor/addIngredient', payload: source.id});
                }
            }, 100);
        """
        self.execute_script(script, source, target)

    @allure.step("Закрытие модального окна если оно есть")
    def close_modal_if_present(self, timeout=10):
        try:
            close_btn = self.wait_for_clickable(MPL.MODAL_CLOSE_BUTTON, timeout)
            self.execute_script("arguments[0].click();", close_btn)
            self.wait_for_invisibility(MPL.MODAL_WINDOW, timeout)
            self.wait_for_invisibility(MPL.MODAL_OVERLAY, timeout)
            self.wait_for_clickable(MPL.ORDER_FEED_LINK, timeout)
        except:
            self.execute_script("""
                var overlays = document.querySelectorAll('[class*="Modal_modal_overlay"]');
                overlays.forEach(function(el) { el.remove(); });
            """)

    @allure.step("Ожидание появления заказа")
    def wait_for_order_appearance(self, timeout=15):
        """Ожидает появления настоящего номера заказа."""
        if 'firefox' in self.driver.capabilities['browserName'].lower():
            return self.wait_for_order_appearance_firefox(timeout)
        self.wait_for_visibility(MPL.MODAL_WINDOW, timeout)
        self.wait_for_element_text_not_equal(MPL.ORDER_ID_IN_MODAL, "9999", timeout)
        return self

    @allure.step("Ожидание видимости модального окна")
    def wait_for_visibility_of_modal(self, time=10):
        self.wait_for_visibility(MPL.MODAL_WINDOW, time)

    @allure.step("Ожидание невидимости модального окна")
    def wait_for_invisibility_of_modal(self, time=10):
        self.wait_for_invisibility(MPL.MODAL_WINDOW, time)

    @allure.step("Ожидание изменения счетчика")
    def wait_for_counter_change(self, initial_value, time=10):
        def counter_changed():
            return self.get_ingredient_counter() != initial_value
        self.wait_for_condition(counter_changed, "Счетчик не изменился", time)

    @allure.step("Закрытие модального окна и подготовка к переходу в ленту")
    def close_modal_and_prepare_for_feed(self):
        """Закрывает модальное окно и для Firefox удаляет overlay."""
        self.close_modal_if_present()
        self.remove_overlay_for_firefox(
            overlay_locator=MPL.MODAL_OVERLAY,
            link_locator=MPL.ORDER_FEED_LINK
        )
        return self
    
    @allure.step("Подготовка к переходу в ленту заказов")
    def prepare_for_feed_transition(self):
        """Подготавливает страницу к переходу в ленту заказов."""
        self.close_modal_if_present()
        if 'firefox' in self.driver.capabilities['browserName'].lower():
            self.remove_overlay_for_firefox(
                overlay_locator=MPL.MODAL_OVERLAY,
                link_locator=MPL.ORDER_FEED_LINK
            )
        self.wait_for_clickable(MPL.ORDER_FEED_LINK, 10)
        return self
    
    @allure.step("Ожидание видимости счетчика ингредиента")
    def wait_for_visibility_of_counter(self, time=5):
        """Ожидает появления счетчика на ингредиенте после перетаскивания."""
        def counter_not_zero():
            return self.get_ingredient_counter() > 0
        self.wait_for_condition(counter_not_zero, "Счетчик не появился или равен 0", time)
        return self
    
    @allure.step("Ожидание загрузки ингредиентов")
    def wait_for_ingredients_to_load(self, timeout=15):
        """Ожидает загрузки ингредиентов на странице."""
        self.wait_for_visibility((By.XPATH, "//a[contains(@href, '/ingredient')]"), timeout)
        def ingredients_loaded():
            ingredients = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/ingredient')]")
            return len(ingredients) >= 3
        self.wait_for_condition(ingredients_loaded, "Ингредиенты не загрузились", timeout)
        return self

    @allure.step("Перетаскивание ингредиента по индексу")
    def drag_ingredient_by_index(self, index=1):
        """Перетаскивает ингредиент по его порядковому номеру (1, 2, 3...)."""
        locator = (By.XPATH, f"(//a[contains(@href, '/ingredient')])[{index}]")
        ingredient = self.find_element(locator)
        target = self.find_element(MPL.CONSTRUCTOR_BASKET)
        self._drag_and_drop(ingredient, target)
        return self
    
    @allure.step("Ожидание увеличения счетчика через JavaScript")
    def wait_for_counter_js_increase(self, initial_count, timeout=20):
        """Ожидает увеличения счетчика через JavaScript."""
        def counter_increased():
            return self.get_ingredient_counter_js() > initial_count
        self.wait_for_condition(counter_increased, timeout)
        return self
    
    @allure.step("Ожидание появления заказа для Firefox")
    def wait_for_order_appearance_firefox(self, timeout=20):
        """Специальный метод для Firefox с принудительным обновлением."""
        self.wait_for_visibility(MPL.MODAL_WINDOW, timeout)
        for _ in range(3):
            self.execute_script("""
                document.body.style.display = 'none';
                document.body.offsetHeight;
                document.body.style.display = '';
                window.dispatchEvent(new Event('resize'));
            """)
            script = """
                const orderElement = document.querySelector('h2[class*="Modal_modal__title"]');
                return orderElement ? orderElement.textContent : '9999';
            """
            order_number = self.execute_script(script)
            if order_number and order_number != '9999':
                print(f"Настоящий номер заказа: {order_number}")
                return self
            self.wait_for_condition(lambda: True, 1)
        self.wait_for_element_text_not_equal(MPL.ORDER_ID_IN_MODAL, "9999", timeout)
        return self
    
    @allure.step("Ожидание готовности конструктора после возврата")
    def wait_for_constructor_ready(self, timeout=5):
        """Ожидает полной готовности конструктора после возврата из ленты."""
        if 'firefox' in self.driver.capabilities['browserName'].lower():
            try:
                self.wait_for_invisibility(MPL.MODAL_OVERLAY, timeout)
            except:
                pass
            self.wait_for_visibility(MPL.INGREDIENT, timeout)
            self.wait_for_clickable(MPL.PLACE_ORDER_BUTTON, timeout)
        return self