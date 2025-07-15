from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import time

class LoginFlow(BasePage):
    # Locators
    GET_STARTED_BUTTON = (By.XPATH, '//*[@id="hero"]/div/div[1]/div[2]/div[2]/button')
    REGISTER_NOW_BUTTON = (By.ID, "registerNow")
    EMAIL_INPUT = (By.XPATH, "//input[@type='email']")
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password']")
    CREATE_MEETING_BUTTON = (By.ID, "createNewMeetingTrigger")
    
    def execute_login_flow(self, email, password):
        """Eksekusi seluruh alur login dengan logging"""
        try:
            # Step 1: Buka landing page
            self.logger.info("STEP 1: Membuka landing page")
            self.driver.get("https://notulensi.id")
            self.take_screenshot("landing_page")
            
            # Step 2: Klik Get Started
            self.logger.info("STEP 2: Mengklik tombol Get Started")
            self.click(self.GET_STARTED_BUTTON)
            self.take_screenshot("after_get_started")
            
            # Step 3: Klik Register Now di dialog
            self.logger.info("STEP 3: Mengklik Register Now di auth dialog")
            self.click(self.REGISTER_NOW_BUTTON)
            self.take_screenshot("auth_dialog")
            
            # Step 4: Mengisi form login
            self.logger.info("STEP 4: Mengisi form login")
            self.enter_text(self.EMAIL_INPUT, email)
            self.enter_text(self.PASSWORD_INPUT, password)
            self.driver.find_element(*self.PASSWORD_INPUT).send_keys(Keys.ENTER)
            self.take_screenshot("after_login_submit")
            
            # Step 5: Verifikasi login berhasil dengan memeriksa button create meeting
            self.logger.info("STEP 5: Memverifikasi login berhasil dengan mengecek button create meeting")
            
            # Tunggu hingga button create meeting muncul
            self.wait.until(EC.visibility_of_element_located(self.CREATE_MEETING_BUTTON))
            self.logger.info("Button create meeting ditemukan - login berhasil")
            
            # Verifikasi tambahan: pastikan URL mengandung '/dashboard' jika ada pola URL yang konsisten
            if "/dashboard" in self.driver.current_url.lower():
                self.logger.info("Berada di halaman dashboard")
            
            self.take_screenshot("dashboard_page")
            return True
            
            self._handle_post_login_modals()
            
        except Exception as e:
            self.base_page.take_screenshot("login_error")
            raise

    def _handle_post_login_modals(self):
        """Handle any post-login modals"""
        try:
            # Wait for dashboard to load completely
            self.base_page.wait.until(
                EC.presence_of_element_located((By.ID, "dashboardView"))
            )

            # Dismiss modal if appears (with multiple fallback options)
            modal_closed = (
                self.base_page.dismiss_modal_if_exists((By.ID, "notNowButton")) or
                self.base_page.dismiss_modal_if_exists((By.XPATH, "//button[contains(.,'Not Now')]")) or
                self.base_page.dismiss_modal_if_exists((By.CSS_SELECTOR, "[data-testid='modal-close-btn']"))
            )

            if modal_closed:
                self.base_page.logger.info("Post-login modal dismissed successfully")
            else:
                self.base_page.logger.info("No post-login modal appeared")

            # Additional stabilization wait
            self.base_page.wait.until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, ".modal-backdrop"))
            )
        except Exception as e:
            self.logger.error(f"Error in login flow: {str(e)}")
            self.take_screenshot("error_during_login")
            raise