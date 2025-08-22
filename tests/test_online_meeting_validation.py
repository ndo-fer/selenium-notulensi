import sys
import types

import pytest


try:
    from pages.meeting_creation_page import MeetingCreationPage
except ModuleNotFoundError:
    # Create minimal selenium stubs for testing without the actual package
    selenium = types.ModuleType("selenium")
    webdriver = types.ModuleType("selenium.webdriver")
    common = types.ModuleType("selenium.webdriver.common")
    by_mod = types.ModuleType("selenium.webdriver.common.by")

    class DummyBy:
        ID = "id"
        XPATH = "xpath"

    by_mod.By = DummyBy
    support = types.ModuleType("selenium.webdriver.support")
    ec_mod = types.ModuleType("selenium.webdriver.support.expected_conditions")
    support.expected_conditions = ec_mod
    ui_mod = types.ModuleType("selenium.webdriver.support.ui")

    class WebDriverWait:  # pragma: no cover - stub
        def __init__(self, *args, **kwargs):
            pass
    ui_mod.WebDriverWait = WebDriverWait
    common_exc = types.ModuleType("selenium.common.exceptions")

    class TimeoutException(Exception):
        pass

    class ElementClickInterceptedException(Exception):
        pass

    common_exc.TimeoutException = TimeoutException
    common_exc.ElementClickInterceptedException = ElementClickInterceptedException

    sys.modules.update({
        "selenium": selenium,
        "selenium.webdriver": webdriver,
        "selenium.webdriver.common": common,
        "selenium.webdriver.common.by": by_mod,
        "selenium.webdriver.support": support,
        "selenium.webdriver.support.expected_conditions": ec_mod,
        "selenium.webdriver.support.ui": ui_mod,
        "selenium.common": types.ModuleType("selenium.common"),
        "selenium.common.exceptions": common_exc,
    })

    from pages.meeting_creation_page import MeetingCreationPage


class DummyMeetingCreationPage(MeetingCreationPage):
    """Stub page object that bypasses Selenium interactions."""

    def __init__(self):
        # Do not call BasePage.__init__
        pass

    def click(self, by_locator):  # pragma: no cover - stub
        pass

    def enter_text(self, by_locator, text):  # pragma: no cover - stub
        pass


@pytest.mark.parametrize(
    "link",
    [
        "https://meet.google.com/abc-defg-hij",
        "https://zoom.us/j/123456789",
        "https://teams.microsoft.com/l/meetup-join/19%3ameeting_ABCD123",
    ],
)
def test_valid_links(link):
    page = DummyMeetingCreationPage()
    page.create_online_meeting(link, "Valid Name")


@pytest.mark.parametrize(
    "invalid_link",
    ["invalid", "https://invalid.com", " ", None],
)
def test_invalid_links_raise(invalid_link):
    page = DummyMeetingCreationPage()
    with pytest.raises(ValueError):
        page.create_online_meeting(invalid_link, "Name")


def test_meeting_name_too_long():
    page = DummyMeetingCreationPage()
    long_name = "A" * 256
    with pytest.raises(ValueError):
        page.create_online_meeting("https://meet.google.com/abc-defg-hij", long_name)
