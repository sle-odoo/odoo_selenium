# -*- coding: utf-8 -*-

from page_objects.common import PageObject
import page_objects


class WebClient(PageObject):

    def __init__(self, *args, **kwargs):
        super(WebClient, self).__init__(*args, **kwargs)

        self.app_switcher = page_objects.AppSwitcher.AppSwitcher(self.driver)
        self.control_panel = page_objects.ControlPanel.ControlPanel(self.driver)
        self.form_view = page_objects.FormView.FormView(self.driver)
        self.kanban_view = page_objects.KanbanView.KanbanView(self.driver)
        self.list_view = page_objects.ListView.ListView(self.driver)
        self.menu = page_objects.Menu.Menu(self.driver)
        self.wizard = page_objects.Wizard.Wizard(self.driver)

    def open_app_switcher(self):
        self.app_switcher.open()
