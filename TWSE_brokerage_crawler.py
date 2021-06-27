from PIL import Image, ImageFilter
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from base_loger import log
from Crawler import Crawler
from settings import IMG_FOLDER, CSV_FOLDER

import os
import time
import random
import asyncio
import validators

loop = asyncio.get_event_loop()

class TWSE_Brokerage_crawler(Crawler):
    def __init__(self, url):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-notifications")
        download_prefs = {"download.default_directory" : CSV_FOLDER}
        options.add_experimental_option("prefs", download_prefs)
        self.chrome = webdriver.Chrome('./web_driver/chromedriver', chrome_options=options)
        
        if validators.url(url) is not True:
            raise SyntaxError
        self.url = url
    
    def crack_captcha(self, img_path:str) -> str:
        try:
            import pytesseract
        except:
            log.error('Cant import pytesseract, check tesseract is installed?')
            raise ImportError
        if os.path.isfile(img_path) is not True:
            raise NameError

        img = Image.open(img_path)
        img = img.filter(ImageFilter.MinFilter(3))
        ans = pytesseract.image_to_string(img, lang='eng', config='--psm 10')
        return ans.strip().replace(" ","")
    
    @staticmethod
    def corp(img_path:str, range:tuple):
        if os.path.isfile(img_path) is not True:
            raise NameError
        img = Image.open(img_path)
        corp_img = img.crop(range)
        corp_img.save(img_path)
    
    async def crawl_data(self, stock_num:str):
        if len(stock_num) != 4:
            log.error(f'${stock_num} is not correct format')
            raise NameError
        try:
            int(stock_num)
        except:
            log.error(f'${stock_num} is not correct format')
            raise SyntaxError

        csv_path = os.path.join(CSV_FOLDER, f'{stock_num}.csv')
        counter = 0
        while os.path.exists(csv_path) is not True:
            counter += 1
            if counter > 100:
                log.error('Try too much time')
                raise
            time.sleep(random.randint(2, 5))
            self.chrome.get(self.url)
            self.chrome.switch_to.frame('page1')

            #snapshoot web pag
            img_path = os.path.join(IMG_FOLDER, f'{stock_num}_web_info.png')
            self.chrome.get_screenshot_as_file(img_path)

            #corp captcha and (50, 200, 250, 260) is captcha index
            self.corp(img_path, (50, 200, 250, 260))

            #script for input data
            stock_num_input = self.chrome.find_element_by_name("TextBox_Stkno")
            stock_num_input.send_keys(stock_num)
            captcha_input = self.chrome.find_element_by_name("CaptchaControl1")
            captcha_input.send_keys(
                self.crack_captcha(img_path)
            )
            self.chrome.find_element_by_name("btnOK").click()
            err_msg = self.chrome.find_element_by_id("Label_ErrorMsg").text
            os.remove(img_path)
            if err_msg == '查無資料':
                log.info(f'There is no data from TWSE')
                print("No data!!")
                break
            #check captcha is worked or not
            try:
                self.chrome.find_element_by_id('HyperLink_DownloadCSV').click()
            except:
                log.info(f'captcha validation fail, need retry')
                #prevent too often run script
                await asyncio.sleep(random.randint(3, 5))




