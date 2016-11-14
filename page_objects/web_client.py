# -*- coding: utf-8 -*-

from selenium.webdriver.common.keys import Keys

from page_objects.common import PageObject
import page_objects


class WebClient(PageObject):

    @property
    def root(self):
        return self.driver.find_element_by_class_name("o_web_client")

    def __init__(self, *args, **kwargs):
        super(WebClient, self).__init__(*args, **kwargs)

        self.app_switcher = page_objects.app_switcher.AppSwitcher(self.driver)
        self.control_panel = page_objects.control_panel.ControlPanel(self.driver)
        self.form_view = page_objects.form_view.FormView(self.driver)
        self.kanban_view = page_objects.kanban_view.KanbanView(self.driver)
        self.list_view = page_objects.list_view.ListView(self.driver)
        self.menu = page_objects.menu.Menu(self.driver)
        self.wizard = page_objects.wizard.Wizard(self.driver)

    def open_app_switcher(self):
        self.app_switcher.open()

    def send_barcode(self, barcode):
        self.root.send_keys(barcode)
        self.root.send_keys(Keys.ENTER)
