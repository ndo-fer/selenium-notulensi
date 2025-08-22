from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from pages.base_page import BasePage
import mimetypes
import os
import time
import re

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
    UPLOAD_INPUT = (By.ID, "meeting_file")
    CREATION_DIALOG = (By.ID, "meetingDialog")
    
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
        # Validate meeting link
        if not isinstance(meeting_link, str) or not meeting_link.strip():
            raise ValueError("Invalid meeting link")

        pattern = (
            r"^https://(meet\.google\.com/.+|"
            r"zoom\.us/j/.+|"
            r"teams\.microsoft\.com/.+)"
        )
        if not re.match(pattern, meeting_link.strip()):
            raise ValueError("Invalid meeting link")

        # Validate meeting name length (max 255 characters)
        if meeting_name and len(meeting_name) > 255:
            raise ValueError("Meeting name too long")

        self.click(self.MEETING_LINK_INPUT)
        self.enter_text(self.MEETING_LINK_INPUT, meeting_link)
        if meeting_name:
            self.enter_text(self.MEETING_NAME_INPUT, meeting_name)
        self.click(self.SUBMIT_BUTTON)
    
    def upload_file(self, file_path):
        """Upload file for meeting"""
        self.enter_text(self.UPLOAD_INPUT, file_path)

    def get_uploaded_file_type(self):
        """Get uploaded file MIME type (audio/video)"""
        try:
            file_input = self.wait.until(
                EC.presence_of_element_located(self.UPLOAD_INPUT)
            )
            file_path = file_input.get_attribute("value")
            if not file_path:
                return None
            if os.name == "nt":
                # Selenium on Windows returns path with backslashes
                file_path = file_path.split("\\")[-1]
            mime_type, _ = mimetypes.guess_type(file_path)
            return mime_type.split("/")[0] if mime_type else None
        except TimeoutException:
            return None

    def create_meeting(self, meeting_name=""):
        """Finalize meeting creation"""
        if meeting_name:
            self.enter_text(self.MEETING_NAME_INPUT, meeting_name)
        self.click(self.SUBMIT_BUTTON)

    def cancel_creation(self):
        """Cancel meeting creation by clicking cancel and waiting for dialog to close"""
        try:
            self.click(self.CANCEL_BUTTON)
            self.wait.until(EC.invisibility_of_element_located(self.CREATION_DIALOG))
        except (TimeoutException, ElementClickInterceptedException):
            return False
        return True

    def is_creation_dialog_open(self):
        """Check if meeting creation dialog is visible"""
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.CREATION_DIALOG)
            ).is_displayed()
        except TimeoutException:
            return False

    def get_meeting_name(self):
        """Return current meeting name or default if empty"""
        try:
            element = self.wait.until(
                EC.visibility_of_element_located(self.MEETING_NAME_INPUT)
            )
            name = element.get_attribute("value")
            return name if name else "Untitled Meeting"
        except TimeoutException:
            return None
    
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
