# -*- coding: utf-8 -*-

from selenium import webdriver
from unittest import TestCase


class SeleniumCase(TestCase):

    def setUp(self):
        super(SeleniumCase, self).setUp()
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.close()
        super(SeleniumCase, self).tearDown()

    def shortDescription(self):
        doc = self._testMethodDoc
        return doc and ' '.join(filter(None, map(str.strip, doc.splitlines()))) or None
