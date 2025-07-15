from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.logger import logger
import time
import os

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.logger = logger
    
    def click(self, by_locator):
        self.logger.info(f"Clicking on element: {by_locator}")
        try:
            element = self.wait.until(EC.element_to_be_clickable(by_locator))
            element.click()
            self.logger.info("Successfully clicked the element")
        except Exception as e:
            self.logger.error(f"Failed to click element: {str(e)}")
            raise
    
    def enter_text(self, by_locator, text):
        self.logger.info(f"Entering text '{text}' in element: {by_locator}")
        try:
            element = self.wait.until(EC.visibility_of_element_located(by_locator))
            element.clear()
            element.send_keys(text)
            self.logger.info("Text entered successfully")
        except Exception as e:
            self.logger.error(f"Failed to enter text: {str(e)}")
            raise
    
    def get_text(self, by_locator):
        self.logger.info(f"Getting text from element: {by_locator}")
        try:
            text = self.wait.until(EC.visibility_of_element_located(by_locator)).text
            self.logger.info(f"Retrieved text: '{text}'")
            return text
        except Exception as e:
            self.logger.error(f"Failed to get text: {str(e)}")
            raise
    
    def take_screenshot(self, name):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/{name}_{timestamp}.png"
        
        # Buat folder jika belum ada
        if not os.path.exists('screenshots'):
            os.makedirs('screenshots')
        
        self.driver.save_screenshot(filename)
        self.logger.info(f"Screenshot saved as {filename}")
    
    def is_element_visible(self, by_locator):
        """Cek apakah element visible di halaman"""
        try:
            return self.wait.until(EC.visibility_of_element_located(by_locator)) is not None
        except:
            return False
    
    def dismiss_modal_if_exists(self, by_locator, timeout=10):
        """
        Safely dismiss modal if it appears with proper wait
        Usage: page.dismiss_modal_if_exists((By.ID, "notNowButton"))
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(by_locator)
            )
            element.click()
            self.logger.info(f"Dismissed modal with locator: {by_locator}")
            return True
        except Exception as e:
            from selenium.common.exceptions import TimeoutException
            if isinstance(e, TimeoutException):
                self.logger.info("No modal found to dismiss")
                return False
            else:
                self.logger.error(f"Error while dismissing modal: {str(e)}")
                raise