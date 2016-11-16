# -*- coding: utf-8 -*-

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from page_objects.common import PageObject, wait_rpc_done


class ListView(PageObject):

    @property
    def root(self):
        list_views = self.driver.find_elements_by_class_name('o_list_view')
        displayed_list_views = [list_view for list_view in list_views if list_view.is_displayed()]
        if len(displayed_list_views) == 1:
            return displayed_list_views[0]

    def is_opened(self):
        return self.driver.find_element_by_class_name("o_list_view") is not None

    @wait_rpc_done()
    def create(self):
        self.driver.find_element_by_class_name("o_list_buttons")\
            .find_element_by_class_name("o_list_button_add")\
            .click()

    def select_rows(self, *args):
        pass

    def select_all_rows(self):
        self.root\
            .find_element_by_class_name("o_list_record_selector")\
            .find_element_by_tag_name("input")\
            .click()

    @wait_rpc_done()
    def click_on_row(self, row_index):
        rows = self.root\
            .find_element_by_tag_name("tbody")\
            .find_elements_by_tag_name("tr")
        rows[row_index -1].click()

    @wait_rpc_done()
    def click_on_row_and_type(self, row_index, text):
        rows = self.root \
            .find_element_by_tag_name("tbody") \
            .find_elements_by_tag_name("tr")
        row = rows[row_index - 1]

        row.click()
        cell = self.driver.switch_to_active_element()
        cell.send_keys(text)
        cell.send_keys(Keys.ENTER)

    def _get_cell(self, row_number, column_name):
        headers = self.root.find_element_by_tag_name("thead").find_elements_by_tag_name("th")
        header = next((h for h in headers if h.text == column_name), None)
        if not header:
            raise NoSuchElementException("Header with text %s not found" % column_name)
        return self.root\
            .find_element_by_tag_name("tbody")\
            .find_elements_by_tag_name("tr")[row_number - 1]\
            .find_elements_by_tag_name("td")[headers.index(header)]

    def get_cell_value(self, row_number, column_name):
        return self._get_cell(row_number, column_name).text

    def get_rows(self):
        return self.root\
            .find_element_by_tag_name("tbody") \
            .find_elements_by_tag_name("tr")

    def wait_until_row_is_visible_and_contains(self, row_number, column_name, expected_row_value):
        wait = WebDriverWait(self.driver, 30, ignored_exceptions=[StaleElementReferenceException])

        def _wait_until_row_is_visible(driver):
            if len(self.get_rows()) - 1 != row_number:  # FIXME remove add an item row ; FIXME if a ask for a row already present this won't work
                return False
            else:
                if self.get_cell_value(row_number, column_name) == expected_row_value:
                    return True

        wait.until(_wait_until_row_is_visible)
