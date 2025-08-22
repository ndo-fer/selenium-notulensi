import sys
import types
from unittest.mock import MagicMock

# Provide minimal selenium stubs if selenium is unavailable
if 'selenium' not in sys.modules:
    selenium = types.ModuleType('selenium')
    sys.modules['selenium'] = selenium

    common = types.ModuleType('selenium.common')
    exceptions = types.ModuleType('selenium.common.exceptions')
    class TimeoutException(Exception):
        pass
    class ElementClickInterceptedException(Exception):
        pass
    exceptions.TimeoutException = TimeoutException
    exceptions.ElementClickInterceptedException = ElementClickInterceptedException
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

from pages.meeting_creation_page import MeetingCreationPage

def test_select_meeting_type_no_default():
    """Should select meeting type when no default is chosen"""
    page = MeetingCreationPage(MagicMock())
    page.get_selected_meeting_type = MagicMock(return_value=None)
    page.click = MagicMock()

    page.select_meeting_type("Online")

    page.click.assert_called_once_with(page.MEETING_TYPE_ONLINE)


def test_select_language_no_default():
    """Should select language when no default is chosen"""
    page = MeetingCreationPage(MagicMock())
    page.get_selected_language = MagicMock(return_value=None)
    page.click = MagicMock()

    page.select_language("English")

    page.click.assert_called_once_with(page.LANGUAGE_ENGLISH)
