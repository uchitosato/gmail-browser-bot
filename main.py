import time

from selenium import webdriver
from src.utilities.constants import MY_CONSTANT
from selenium.webdriver.common.keys import Keys



driver = webdriver.Chrome()

def main():
    driver.get("https://www/python.org")
    time.sleep(30)
    # driver.find_element("Connect Wallet")
    # print(MY_CONSTANT)

if __name__ == '__main__':
    main()
