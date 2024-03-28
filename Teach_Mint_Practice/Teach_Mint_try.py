from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from helium import *
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import time

username = "username"
password = "password"

default_options = ["--disable-extensions", "--disable-user-media-security=true",
                   "--allow-file-access-from-files", "--use-fake-device-for-media-stream",
                   "--use-fake-ui-for-media-stream", "--disable-popup-blocking",
                   "--disable-infobars", "--enable-usermedia-screen-capturing",
                   "--disable-dev-shm-usage", "--no-sandbox",
                   "--auto-select-desktop-capture-source=Screen 1",
                   "--disable-blink-features=AutomationControlled"]
headless_options = ["--headless", "--use-system-clipboard",
                    "--window-size=1920x1080"]


def browser_options(chrome_type):
    webdriver_options = webdriver.ChromeOptions()
    notification_opt = {"profile.default_content_setting_values.notifications": 1}
    webdriver_options.add_experimental_option("prefs", notification_opt)

    if chrome_type == "headless":
        var = default_options + headless_options
    else:
        var = default_options

    for d_o in var:
        webdriver_options.add_argument(d_o)
        return webdriver_options


def get_webdriver_instance(browser=None):
    base_url = "https://accounts.teachmint.com/"
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "normal"
    driver = webdriver.Chrome(options=browser_options(browser))
    driver.command_executor._commands["send_command"] = ("POST",
                                                         '/session/$sessionId/chromium/send_com,mand')
    driver.maximize_window()
    driver.get(base_url)
    set_driver(driver)
    return driver


def enter_phone_number_otp(driver, creds):
    driver.find_element("xpath", "//input[@type='text']").send_keys(creds[0])
    time.sleep(1)
    print("entered user phone number {}".format(creds[0]))
    driver.find_element("id", "send-otp-btn-id").click()
    WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.CSS_SELECTOR, "loader")))
    WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.CLASS_NAME, "loader")))
    time.sleep(1)
    _input_otp_field = "//input[@data-group-idx='{}']"

    for i, otp in enumerate(creds[1]):
        otp_field = _input_otp_field.format(str(i))
        write(otp, into=S(otp_field))

    print("entered otp {}".format(creds[1]))
    time.sleep(1)
    driver.find_element("id", "submit-otp-btn-id").click()
    time.sleep(2)

    driver.find_element("xpath", '//img[@alt="arrow"]').click()
    WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.CSS_SELECTOR, "loader")))
    WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.CLASS_NAME, "loader")))
    time.sleep(1)
    print("successfully entered user phone number and otp")


def Navigating_To_Certificates(driver):
    print("navigating to get the certificate.....")
    action_object = ActionChains(driver)
    element = driver.find_element("xpath",'//div[text()="Administration"]')
    action_object.move_to_element(element).perform()
    driver.find_element("xpath",'//span[@data-qa="icon-administrator"]').click()
    driver.find_element("xpath",'//a[text()="Certificates"]').click()
    time.sleep(2)


def Selecting_Certificate_Type(driver):
    driver.find_element("xpath",'//h6[text()="School leaving certificate"]').click()
    print("certificate selected....")
    time.sleep(2)


def Clicking_on_generate(driver):
    driver.find_element("xpath",'//div[text()="Generate"]').click()
    print("generated the certificate")


def Searching_student(driver):
    print("searching the student")
    driver.find_element("xpath",'// input[ @ name = "search"]').send_keys("sam")
    driver.find_element("xpath",'//div[text()="Generate"]').click()
    print("student selected and certificate generated")


def Updating_remarks(driver):
    time.sleep(2)
    driver.find_element("xpath",'//input[@placeholder="Date"]').send_keys("28/03/2024")
    driver.find_element("xpath",'//input[@placeholder="Remarks"]').send_keys("Good Performance in academic as well sports")
    print("remarks updated")


def Downloading_certificate(driver):
    driver.find_element("xpath",'//div[text()="Generate"]').click()
    time.sleep(10)
    driver.find_element("xpath",'//div[text()="Download"]').click()
    time.sleep(50)
    print("certificate downloaded")


def Validating_history_of_Certificate(drive):
    verify_certificate = drive.find_element("xpath",'//p[text()="Student Details"]').is_displayed()
    assert verify_certificate, "history if certificate not available"
    print("validation succussfull")


def login(admin_credentials=["0000020232", "120992", "@Automation-2"], account_name="@Automation-2"):
    driver = get_webdriver_instance()
    WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.CSS_SELECTOR, "loader")))
    WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.CLASS_NAME, "loader")))
    time.sleep(1)
    enter_phone_number_otp(driver, admin_credentials)

    dashboard_xpath = "//a[text()='Dashboard']"
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, dashboard_xpath)))
    time.sleep(20)
    refresh()
    time.sleep(10)
    driver.implicitly_wait(10)
    Navigating_To_Certificates(driver)
    Selecting_Certificate_Type(driver)
    Clicking_on_generate(driver)
    Searching_student(driver)
    Updating_remarks(driver)
    time.sleep(2)
    Downloading_certificate(driver)
    time.sleep(2)
    Validating_history_of_Certificate(driver)
    return driver


def main():
    login()


if __name__ == "__main__":
    print("start")
    main()
    print("end")
