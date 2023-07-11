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

def send_in_loop():
    total_sent = int(read_file_line_by_line(url_total_sent)[0])
    senders = read_file_line_by_line(url_senders)
    recipients  = read_file_line_by_line(url_ricipients)
    number_recipients = len(recipients)
    while number_recipients != 0:
        for sender in senders:
            sender_info = sender.split(",")
            Email = sender_info[0]
            Password = sender_info[1]
            Recovery = sender_info[2]
            Driver = driver_chrome_incognito()
            login = login_to_gmail(driver=Driver, email=Email, password=Password, recovery_email=Recovery)
            for i in range(0, 10):
                Message = select_random_msg(url_message)
                if number_recipients == 0:
                    break
                elif number_recipients <= i:
                    Recipient = recipients[0]
                    send_mail(driver=login, msg_content=Message, recipient_email=Recipient)
                    print(Email + Recipient + "\n")
                    update_file(url_ricipients, 1)
                    recipients = read_file_line_by_line(url_ricipients)
                    number_recipients = len(recipients)
                    total_sent += 1
                else:
                    Recipient = recipients[i].strip()
                    send_mail(driver=login, msg_content=Message, recipient_email=Recipient)
                    update_file(url_ricipients, i+1)
                    recipients = read_file_line_by_line(url_ricipients)
                    number_recipients = len(recipients)
                    total_sent += 1
                with open(url_total_sent, "w", encoding="utf-8") as total:
                    total.write(format(total_sent))
            login.close()


    print("Sent to all recipients!")
    

def main():
    send_in_loop()

if __name__ == '__main__':
    main()

