import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from data.urls import Urls
from api.user_api import create_user, delete_user

@pytest.fixture(params=['chrome', 'firefox'])
def driver(request):
    browser = request.param
    if browser == 'chrome':
        options = ChromeOptions()
        driver = webdriver.Chrome(options=options)
    elif browser == 'firefox':
        options = FirefoxOptions()
        driver = webdriver.Firefox(options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.get(Urls.BASE_URL)
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture
def registered_user():
    user_data = create_user()
    yield user_data
    delete_user(user_data.get('accessToken'))