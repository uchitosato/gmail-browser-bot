import time
import xlrd
import threading, time
import random
import pyautogui

from email.parser import Parser
from email.message import EmailMessage

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from src.utilities.constants import MY_CONSTANT, RECIPIENT_PASSWORD, RECIPIENT_ADDRESS, SMTP_SERVER, SMTP_INTERVAL, POP3_SERVER, POP3_INTERVAL
from src.utilities.select_message_for_sending import select_random_msg, read_file_line_by_line
# driver = webdriver.Chrome()

sender = []
recipients = read_file_line_by_line("./assets/txt/recipients test.txt")
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

def send_mail(driver, msg_content, recipient_email):
    print(msg_content)
    try:
        driver.find_element(by=By.XPATH, value="//div[@class='T-I T-I-KE L3']").click()
        time.sleep(1)
        try:
            recipient = driver.find_element(by=By.XPATH, value="//input[@class='agP aFw']")
            recipient.send_keys(recipient_email)
            time.sleep(1)
            try:
                subject = driver.find_element(by=By.NAME, value="subjectbox")
                subject_content ='{0}'.format(recipient_email.split('@')[0]).strip()
                subject.send_keys(subject_content)
                time.sleep(1)
                try:    
                    msg_body = driver.find_element(by=By.XPATH, value="//div[@aria-label='Message Body']")
                    time.sleep(1)
                    ActionChains(driver=driver).move_to_element(msg_body).click().perform()
                    ActionChains(driver=driver).send_keys(msg_content).perform()
                    time.sleep(5)
                    print("entered message")
                    try:
                        send_button = driver.find_element(by=By.XPATH, value="//div[@class='T-I J-J5-Ji aoO v7 T-I-atl L3']")
                        send_button.click()
                        print("successly sent")
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

def watch_unread_gmails(index):
    init_driver = driver_chrome_incognito()
    while True:
        driver = login_to_gmail(driver=init_driver, index=index)
        try:
            inbox_button = driver.find_element(by=By.XPATH, value="//div[@class='aio UKr6le']")
            print("found!!!")
            inbox_button.click()
            print("clicked!!!")
            try:
                unread_gmails = driver.find_elements(by=By.XPATH, value="//tr[@class='zA zE']")
                print("find class")
                time.sleep(5)
                for email in unread_gmails:
                    # email_subject = email.find_element(by=By.XPATH, value='//span[@class="bqe"]').text()
                    email_sender = email.find_element(by=By.XPATH, value='//span[@class="zF"]').get_attribute('email')
                    print(email_sender)
                    if email_sender.strip() + '\n' in recipients:
                        print("equal")
                        reply_msg = select_random_msg("assets/txt/Reply Message 200 Eng.txt").split(":")[0] + " : " + select_random_msg("assets/txt/links test.txt")
                        send_mail(driver=driver, msg_content=reply_msg, recipient_email=email_sender)
                        print("replied!!!")
                        ActionChains(driver=driver).move_to_element(email).click().perform()
                        time.click(1)
                    time.sleep(1)
                    # email_body = email.find_element_by_xpath('.//span[@class="y2"]').text
            except:
                print("cannot find such class!")
        except:
            print("cannot find inbox button")

def send_in_loop():
    for i in range(0, 3):
        driver = driver_chrome_incognito()
        time.sleep(1)
        login_driver = login_to_gmail(driver=driver, index=i)
        msg_content = select_random_msg("assets/txt/First Message 200 Eng.txt")
        send_mail(driver=login_driver, msg_content=msg_content, recipient_email=recipients[i].strip())
        time.sleep(10)
        driver.close()


def main():
    thread_sender = threading.Thread(target=send_in_loop)
    thread_sender.start()
    thread_sender.join()

    for i in range(0, 3):
        time.sleep(10)
        threading.Thread(target=lambda:watch_unread_gmails(index=i)).start()

if __name__ == '__main__':
    main()

