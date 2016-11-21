# -*- coding: utf-8 -*-

from common import SeleniumCase


class TestStockBarcode(SeleniumCase):

    _depends = ['stock_barcode']

    def test_01_barcode_handling(self):
        """ Stress the barcode handler of a picking by sending very quickly
        barcodes and check that they are rightly queued.
        """
        self.web_client = self.login("admin", "admin")

        # create user with the stock manager access rights
        self.web_client.open_app_switcher()
        self.web_client.app_switcher.click_on_menu("Settings")
        self.web_client.menu.dropdown_click("Users", "Users")
        self.assertTrue(self.web_client.list_view.is_opened())
        self.web_client.list_view.create()
        self.assertTrue(self.web_client.form_view.is_opened())
        self.web_client.form_view.fill_field_by_label("Name", "stock user 1")
        self.web_client.form_view.fill_field_by_label("Email Address", "stock user 1")
        self.web_client.form_view.fill_field_by_label("Inventory", "Manager")
        self.web_client.form_view.save()
        self.assertTrue(self.web_client.form_view.is_in_readonly_mode())
        self.assertTrue(self.web_client.control_panel.sidebar.is_opened())
        self.web_client.control_panel.sidebar.click("Change Password")  # FIXME sometimes fail
        self.assertTrue(self.web_client.wizard.is_opened())
        self.assertTrue(self.web_client.list_view.is_opened())
        self.web_client.list_view.row_click_and_type(1, "password")
        self.web_client.wizard.click_on_footer_buttons("CHANGE PASSWORD")
        self.web_client.wizard.wait_is_closed()
        self.assertTrue(self.web_client.form_view.is_opened())  # FIXME
        self.web_client.menu.user_menu.click("Log out")
        self.web_client = self.login("stock user 1", "password")

        # set an email on the user, for some reasons it's mandatory when creating a product
        self.web_client.menu.user_menu.click("Preferences")
        self.assertTrue(self.web_client.wizard.is_opened())
        self.web_client.form_view.fill_field_by_label("Email", "fake@fake.fake")
        self.web_client.wizard.click_on_footer_buttons("SAVE")

        # create some products
        self.assertTrue(self.web_client.app_switcher.is_opened())
        self.web_client.app_switcher.click_on_menu("Inventory")
        self.assertTrue(self.web_client.kanban_view.is_opened())
        self.web_client.menu.dropdown_click("Inventory Control", "Products")
        self.assertTrue(self.web_client.kanban_view.is_opened())
        self.web_client.kanban_view.create()
        self.assertTrue(self.web_client.form_view.is_opened())
        self.web_client.form_view.fill_field_by_label("Product Name", "dummy")
        self.web_client.form_view.save()
        products = {
            'product01': '1000000000009',
            'product02': '2000000000008',
            'product03': '3000000000007',
            'product04': '4000000000006',
            'product05': '5000000000005',
            'product06': '6000000000004',
            'product07': '7000000000003',
            'product08': '8000000000002',
            'product09': '9000000000001',
            'product10': '0100000000007',
        }
        for name, barcode in products.iteritems():
            self.web_client.form_view.create()
            self.web_client.form_view.fill_field_by_label("Product Name", name)
            self.web_client.form_view.fill_field_by_label("Barcode", barcode)
            self.web_client.form_view.save()

        def _test_picking_barcode(xs=False):
            # create 5 pickings and scan 20 times each product created before
            for x in range(0, 5):
                self.web_client.open_app_switcher()
                self.assertTrue(self.web_client.app_switcher.is_opened())
                self.web_client.app_switcher.click_on_menu("Barcode")
                self.driver.find_element_by_class_name("button_operations").click()
                self.web_client.kanban_view.wait_is_opened()
                self.web_client.kanban_view.vignette_click(1)
                self.web_client.kanban_view.create()
                # set no initial demand
                self.web_client.form_view.status_bar.click("MARK AS TODO")
                # scan the products
                for _, barcode_ in products.iteritems():
                    for y in range(0, 20):
                        self.web_client.send_barcode(barcode_)

                # it's possible that all barcodes were not yet processed here (they are queued)
                # wait for the last one to complete before the asserts
                if not xs:
                    self.web_client.list_view.wait_until_row_is_visible_and_contains(len(products), "Done", "20")
                    i = 1
                    while i < len(products) + 1:
                        self.assertEqual(self.web_client.list_view.get_cell_value(i, "Done"), "20")
                        i += 1
                    self.assertEqual(len(self.web_client.list_view.get_rows()), len(products))
                else:
                    self.web_client.kanban_view.wait_until_vignette_is_visible_and_contains(len(products), "20.000 of 0.000 Unit(s)")
                    i = 1
                    while i < len(products) + 1:
                        self.assertTrue(self.web_client.kanban_view.vignette_contains(i, "20.000 of 0.000 Unit(s)"))
                        i += 1
                    self.assertEqual(len(self.web_client.kanban_view.get_vignettes()), len(products))

                # validate the picking
                self.web_client.form_view.status_bar.click("VALIDATE")
                self.web_client.form_view.save()
                self.assertTrue(self.web_client.form_view.is_opened())

        # Editable list
        _test_picking_barcode()

        # Kanban view
        self.driver.set_window_size(500, 800)
        _test_picking_barcode(xs=True)

        #TODO: test the "last quantity scanned feature
        #FIXME: memory leak in the webclient leading the so so so long wait screen arout the 8 or 9 picking
