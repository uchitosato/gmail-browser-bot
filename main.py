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

from src.utilities.constants import PROXY_IP, PROXY_PORT, RECIPIENT_ADDRESS, SMTP_SERVER, SMTP_INTERVAL, POP3_SERVER, POP3_INTERVAL
from src.utilities.select_message_for_sending import select_random_msg, read_file_line_by_line
# driver = webdriver.Chrome()

sender = []
recipients = read_file_line_by_line("./assets/txt/recipients test.txt")
number_of_recipients = len(recipients)
recipients_backup = recipients
senders_file = xlrd.open_workbook("./assets/xls/50-pcs-2020-16.6.xlsx") 
senders_list = senders_file.sheet_by_index(0)
number_of_senders = senders_list.nrows

total_sent = 0
total_reply = 0
total_recive = 0


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
    # chrome_options.add_argument('--proxy-server={}:{}'.format(PROXY_IP, PROXY_PORT))
    # Add any additional options as needed

    driver = webdriver.Chrome(options=chrome_options)
    return driver


def login_to_gmail(driver, index):
    relogin_driver = driver
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
                            driver.get("https://mail.google.com/mail/u/0/#inbox")
                        except:
                            # print("Cannot find url 'mail.google.com!!!!!!!!!!!!'")
                            pass
                    except:
                        try:
                            driver.get("https://mail.google.com/mail/u/0/#inbox")
                        except:
                            # print("Cannot find url 'mail.google.com!!!!!!!!!!!!'")
                            pass
                        # print("There is no 'Not now' button!")
                        pass
                except:
                    print("Cannot find element 'input_recovery_email'")
                    try:
                        driver.get("https://mail.google.com/mail/u/0/#inbox")
                    except:
                        # print("Cannot find url 'mail.google.com!!!!!!!!!!!!'")
                        pass
            except:
                # print("There is no element have ID 'knowledge-preregistered-email-response'")
                try:
                    driver.get("https://mail.google.com/mail/u/0/#inbox")
                except:
                    # print("Cannot find url 'mail.google.com!!!!!!!!!!!!'")
                    pass
        except:
            print("There is no element named 'Passwd'")
            # login_to_gmail(driver=relogin_driver, index=index)
            try:
                driver.get("https://mail.google.com/mail/u/0/#inbox")
            except:
                # print("Cannot find url 'mail.google.com!!!!!!!!!!!!'")
                pass
    except:
        try:
            driver.get("https://mail.google.com/mail/u/0/#inbox")
        except:
            # print("Cannot find url 'mail.google.com!!!!!!!!!!!!'")
            pass
    return driver

def send_mail(driver, msg_content, recipient_email, is_reply):  
    global total_sent
    global total_reply
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
                    time.sleep(2)
                    # print("entered message")
                    try:
                        send_button = driver.find_element(by=By.XPATH, value="//div[@class='T-I J-J5-Ji aoO v7 T-I-atl L3']")
                        send_button.click()
                        print("---------------------------------------------------------->")
                        if is_reply == "no_reply":
                            total_sent += 1
                            print("This bot totally sent: " + format(total_sent) + " emails!")
                        else:
                            total_reply += 1
                            print("This bot totally replied: " + format(total_reply) + " emails!")
                            
                        print("<----------Total sent: " + format(total_sent) + " Total reply: " + format(total_reply) + "---------->")

                    except:
                        # print("Cannot find send button")
                        pass
                except:
                    # print("Cannot find msg body!")
                    pass
            except:
                # print("cannot find subject!")
                pass
        except:
            # print("Cannot find receipient!")
            pass
    except:
        # print("Cannot find 'Compose' button'!")
        pass
    return driver

def watch_unread_gmails(index):
    global total_recive
    init_driver = driver_chrome_incognito()
    driver = login_to_gmail(driver=init_driver, index=index)
    while True:
        try:
            inbox_button = driver.find_element(by=By.XPATH, value="//div[@class='aio UKr6le']")
            inbox_button.click()
            time.sleep(15)
            try:
                unread_gmails = driver.find_elements(by=By.XPATH, value="//tr[@class='zA zE']")
                time.sleep(1)
                for email in unread_gmails:
                    # email_subject = email.find_element(by=By.XPATH, value='//span[@class="bqe"]').text()
                    email_sender = email.find_element(by=By.XPATH, value='//span[@class="zF"]').get_attribute('email')
                    recipients = read_file_line_by_line("./assets/txt/recipients test.txt")
                    if email_sender.strip() + '\n' in recipients:
                        # print("This sender is in recipients!")
                        reply_msg = select_random_msg("assets/txt/Reply Message 200 Eng.txt").split(":")[0] + " : " + select_random_msg("assets/txt/links test.txt")
                        send_mail(driver=driver, msg_content=reply_msg, recipient_email=email_sender, is_reply="reply")
                        print("------------------------------------------------->")
                        total_recive += 1
                        print(format(total_recive) + " recipients replied to this bot!")
                        ActionChains(driver=driver).move_to_element(email).click().perform()
                        time.click(1)
                    time.sleep(1)
                    # email_body = email.find_element_by_xpath('.//span[@class="y2"]').text
            except:
                # print("cannot find such class!")
                pass
        except:
            # print("cannot find inbox button")
            pass

def send_in_loop():
    number_of_recipients = len(recipients_backup)
    while True:
        try:
            if number_of_recipients == 0:
                break
            else:
                for i in range(0, number_of_senders):
                    driver = driver_chrome_incognito()
                    time.sleep(1)
                    login_driver = login_to_gmail(driver=driver, index=i)
                    msg_content = select_random_msg("assets/txt/First Message 200 Eng.txt")
                    try:
                        random_number = random.randrange(0, number_of_recipients)
                        send_mail(driver=login_driver, msg_content=msg_content, recipient_email=recipients[random_number].strip(), is_reply="no_reply")
                        recipients_backup.remove(recipients_backup[random_number])
                        number_of_recipients = len(recipients_backup)
                        time.sleep(30)
                        driver.close()
                    except:
                        pass
        except:
            pass


def main():
    thread_sender = threading.Thread(target=send_in_loop)
    thread_sender.start()
    thread_sender.join()

    for i in range(0, 2):
        time.sleep(2)
        threading.Thread(target=lambda:watch_unread_gmails(index=i)).start()

if __name__ == '__main__':
    main()

