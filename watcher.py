import time
import xlrd
import threading, time
import random
import pyautogui
import pyperclip

from email.parser import Parser
from email.message import EmailMessage

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from src.utilities.constants import PROXY_IP, PROXY_PORT, RECIPIENT_ADDRESS, SMTP_SERVER, SMTP_INTERVAL, POP3_SERVER, POP3_INTERVAL
from src.utilities.select_message_for_sending import select_random_msg, read_file_line_by_line, update_file
# driver = webdriver.Chrome()

url_senders = "./assets/txt/senders.txt"
url_ricipients = "./assets/txt/recipients.txt"
url_links = "./assets/txt/links.txt"
url_message = "./assets/txt/First Message 200 Eng.txt"
url_total_sent = "./assets/txt/total_sent.txt"
url_total_reply = "./assets/txt/total_reply.txt"



def copy(string):
    pyperclip.copy(string)

def driver_chrome_incognito():
    from undetected_chromedriver import Chrome, ChromeOptions
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--encoding=UTF-8')
    chrome_options.add_argument("--log-level=OFF")
    chrome_options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
    driver = Chrome(options=chrome_options, version_main = 114)
    return driver


def login_to_gmail(driver, email, password, recovery_email):
    driver.get("https://gmail.com")
    time.sleep(1)
    try:
        input_email = driver.find_element(by=By.XPATH, value="//input[@name='identifier']")
        email_next = driver.find_element(by=By.ID, value="identifierNext")
        time.sleep(1)
        input_email.send_keys(email)
        time.sleep(1)
        email_next.click()
        time.sleep(2)
        try:
            input_password = driver.find_element(by=By.NAME, value="Passwd")
            time.sleep(1)
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
                    except:
                        pass
                except:
                    print("Cannot find element 'input_recovery_email'")
            except:
                pass
        except:
            pass
    except:
        pass
    return driver

def send_mail(driver, msg_content, recipient_email):  
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
                subject_content ='{0}'.format(recipient_email.split('@')[0]).strip().capitalize()
                subject.send_keys(subject_content)
                time.sleep(1)
                try:    
                    msg_body = driver.find_element(by=By.XPATH, value="//div[@aria-label='Message Body']")
                    time.sleep(1)
                    time.sleep(1)
                    ActionChains(driver=driver).move_to_element(msg_body).click().perform()
                    copy(msg_content)
                    msg_body.send_keys(Keys.CONTROL + "v")
                    time.sleep(2)
                    try:
                        send_button = driver.find_element(by=By.XPATH, value="//div[@class='T-I J-J5-Ji aoO v7 T-I-atl L3']")
                        send_button.click()
                        print("---------------------------------------------------------->")
                        total_sent = read_file_line_by_line(url_total_sent)[0]
                        total_reply = read_file_line_by_line(url_total_reply)[0]
                        print("<----------Total sent: " + total_sent + " Total reply: " + total_reply + "---------->")
                        time.sleep(2)

                    except:
                        pass
                except:
                    pass
            except:
                pass
        except:
            pass
    except:
        pass

    return driver


def watch_unread_gmails(email, password, recovery_email):
    total_reply = int(read_file_line_by_line(url_total_reply)[0])
    init_driver = driver_chrome_incognito()
    driver = login_to_gmail(driver=init_driver, email=email, password=password, recovery_email=recovery_email)
    try:
        inbox_button = driver.find_element(by=By.XPATH, value="//div[@class='aio UKr6le']")
        inbox_button.click()
        time.sleep(5)
        try:
            unread_gmails = driver.find_elements(by=By.XPATH, value="//tr[@class='zA zE']")
            time.sleep(1)
            for email in unread_gmails:
                # email_subject = email.find_element(by=By.XPATH, value='//span[@class="bqe"]').text()
                email_sender = email.find_element(by=By.XPATH, value='//span[@class="zF"]').get_attribute('email')
                recipients = read_file_line_by_line("./assets/txt/recipients_backup.txt")
                if email_sender.strip() + '\n' in recipients:
                    # print("This sender is in recipients!")
                    reply_msg = select_random_msg("assets/txt/Reply Message 200 Eng.txt").split(":")[0] + " : " + select_random_msg("assets/txt/links.txt")
                    send_mail(driver=driver, msg_content=reply_msg, recipient_email=email_sender)
                    total_reply += 1
                    with open(url_total_reply, "w", encoding="utf-8") as reply:
                        reply.write(format(total_reply))
                    print(format(total_reply) + " recipients replied to this bot!")
                    time.sleep(1)
                    ActionChains(driver=driver).move_to_element(email).click().perform()
                    time.sleep(1)
                    ActionChains(driver=driver).move_to_element(inbox_button).click().perform()
                    time.sleep(1)
                # email_body = email.find_element_by_xpath('.//span[@class="y2"]').text
        except:
            # print("cannot find such class!")
            pass
    except:
        # print("cannot find inbox button")
        pass

    driver.close()

def main():
    senders = read_file_line_by_line(url_senders)
    while True:
        for i in range(0, len(senders)):
            sender_info = senders[len(senders) - i -1].split(",")
            Email = sender_info[0]
            Password = sender_info[1]
            Recovery = sender_info[2]
            watch_unread_gmails(email=Email, password=Password, recovery_email=Recovery)

if __name__ == '__main__':
    main()

