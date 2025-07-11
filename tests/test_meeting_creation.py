import pytest
from pages.meeting_creation_page import MeetingCreationPage
import os

class TestMeetingCreation:
    @pytest.fixture(autouse=True)
    def setup(self, login_flow):
        """Setup: Login terlebih dahulu"""
        self.login_flow = login_flow
        self.meeting_page = MeetingCreationPage(login_flow.driver)
        
        # Login dengan credential valid
        self.login_flow.execute_login_flow(
            email="nandopanjaitan003@gmail.com",
            password="Twice300403"
        )
        
        # Buka dialog create meeting
        self.meeting_page.open_meeting_creation_dialog()
        yield
    
    def test_create_online_meeting_with_gmeet_link(self):
        """Test membuat online meeting dengan GMeet link"""
        # Data test
        GMEET_LINK = "https://meet.google.com/jna-nsyi-qqa"
        
        # Eksekusi create meeting
        self.meeting_page.create_online_meeting(
            meeting_link=GMEET_LINK,
            language="indonesian",
            meeting_name="Test Meeting GMeet"
        )
        
        # Verifikasi (sesuaikan dengan aplikasi Anda)
        assert "meeting" in self.login_flow.driver.current_url.lower()
    
    def test_create_online_meeting_with_zoom_link(self):
        """Test membuat online meeting dengan Zoom link"""
        # Data test
        ZOOM_LINK = "https://zoom.us/j/123456789"
        
        # Eksekusi create meeting
        self.meeting_page.create_online_meeting(
            meeting_link=ZOOM_LINK,
            language="english",
            meeting_name="Test Meeting Zoom"
        )
        
        # Verifikasi
        assert "meeting" in self.login_flow.driver.current_url.lower()
    
    def test_create_meeting_with_audio_upload(self):
        """Test membuat meeting dengan upload file audio"""
        # Dapatkan path file sample (buat folder test_files di root project)
        file_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            "../test_files/sample_audio.mp3"
        ))
        
        # Pastikan file sample ada
        if not os.path.exists(file_path):
            pytest.skip("File sample audio tidak ditemukan")
        
        # Eksekusi create meeting
        self.meeting_page.create_upload_meeting(
            file_path=file_path,
            language="indonesian",
            meeting_name="Test Meeting Upload Audio"
        )
        
        # Verifikasi
        assert "meeting" in self.login_flow.driver.current_url.lower()