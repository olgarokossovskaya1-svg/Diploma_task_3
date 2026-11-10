from selenium.webdriver.common.by import By

class MainPageLocators:
    CONSTRUCTOR_LINK = (By.XPATH, "//a[contains(@href, '/')]")
    ORDER_FEED_LINK = (By.XPATH, "//a[contains(@href, '/feed')]")
    PERSONAL_ACCOUNT_LINK = (By.XPATH, "//a[@href='/account']")
    INGREDIENT = (By.XPATH, "(//a[contains(@href, '/ingredient')])[1]")
    INGREDIENT_COUNTER = (By.XPATH, ".//p[contains(@class, 'counter_counter__num__3nue1')]")
    MODAL_WINDOW = (By.XPATH, "//section[contains(@class, 'Modal_modal_opened__3ISw4')]")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//button[contains(@class, 'Modal_modal__close__TnseK')]")
    PLACE_ORDER_BUTTON = (By.XPATH, "//button[text()='Оформить заказ']")
    ORDER_ID_IN_MODAL = (By.XPATH, "//h2[contains(@class, 'Modal_modal__title__2L34m')]")
    LOGIN_BUTTON_ON_MAIN = (By.XPATH, "//button[text()='Войти в аккаунт']")
    CONSTRUCTOR_BASKET = (By.XPATH, "//section[contains(@class, 'mt-25')]")
    BUN_ZONE_TOP = (By.XPATH, "//*[contains(text(),'Перетяните булочку сюда (верх)')]/..")
    BUN_ZONE_BOTTOM = (By.XPATH, "//*[contains(text(),'Перетяните булочку сюда (низ)')]/..")
    BUN_INGREDIENT = (By.XPATH, "(//a[contains(@href, '/ingredient')])[1]")
    MEAT_INGREDIENT = (By.XPATH, "(//a[contains(@href, '/ingredient')])[10]")
    MODAL_OVERLAY = (By.XPATH, "//div[contains(@class, 'Modal_modal_overlay__x2ZCr')]")  
class LoginPageLocators:
    EMAIL_INPUT = (By.XPATH, "//input[@name='name']")  
    PASSWORD_INPUT = (By.XPATH, "//input[@name='Пароль']")  
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти']")  
    RECOVERY_PASSWORD_LINK = (By.XPATH, "//a[text()='Восстановить пароль']") 
    PERSONAL_ACCOUNT_LINK = (By.XPATH, "//a[@href='/account']") 

class RecoveryPageLocators:
    EMAIL_INPUT = (By.XPATH, "//input[@name='name']")  
    RECOVERY_BUTTON = (By.XPATH, "//button[text()='Восстановить']")  
    SHOW_HIDE_PASSWORD_BUTTON = (By.XPATH, "//div[contains(@class, 'input__icon-action')]")  
    PASSWORD_INPUT = (By.XPATH, "//input[contains(@class, 'input__textfield')]")  
    RESET_PASSWORD_BUTTON = (By.XPATH, "//button[text()='Сохранить']")  

class PersonalAccountPageLocators:
    ORDER_HISTORY_LINK = (By.XPATH, "//a[text()='История заказов']")  
    LOGOUT_BUTTON = (By.XPATH, "//button[text()='Выход']")  
    PROFILE_LINK = (By.XPATH, "//a[text()='Профиль']")
    MODAL_OVERLAY = (By.XPATH, "//div[contains(@class, 'Modal_modal_overlay__x2ZCr')]")  
    CONSTRUCTOR_LINK = (By.XPATH, "//a[@href='/']")

class OrderFeedPageLocators:
    ORDER_ITEM = (By.XPATH, "(//li[contains(@class, 'OrderHistory_listItem__2x95r')])[1]")  
    ORDER_MODAL = (By.XPATH, "//section[contains(@class, 'Modal_modal_opened__3ISw4')]")  
    ORDER_NUMBERS = (By.XPATH, "//li[contains(@class, 'mb-2')]")  
    COMPLETED_ALL_TIME_COUNTER = (By.XPATH, "//p[contains(text(), 'Выполнено за все время')]/following-sibling::p[contains(@class, 'OrderFeed_number')]")  
    COMPLETED_TODAY_COUNTER = (By.XPATH, "//p[contains(text(), 'Выполнено за сегодня')]/following-sibling::p[contains(@class, 'OrderFeed_number')]")  
    ORDERS_IN_WORK_LIST = (By.XPATH, "//ul[contains(@class, 'OrderFeed_orderListReady__1YFem')]/li")  
    MODAL_CLOSE_BUTTON = (By.XPATH, "//button[contains(@class, 'Modal_modal__close__TnseK')]")  
    MODAL_OVERLAY = (By.XPATH, "//div[contains(@class, 'Modal_modal_overlay__x2ZCr')]")  
    FEED_LINK = (By.XPATH, "//a[@href='/feed']")