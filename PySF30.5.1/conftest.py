import pytest
from selenium import webdriver

@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Firefox()
    driver.get('https://petfriends.skillfactory.ru/login')

    yield driver

    driver.quit()