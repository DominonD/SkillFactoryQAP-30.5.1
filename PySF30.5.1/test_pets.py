import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_show_all_pets(driver):
    driver.implicitly_wait(10)
    driver.find_element(By.ID, 'email').send_keys('vasya@mail.com')
    driver.find_element(By.ID, 'pass').send_keys('12345')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')


    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0

def test_show_my_pets(driver):
    driver.find_element(By.ID, 'email').send_keys('vasya@mail.com')
    driver.find_element(By.ID, 'pass').send_keys('12345')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    driver.get("https://petfriends.skillfactory.ru/my_pets")

    user_stat = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]')
    pet_count = user_stat.text.split("\n")[1].split()[1]

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.table tbody tr')))

    images = driver.find_elements(By.CSS_SELECTOR, '.table tbody img')
    names = driver.find_elements(By.CSS_SELECTOR, '.table tbody tr td:nth-child(2)')
    types = driver.find_elements(By.CSS_SELECTOR, '.table tbody tr td:nth-child(3)')
    ages = driver.find_elements(By.CSS_SELECTOR, '.table tbody tr td:nth-child(4)')

    has_image = 0
    has_name_age_type = True
    unique_names = set()
    unique_pets = []

    for i in range(len(names)):
        if images[i].get_attribute('src') != '':
            has_image += 1
        if names[i].text == '' or ages[i].text == '' or types[i].text == '':
            has_name_age_type = False
        unique_names.add(names[i].text)
        pet = [names[i].text, types[i].text, ages[i].text]
        while unique_pets != [1]: #Способ не записывать данные в список, если проверка уже провалена
            if pet not in unique_pets:
                unique_pets.append(pet)
            else:
                unique_pets = [1]

    assert len(names) == int(pet_count), "Not all pets in table"
    assert has_image >= int(pet_count)//2, "Less than half pets have an image"
    assert has_name_age_type, "Not all pets have name, age or type"
    assert len(unique_names) == len(names), "Not all pets have unique names"

    assert len(unique_pets) == len(names), "Not all pets are unique"
