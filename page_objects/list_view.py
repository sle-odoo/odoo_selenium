# -*- coding: utf-8 -*-

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from page_objects.common import PageObject, wait_rpc_done


class ListView(PageObject):

    @property
    def root(self):
        list_views = self.driver.find_elements_by_class_name('o_list_view')
        return next((list_view for list_view in list_views if list_view.is_displayed()), None)

    def is_opened(self):
        return self.root is not None

    @wait_rpc_done()
    def create(self):
        self.driver.find_element_by_class_name("o_list_buttons")\
            .find_element_by_class_name("o_list_button_add")\
            .click()

    def row_select_all(self):
        self.root\
            .find_element_by_class_name("o_list_record_selector")\
            .find_element_by_tag_name("input")\
            .click()

    def get_rows(self):
        rows = self.root\
            .find_element_by_tag_name("tbody") \
            .find_elements_by_tag_name("tr")
        return [row for row in rows if row.text != "Add an item"]

    def get_non_empty_rows(self):
        return [row for row in self.get_rows() if row.text.strip()]

    def get_row(self, row_index):
        rows = self.get_rows()
        if len(rows) < row_index:
            raise NoSuchElementException(msg='Row with index %s was not found '
                                             '(not enough rows in the displayed list view).' % row_index)
        return rows[row_index - 1]

    @wait_rpc_done()
    def row_click(self, row_index):
        self.get_row(row_index).click()

    @wait_rpc_done()
    def row_click_and_type(self, row_index, text):
        self.get_row(row_index).click()
        cell = self.driver.switch_to_active_element()
        cell.send_keys(text)
        cell.send_keys(Keys.ENTER)

    def _get_cell(self, row_index, column_name):
        headers = self.root.find_element_by_tag_name("thead").find_elements_by_tag_name("th")
        header = next((h for h in headers if h.text == column_name), None)
        if not header:
            raise NoSuchElementException("Header with text %s not found." % column_name)
        return self.get_row(row_index)\
            .find_elements_by_tag_name("td")[headers.index(header)]

    def get_cell_value(self, row_index, column_name):
        return self._get_cell(row_index, column_name).text

    def wait_until_row_is_visible_and_contains(self, row_index, column_name, expected_row_value):
        wait = WebDriverWait(self.driver, 30, ignored_exceptions=[StaleElementReferenceException])

        def _wait_until_row_is_visible(driver):
            if len(self.get_non_empty_rows()) >= row_index:
                return self.get_cell_value(row_index, column_name) == expected_row_value
            else:
                return False

        wait.until(_wait_until_row_is_visible)
