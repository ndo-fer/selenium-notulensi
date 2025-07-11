from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class AuthDialog(BasePage):
    REGISTER_NOW_BUTTON = (By.ID, "registerNow")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def click_register_now(self):
        self.click(self.REGISTER_NOW_BUTTON)