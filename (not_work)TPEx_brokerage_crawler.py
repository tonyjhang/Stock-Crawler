from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import random
import time
import os

PATH = os.path.abspath(os.getcwd())
CAVFOLDER = os.path.join(PATH, 'tmp', 'csv')

def run(url:str, traget_list:list[str]):
    options = Options()
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    options.add_argument("--disable-notifications")
    options.add_argument('--user-agent=%s' % user_agent)
    download_prefs = {"download.default_directory" : CAVFOLDER}
    options.add_experimental_option("prefs", download_prefs)
    chrome = webdriver.Chrome('./web_driver/chromedriver', chrome_options=options)
    chrome.get(url)
    for stock_num in traget_list:
        print(f'Crawing stock num: {stock_num} ...')
        csv_path = os.path.join(CAVFOLDER, f'{stock_num}.csv')
        while os.path.exists(csv_path) is not True:
            chrome.get(url)
            captcha_iframe = WebDriverWait(chrome, 10).until(
                ec.presence_of_element_located(
                    (By.TAG_NAME, 'iframe')
                )
            )
            time.sleep(random.randint(3, 5))
            ActionChains(chrome).move_to_element(captcha_iframe).click().perform()
            captcha_box = WebDriverWait(chrome, 10).until(
                ec.presence_of_element_located(
                    (
                        By.ID, 'g-recaptcha-response'
                    )
                )
            )
            time.sleep(random.randint(3, 5))
            chrome.execute_script("arguments[0].click()", captcha_box)
            stock_num_input = chrome.find_element_by_id("stk_code")
            stock_num_input.send_keys(stock_num)
            chrome.find_element_by_name("btnOK").click()
            err_msg = chrome.find_element_by_id("Label_ErrorMsg").text
            try:
                chrome.find_element_by_id('HyperLink_DownloadCSV').click()
            except:
                time.sleep(3)
run(
    "https://www.tpex.org.tw/web/stock/aftertrading/broker_trading/brokerBS.php?l=zh-tw",
    ['5555', '3231']
)
