# -*- coding: utf-8 -*-

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
SHORT_WAIT = 10
MEDIUM_WAIT = 30
LONG_WAIT = 60


# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------
class PageObject(object):

    def __init__(self, driver):
        self.driver = driver


# -----------------------------------------------------------------------------
# Decorators
# -----------------------------------------------------------------------------
def wait_rpc_done(timeout=10):
    def decorator(func):
        def inner(self, *args, **kwargs):
            driver = getattr(self, "driver")

            res = func(self, *args, **kwargs)

            wait = WebDriverWait(driver, timeout)
            wait.until(
                expected_conditions.invisibility_of_element_located((By.CLASS_NAME, "o_loading"))
            )
            return res
        return inner
    return decorator
