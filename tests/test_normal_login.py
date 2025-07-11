import pytest
from pages.login_flow import LoginFlow
from utilities.logger import logger

class TestNormalLogin:
    @pytest.fixture(autouse=True)
    def setup(self, browser):
        self.login_flow = LoginFlow(browser)
        yield
        logger.info("Test completed. Cleaning up...")
    
    def test_successful_login_with_valid_credentials(self):
        """Test alur login normal dengan credential valid"""
        logger.info("Starting test_successful_login_with_valid_credentials")
        
        # Data test
        TEST_EMAIL = "nandopanjaitan003@gmail.com"
        TEST_PASSWORD = "Twice300403"
        
        # Eksekusi login flow
        result = self.login_flow.execute_login_flow(TEST_EMAIL, TEST_PASSWORD)
        
        # Verifikasi
        assert result is True, "Login flow should return True"
        
        # Verifikasi tambahan: button create meeting visible
        assert self.login_flow.is_element_visible(self.login_flow.CREATE_MEETING_BUTTON), \
            "Create meeting button should be visible after login"
        
        logger.info("Successfully verified login and dashboard page")
    
    @pytest.mark.parametrize("email,password", [
        ("valid@example.com", "wrongpass"),
        ("invalid@example.com", "password123"),
        ("", "password123"),
        ("valid@example.com", "")
    ])
    def test_login_with_invalid_credentials(self, email, password):
        """Test login dengan berbagai kombinasi credential invalid"""
        logger.info(f"Starting test with email: {email}, password: {password}")
        
        with pytest.raises(Exception):
            self.login_flow.execute_login_flow(email, password)
        
        logger.info("Test passed - login failed as expected with invalid credentials")