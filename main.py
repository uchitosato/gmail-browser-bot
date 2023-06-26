import time
import xlrd
import smtplib, ssl, threading, time
import poplib
import random

from email.parser import Parser
from email.message import EmailMessage

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from src.utilities.constants import MY_CONSTANT, RECIPIENT_PASSWORD, RECIPIENT_ADDRESS, SMTP_SERVER, SMTP_INTERVAL, POP3_SERVER, POP3_INTERVAL

# driver = webdriver.Chrome()

sender = []
senders_file = xlrd.open_workbook("./assets/xls/50-pcs-2020-16.6.xlsx") 
senders_list = senders_file.sheet_by_index(0)
number_of_senders = senders_list.nrows

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


def login_to_gmail(driver, index):
    email = senders_list.cell_value(index, 0)
    password = senders_list.cell_value(index, 1)
    recovery_email = senders_list.cell_value(index,2)
    driver.get("https://google.com/accounts/Login")
    time.sleep(1)
    try:
        input_email = driver.find_element(by=By.XPATH, value="//input[@name='identifier']")
        email_next = driver.find_element(by=By.ID, value="identifierNext")
        time.sleep(1)
        input_email.send_keys(email)
        time.sleep(1)
        email_next.click()
        time.sleep(1)
        try:
            input_password = driver.find_element(by=By.NAME, value="Passwd")
            password_Next = driver.find_element(by=By.ID, value="passwordNext")
            time.sleep(1)
            input_password.send_keys(password)
            time.sleep(1)
            password_Next.click()
            time.sleep(1)
            try:
                confirm_recovery_email = driver.find_element(by=By.XPATH, value="//div[@data-challengeindex='2']")
                time.sleep(1)
                confirm_recovery_email.click()
                time.sleep(1)
                try:
                    input_recovery_email = driver.find_element(by=By.ID, value="knowledge-preregistered-email-response")
                    input_recovery_email.send_keys(recovery_email)
                    input_recovery_email.send_keys(Keys.ENTER)
                    time.sleep(1)
                    try:
                        not_now_button = driver.find_element(by=By.TAG_NAME, value="button")
                        not_now_button.click()
                        time.sleep(1)
                        try:
                            driver.get("https://mail.google.com")
                        except:
                            print("Cannot find url 'mail.google.com!!!!!!!!!!!!'")
                    except:
                        try:
                            driver.get("https://mail.google.com")
                        except:
                            print("Cannot find url 'mail.google.com!!!!!!!!!!!!'")
                        print("There is no 'Not now' button!")
                except:
                    print("Cannot find element 'input_recovery_email'")
                    try:
                        driver.get("https://mail.google.com")
                    except:
                        print("Cannot find url 'mail.google.com!!!!!!!!!!!!'")
            except:
                print("There is no element have ID 'knowledge-preregistered-email-response'")
                try:
                    driver.get("https://mail.google.com")
                except:
                    print("Cannot find url 'mail.google.com!!!!!!!!!!!!'")
        except:
            print("There is no element named 'Passwd'")
            try:
                driver.get("https://mail.google.com")
            except:
                print("Cannot find url 'mail.google.com!!!!!!!!!!!!'")
    except:
        try:
            driver.get("https://mail.google.com")
        except:
            print("Cannot find url 'mail.google.com!!!!!!!!!!!!'")
    return driver

def send_mail(driver):
    try:
        driver.find_element(by=By.XPATH, value="//div[@class='T-I T-I-KE L3']").click()
        time.sleep(1)
        try:
            recipient = driver.find_element(by=By.XPATH, value="//input[@class='agP aFw']")
            recipient.send_keys(RECIPIENT_ADDRESS)
            try:
                subject = driver.find_element(by=By.NAME, value="subjectbox")
                subject.send_keys("MY First Subject")
                try:    
                    msg_body = driver.find_element(by=By.XPATH, value="//div[@aria-label='Message Body']")
                    time.sleep(1)
                    msg_body.send_keys("Are you finding full stack jobs?")
                    try:
                        send_button = driver.find_element(by=By.XPATH, value="//div[@class='T-I J-J5-Ji aoO v7 T-I-atl L3']")
                        send_button.click()
                    except:
                        print("Cannot find send button")
                except:
                    print("Cannot find msg body!")
            except:
                print("cannot find subject!")
        except:
            print("Cannot find receipient!")
    except:
        print("Cannot find 'Compose' button'!")
    return driver


def send_in_loop():
    for i in range(0, number_of_senders):
        driver = driver_chrome_incognito()
        time.sleep(1)
        send_mail(login_to_gmail(driver=driver, index=i))
        time.sleep(10)
        driver.close()

def listening_unread_emails():
    for i in range(0, number_of_senders):
        driver = driver_chrome_incognito()
        time.sleep(1)
        

def main():
    thread_sender = threading.Thread(target=send_in_loop)
    thread_sender.start()
    thread_sender.join()

if __name__ == '__main__':
    main()

