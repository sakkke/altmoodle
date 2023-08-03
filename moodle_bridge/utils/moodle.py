import os
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

def login(driver: WebDriver):
    driver.get(os.getenv('MOODLE_URL') + '/login/index.php')

    username = driver.find_element(By.NAME, 'username')
    password = driver.find_element(By.NAME, 'password')
    login_button = driver.find_element(By.ID, 'loginbtn')

    username.send_keys(os.getenv('USERNAME'))
    password.send_keys(os.getenv('PASSWORD'))

    login_button.click()
