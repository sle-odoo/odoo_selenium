# -*- coding: utf-8 -*-

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from WebClient import WebClient


class Login(object):

    def __init__(self, driver, instance_url):
        self.driver = driver
        self.instance_url = instance_url

    def login(self, login, password):
        wait = WebDriverWait(self.driver, 10)
        self.driver.get(self.instance_url)
        wait.until(
            expected_conditions.presence_of_element_located((By.NAME, "login"))
        )

        assert self.driver.title == "Odoo"
        assert self.driver.current_url.endswith("/web/login")

        self.driver.find_element_by_name("login").send_keys(login)
        self.driver.find_element_by_name("password").send_keys(password)
        self.driver.find_element_by_name("password").submit()

        wait.until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, "o_web_client"))
        )

        wait.until(
            expected_conditions.invisibility_of_element_located((By.CLASS_NAME, "o_loading"))
        )

        return WebClient(self.driver)
