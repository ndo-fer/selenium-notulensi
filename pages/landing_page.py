from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LandingPage(BasePage):
    GET_STARTED_BUTTON = (By.XPATH, '//*[@id="hero"]/div/div[1]/div[2]/div[2]/button')
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def open_landing_page(self):
        self.driver.get("https://notulensi.id")
    
    def click_get_started(self):
        self.click(self.GET_STARTED_BUTTON)