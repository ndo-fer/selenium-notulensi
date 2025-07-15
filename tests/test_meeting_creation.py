import os
import pytest
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.meeting_creation_page import MeetingCreationPage

class TestMeetingCreation:
    @pytest.fixture(autouse=True)
    def setup(self, login_flow):
        """Optimized setup with modal handling"""
        self.login_flow = login_flow
        self.meeting_page = MeetingCreationPage(login_flow.driver)
        
        # Login and handle any modals
        self.login_flow.execute_login_flow(
            email="valid@email.com",
            password="validPassword"
        )
        
        # Additional stabilization before opening dialog
        self.meeting_page.wait.until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, ".loading-spinner")))
        
        # Open meeting dialog with retry
        self.meeting_page.open_meeting_creation_dialog()
        
        yield
        
        # Cleanup with improved reliability
        try:
            self.meeting_page.close_meeting_creation_dialog()
        except Exception as e:
            self.meeting_page.take_screenshot("teardown_error")
            self.meeting_page.driver.refresh()  # Reset state
            
    @pytest.fixture(autouse=True)
    def setup(self, login_flow):
        """Setup: Login and open meeting creation dialog"""
        self.login_flow = login_flow
        self.meeting_page = MeetingCreationPage(login_flow.driver)
        self.login_flow.execute_login_flow(
            email="nandopanjaitan003@gmail.com",
            password="Twice300403"
        )
        self.meeting_page.open_meeting_creation_dialog()
        yield
        # Teardown
        self.meeting_page.close_meeting_creation_dialog()

    # --- Online Meeting Tests ---
    def test_create_online_meeting_default(self):
        """Test creating online meeting with default values (Indonesia)"""
        meeting_link = "https://meet.google.com/jna-nsyi-qqa"
        
        # Tidak perlu set type (default Online) dan language (default Indonesia)
        self.meeting_page.create_online_meeting(
            meeting_link=meeting_link,
            meeting_name="Test Default Meeting"
        )
        
        assert self.meeting_page.is_meeting_created()
        assert self.meeting_page.get_selected_language() == "Indonesia"

    def test_create_online_meeting_english(self):
        """Test creating online meeting with English language"""
        meeting_link = "https://zoom.us/j/123456789"
        
        # Tidak perlu set type (default Online), tapi perlu set language
        self.meeting_page.select_language("English")
        self.meeting_page.create_online_meeting(
            meeting_link=meeting_link,
            meeting_name="Test English Meeting"
        )
        
        assert self.meeting_page.is_meeting_created()
        assert self.meeting_page.get_selected_language() == "English"

    @pytest.mark.parametrize("meeting_link", [
        "https://meet.google.com/jna-nsyi-qqa",
        "https://zoom.us/j/123456789",
        "https://teams.microsoft.com/l/meetup-join/19%3ameeting_ABCD123"
    ])
    def test_create_online_meeting_various_platforms(self, meeting_link):
        """Test online meeting with various platform links"""
        self.meeting_page.create_online_meeting(
            meeting_link=meeting_link,
            meeting_name="Test Platform: " + meeting_link.split('/')[2]
        )
        assert self.meeting_page.is_meeting_created()

    # --- Upload Meeting Tests ---
    def test_create_meeting_with_audio_upload(self):
        """Test creating meeting with audio file upload"""
        file_path = os.path.abspath("test_files/sample_audio.mp3")
        
        # Perlu set type ke Upload (bukan default)
        self.meeting_page.select_meeting_type("Upload")
        self.meeting_page.upload_file(file_path)
        self.meeting_page.create_meeting(
            meeting_name="Test Audio Upload"
        )
        
        assert self.meeting_page.is_meeting_created()
        assert "audio" in self.meeting_page.get_uploaded_file_type()

    def test_create_meeting_with_video_upload(self):
        """Test creating meeting with video file upload"""
        file_path = os.path.abspath("test_files/sample_video.mp4")
        
        self.meeting_page.select_meeting_type("Upload")
        self.meeting_page.upload_file(file_path)
        self.meeting_page.select_language("English")  # Non-default language
        self.meeting_page.create_meeting(
            meeting_name="Test Video Upload"
        )
        
        assert self.meeting_page.is_meeting_created()
        assert "video" in self.meeting_page.get_uploaded_file_type()

    # --- Validation Tests ---
    @pytest.mark.parametrize("invalid_link", [
        "invalidlink",
        "https://invalid.com",
        " ",
        None
    ])
    def test_invalid_meeting_links(self, invalid_link):
        """Test invalid meeting links validation"""
        with pytest.raises(ValueError, match="Invalid meeting link"):
            self.meeting_page.create_online_meeting(
                meeting_link=invalid_link,
                meeting_name="Test Invalid Link"
            )

    @pytest.mark.parametrize("name,expected", [
        ("Normal Name", True),
        ("A", True),  # Minimum length
        ("", True),   # Optional
        (255*"A", True),  # Max length
        (256*"A", False)  # Exceeds max length
    ])
    def test_meeting_name_validation(self, name, expected):
        """Test meeting name validation"""
        if expected:
            self.meeting_page.create_online_meeting(
                meeting_link="https://meet.google.com/jna-nsyi-qqa",
                meeting_name=name
            )
            assert self.meeting_page.is_meeting_created()
        else:
            with pytest.raises(ValueError, match="Meeting name too long"):
                self.meeting_page.create_online_meeting(
                    meeting_link="https://meet.google.com/jna-nsyi-qqa",
                    meeting_name=name
                )

    # --- Edge Cases ---
    def test_cancel_meeting_creation(self):
        """Test canceling meeting creation"""
        self.meeting_page.cancel_creation()
        assert not self.meeting_page.is_creation_dialog_open()

    def test_create_meeting_no_name(self):
        """Test meeting creation without name (optional)"""
        self.meeting_page.create_online_meeting(
            meeting_link="https://meet.google.com/jna-nsyi-qqa",
            meeting_name=""  # Empty name
        )
        assert self.meeting_page.is_meeting_created()
        assert self.meeting_page.get_meeting_name() == "Untitled Meeting"