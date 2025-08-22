import sys
import types
from unittest.mock import MagicMock
import pytest

# Provide minimal selenium stubs if selenium is unavailable
if 'selenium' not in sys.modules:
    selenium = types.ModuleType('selenium')
    sys.modules['selenium'] = selenium

    common = types.ModuleType('selenium.common')
    exceptions = types.ModuleType('selenium.common.exceptions')

    class TimeoutException(Exception):
        pass

    class NoSuchElementException(Exception):
        pass

    exceptions.TimeoutException = TimeoutException
    exceptions.NoSuchElementException = NoSuchElementException
    common.exceptions = exceptions
    sys.modules['selenium.common'] = common
    sys.modules['selenium.common.exceptions'] = exceptions

    webdriver = types.ModuleType('selenium.webdriver')
    webdriver.common = types.ModuleType('selenium.webdriver.common')
    by = types.ModuleType('selenium.webdriver.common.by')

    class By:
        ID = 'id'
        XPATH = 'xpath'
    by.By = By
    webdriver.common.by = by

    support = types.ModuleType('selenium.webdriver.support')
    support.expected_conditions = types.ModuleType('selenium.webdriver.support.expected_conditions')
    ui = types.ModuleType('selenium.webdriver.support.ui')

    class WebDriverWait:
        def __init__(self, *args, **kwargs):
            pass
        def until(self, method):
            return None
    ui.WebDriverWait = WebDriverWait
    support.ui = ui
    webdriver.support = support

    sys.modules['selenium.webdriver'] = webdriver
    sys.modules['selenium.webdriver.common'] = webdriver.common
    sys.modules['selenium.webdriver.common.by'] = by
    sys.modules['selenium.webdriver.support'] = support
    sys.modules['selenium.webdriver.support.expected_conditions'] = support.expected_conditions
    sys.modules['selenium.webdriver.support.ui'] = ui

import pages.base_page as base_page
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException


@pytest.mark.parametrize("exception", [TimeoutException, NoSuchElementException])
def test_is_element_selected_returns_false_when_locator_absent(exception):
    page = BasePage(MagicMock())
    base_page.EC.presence_of_element_located = MagicMock()
    page.wait.until = MagicMock(side_effect=exception("not found"))
    assert page.is_element_selected((By.ID, "missing")) is False

