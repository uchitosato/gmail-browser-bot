import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


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

def login_to_gmail(driver):
    driver.get("https://google.com/accounts/Login")
    time.sleep(1)
    try:
        input_email = driver.find_element(by=By.XPATH, value="//input[@name='identifier']")
        email_next = driver.find_element(by=By.ID, value="identifierNext")
        time.sleep(1)
        input_email.send_keys("azubikeemmanuel200@gmail.com")
        time.sleep(1)
        email_next.click()
        time.sleep(1)
        try:
            input_password = driver.find_element(by=By.NAME, value="Passwd")
            password_Next = driver.find_element(by=By.ID, value="passwordNext")
            time.sleep(1)
            input_password.send_keys("Wylrzdaeggcm")
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
                    input_recovery_email.send_keys("kzapelhaqhsz451556@kaishime.com")
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
            recipient.send_keys("uchitosato@gmail.com")
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

def sign_out(driver):
    try:
        account_button = driver.find_element(by=By.XPATH, value="//a[@class='gb_d gb_Fa gb_x']")
        account_button.click()
        try:
            sign_out_button = driver.find_element(by=By.XPATH, value="//a[@class='V5tzAf jFfZdd']")
            sign_out_button.click()
        except:
            print("Cannot find sign out button!")
    except:
        print("Cannot find account button!")
    time.sleep(5)    
    return driver

def watch_unread_gmails(driver):
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
                email_subject = email.find_element(by=By.XPATH, value='//span[@class="bqe"]').text
                email_sender = email.find_element(by=By.XPATH, value='//span[@class="zF"]').get_attribute('email')
                if email_sender == "uchitosato@gmail.com":
                    send_mail(driver=driver)
                    email.click()
                    
                    inbox_button.click()
                time.sleep(5)
                # email_body = email.find_element_by_xpath('.//span[@class="y2"]').text
                print(email_subject, email_sender)
                time.sleep(1000)
        except:
            print("cannot find such class!")
            time.sleep(1000)
    except:
        print("cannot find inbox button")

driver = driver_chrome_incognito()
time.sleep(1)
gmail_driver = login_to_gmail(driver)
sender_driver = send_mail(gmail_driver)
time.sleep(5)
read_driver = watch_unread_gmails(sender_driver)
time.sleep(5)
sign_out_driver = sign_out(read_driver)
time.sleep(5)
sign_out_driver.close()
time.sleep(1000)