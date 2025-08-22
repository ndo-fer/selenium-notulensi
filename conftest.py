import pytest

try:
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
except ImportError:  # pragma: no cover
    webdriver = None
    ChromeDriverManager = None
    Service = None

@pytest.fixture(scope="function")
def browser():
    if webdriver is None:
        pytest.skip("selenium not installed")

    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)

    yield driver

    driver.quit()

@pytest.fixture
def landing_page(browser):
    from pages.landing_page import LandingPage
    return LandingPage(browser)

@pytest.fixture
def auth_dialog(browser):
    from pages.auth_dialog import AuthDialog
    return AuthDialog(browser)

@pytest.fixture
def login_page(browser):
    from pages.login_flow import LoginPage
    return LoginPage(browser)

@pytest.fixture
def login_flow(browser):
    from pages.login_flow import LoginFlow
    return LoginFlow(browser)