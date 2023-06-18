from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def driver_chrome_incognito():


    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation detection
    chrome_options.add_argument("--disable-infobars")  # Disable infobars
    chrome_options.add_argument("--disable-notifications")  # Disable notifications
    chrome_options.add_argument("--disable-popup-blocking")  # Disable popup blocking
    chrome_options.add_argument("--disable-extensions")  # Disable extensions
    chrome_options.add_argument("--disable-dev-shm-usage")  # Disable /dev/shm usage
    chrome_options.add_argument("--disable-browser-side-navigation")  # Disable browser side navigation
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument("--no-sandbox")  # Disable sandbox mode
    chrome_options.add_argument("--ignore-certificate-errors")  # Ignore certificate errors
    chrome_options.add_argument("--incognito")

    # Add any additional options as needed

    driver = webdriver.Chrome(options=chrome_options)
    return driver

driver = driver_chrome_incognito()
time.sleep(1)

driver.get("https://google.com/accounts/Login")

time.sleep(1)
input_email = driver.find_element(by=By.XPATH, value="//input[@name='identifier']")
email_next = driver.find_element(by=By.ID, value="identifierNext")
time.sleep(1)
input_email.send_keys("afoucher7255@gmail.com")
time.sleep(1)
email_next.click()
time.sleep(1)
input_password = driver.find_element(by=By.XPATH, value="//input[@name='password']")
time.sleep(1)
password_Next = driver.find_element(by=By.ID, value="passwordNext")
time.sleep(1)
input_password.send_keys("aksuifaksuif")
time.sleep(1)
password_Next.click()
time.sleep(20)

