from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
import time

class MeetingCreationPage(BasePage):
    # Locators untuk dialog create meeting
    CREATE_MEETING_TRIGGER = (By.ID, "createNewMeetingTrigger")
    
    # Section 1: Meeting Type
    MEETING_TYPE_ONLINE = (By.ID, "meetingType-Online")
    MEETING_TYPE_UPLOAD = (By.ID, "meetingType-Upload")
    
    # Section 2: Meeting Details
    MEETING_LINK_INPUT = (By.ID, "meeting_link")
    FILE_UPLOAD_INPUT = (By.ID, "file-upload")
    
    # Section 3: Language Selection
    LANGUAGE_INDONESIAN = (By.ID, "meetingLang-Indonesian")
    LANGUAGE_ENGLISH = (By.ID, "meetingLang-English")
    
    # Section 4: Meeting Name
    MEETING_NAME_INPUT = (By.ID, "meeting_name")
    
    # Submit Button
    SUBMIT_BUTTON = (By.ID, "createNewMeetingBtn")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def open_meeting_creation_dialog(self):
        """Klik button untuk membuka dialog create meeting"""
        self.logger.info("Membuka dialog create new meeting")
        self.click(self.CREATE_MEETING_TRIGGER)
        self.take_screenshot("meeting_creation_dialog_opened")
    
    def create_online_meeting(self, meeting_link, language="indonesian", meeting_name=None):
        """
        Membuat online meeting
        :param meeting_link: Link meeting (GMeet/Zoom)
        :param language: 'indonesian' atau 'english'
        :param meeting_name: Nama meeting (opsional)
        """
        self.logger.info("Memulai proses create online meeting")
        
        # Pilih meeting type
        self.click(self.MEETING_TYPE_ONLINE)
        self.logger.info("Memilih meeting type: Online")
        
        # Input meeting link
        self.enter_text(self.MEETING_LINK_INPUT, meeting_link)
        self.logger.info(f"Memasukkan meeting link: {meeting_link}")
        
        # Pilih bahasa
        if language.lower() == "english":
            self.click(self.LANGUAGE_ENGLISH)
            self.logger.info("Memilih bahasa: English")
        else:
            self.click(self.LANGUAGE_INDONESIAN)
            self.logger.info("Memilih bahasa: Indonesian")
        
        # Input meeting name jika ada
        if meeting_name:
            self.enter_text(self.MEETING_NAME_INPUT, meeting_name)
            self.logger.info(f"Memasukkan meeting name: {meeting_name}")
        
        # Submit
        self.click(self.SUBMIT_BUTTON)
        self.logger.info("Mengklik button submit")
        self.take_screenshot("after_meeting_submission")
        
        # Tunggu proses selesai (sesuaikan dengan aplikasi Anda)
        time.sleep(3)  # Ganti dengan explicit wait sesuai kebutuhan
    
    def create_upload_meeting(self, file_path, language="indonesian", meeting_name=None):
        """
        Membuat meeting dengan upload file
        :param file_path: Path lengkap ke file yang akan diupload
        :param language: 'indonesian' atau 'english'
        :param meeting_name: Nama meeting (opsional)
        """
        self.logger.info("Memulai proses create meeting dengan upload file")
        
        # Pilih meeting type
        self.click(self.MEETING_TYPE_UPLOAD)
        self.logger.info("Memilih meeting type: Upload")
        
        # Upload file
        self.driver.find_element(*self.FILE_UPLOAD_INPUT).send_keys(file_path)
        self.logger.info(f"Mengupload file: {file_path}")
        
        # Pilih bahasa
        if language.lower() == "english":
            self.click(self.LANGUAGE_ENGLISH)
            self.logger.info("Memilih bahasa: English")
        else:
            self.click(self.LANGUAGE_INDONESIAN)
            self.logger.info("Memilih bahasa: Indonesian")
        
        # Input meeting name jika ada
        if meeting_name:
            self.enter_text(self.MEETING_NAME_INPUT, meeting_name)
            self.logger.info(f"Memasukkan meeting name: {meeting_name}")
        
        # Submit
        self.click(self.SUBMIT_BUTTON)
        self.logger.info("Mengklik button submit")
        self.take_screenshot("after_meeting_submission")
        
        # Tunggu proses selesai
        time.sleep(5)  # Ganti dengan explicit wait sesuai kebutuhan