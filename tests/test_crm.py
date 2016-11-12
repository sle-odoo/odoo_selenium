# -*- coding: utf-8 -*-

from page_objects.login import Login
from common import SeleniumCase


class TestCRM(SeleniumCase):

    _depends = ['crm']

    def setUp(self):
        super(TestCRM, self).setUp()
        self.web_client = Login(self.driver, self.odoo_url).login("admin", "admin")
        # FIXME
        import os
        self.addCleanup(os.kill, self.odoo_process.pid, 9)

    def test_01_partners_handling(self):
        # Create two partners
        self.web_client.open_app_switcher()
        self.web_client.app_switcher.click_on_menu("CRM")
        self.assertTrue(self.web_client.kanban_view.is_opened())
        self.web_client.menu.click_on_top_menu("Sales")
        self.web_client.menu.click_on_menu("Customers")
        self.assertTrue(self.web_client.kanban_view.is_opened())
        self.web_client.kanban_view.create()
        self.assertTrue(self.web_client.form_view.is_opened())
        self.assertTrue(self.web_client.form_view.is_in_edit_mode())
        self.web_client.form_view.set_field_value_by_placeholder_name("Name", "Customer test 1")
        self.web_client.form_view.save()
        self.web_client.form_view.create()
        self.web_client.form_view.set_field_value_by_placeholder_name("Name", "Customer test 2")
        self.web_client.form_view.fill_field_by_label("Job Position", "Job position of customer test 2")
        self.web_client.form_view.save()

        # Merge these two partners
        self.web_client.control_panel.breadcrumbs.go_to_previous()
        self.web_client.control_panel.view_switcher.to_list()
        self.web_client.control_panel.search_view.type_and_enter("Customer test")
        self.web_client.list_view.select_all_rows()
        self.web_client.control_panel.sidebar.click_on_action("Merge Selected Contacts")
        self.assertTrue(self.web_client.wizard.is_opened())
        self.web_client.wizard.click_on_footer_buttons("MERGE CONTACTS")
        self.assertTrue(self.web_client.wizard.is_opened())
        self.web_client.wizard.click_on_footer_buttons("Close")

        # Check that the merge did something
        self.web_client.list_view.click_on_row(1)
        self.web_client.form_view.is_opened()
        self.assertEqual(
            self.web_client.control_panel.breadcrumbs.get_current_step_value(),
            "Customer test 1"
        )
        self.assertEqual(
            self.web_client.form_view.get_field_value_by_label_name("Job Position"),
            "Job position of customer test 2"
        )


if __name__ == '__main__':
    import unittest
    unittest.main()
