from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from pages.base_page import BasePage
import time

class MeetingCreationPage(BasePage):
    # Locators
    MEETING_TYPE_ONLINE = (By.ID, "meetingType-Online")
    MEETING_TYPE_UPLOAD = (By.ID, "meetingType-Upload")
    MEETING_LINK_INPUT = (By.ID, "meeting_link")
    LANGUAGE_INDONESIAN = (By.ID, "meetingLang-Indonesian")
    LANGUAGE_ENGLISH = (By.ID, "meetingLang-English")
    MEETING_NAME_INPUT = (By.ID, "meeting_name")
    SUBMIT_BUTTON = (By.ID, "createNewMeetingBtn")
    CANCEL_BUTTON = (By.XPATH, '//*[@id=":r24:"]/button')
    UPLOAD_INPUT = (By.ID, "createNewMeetingBtn")
    
    def select_meeting_type(self, meeting_type):
        """Select meeting type only if not already selected"""
        current_type = self.get_selected_meeting_type()
        if current_type.lower() != meeting_type.lower():
            if meeting_type.lower() == "online":
                self.click(self.MEETING_TYPE_ONLINE)
            elif meeting_type.lower() == "upload":
                self.click(self.MEETING_TYPE_UPLOAD)
    
    def get_selected_meeting_type(self):
        """Get currently selected meeting type"""
        if self.is_element_selected(self.MEETING_TYPE_ONLINE):
            return "Online"
        elif self.is_element_selected(self.MEETING_TYPE_UPLOAD):
            return "Upload"
        return None
    
    def select_language(self, language):
        """Select language only if not already selected"""
        current_lang = self.get_selected_language()
        if current_lang.lower() != language.lower():
            if language.lower() == "indonesia":
                self.click(self.LANGUAGE_INDONESIAN)
            elif language.lower() == "english":
                self.click(self.LANGUAGE_ENGLISH)
    
    def get_selected_language(self):
        """Get currently selected language"""
        if self.is_element_selected(self.LANGUAGE_INDONESIAN):
            return "Indonesia"
        elif self.is_element_selected(self.LANGUAGE_ENGLISH):
            return "English"
        return None
    
    def create_online_meeting(self, meeting_link, meeting_name=""):
        """Create online meeting with default Indonesia language"""
        print("1")
        self.click(self.MEETING_LINK_INPUT)
        print("2")
        self.enter_text(self.MEETING_LINK_INPUT, meeting_link)
        if meeting_name:
            self.enter_text(self.MEETING_NAME_INPUT, meeting_name)
        self.click(self.SUBMIT_BUTTON)
    
    def upload_file(self, file_path):
        """Upload file for meeting"""
        self.enter_text(self.UPLOAD_INPUT, file_path)
    
    def create_meeting(self, meeting_name=""):
        """Finalize meeting creation"""
        if meeting_name:
            self.enter_text(self.MEETING_NAME_INPUT, meeting_name)
        self.click(self.SUBMIT_BUTTON)
    
    def is_meeting_created(self):
        """Check if meeting was successfully created"""
        # try:
        #     return self.wait.until(
        #         EC.visibility_of_element_located(
        #             (By.ID, ":r1q:")
        #         )
        #     ).is_displayed()
        # except TimeoutException:
        #     return False
    
    def open_meeting_creation_dialog(self):
        """Open meeting dialog by clicking notNowButton first, then createNewMeetingTrigger, with waits."""
        try:
            # Click notNowButton if present
            not_now_btn = self.wait.until(
                EC.element_to_be_clickable((By.ID, "notNowButton"))
            )
            not_now_btn.click()
            time.sleep(3)  # Wait after dismissing modal

        except TimeoutException:
            # notNowButton not present, continue
            pass

        # Click createNewMeetingTrigger
        trigger = self.wait.until(
            EC.element_to_be_clickable((By.ID, "createNewMeetingTrigger"))
        )
        trigger.click()
        time.sleep(3)  # Wait after opening dialog
        
        # Wait specifically for dialog animation to complete
        # self.wait.until(
        #     lambda d: "show" in d.find_element(
        #         By.ID, "meetingDialog").get_attribute("class"))