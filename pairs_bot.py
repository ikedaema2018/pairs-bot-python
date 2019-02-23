# -*- coding: utf-8 -*-

import os
from datetime import datetime
import time
import random
import sys
import json
import asyncio

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

from os.path import join, dirname
from dotenv import load_dotenv

def lambda_handler(event, context):

    try:
        #自動ログイン開始
        options = webdriver.ChromeOptions()
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)

        if os.getenv("ENVIRONMENT", "") == "develop":
            driver_path = "./binbin/chromedriver"
        else:
            driver_path = "./bin/chromedriver"
            # のちほどダウンロードするバイナリを指定
            options.binary_location = "./bin/headless-chromium"


        # headlessで動かすために必要なオプション
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280x1696")
        options.add_argument("--disable-application-cache")
        options.add_argument("--disable-infobars")
        options.add_argument("--no-sandbox")
        options.add_argument("--hide-scrollbars")
        options.add_argument("--enable-logging")
        options.add_argument("--log-level=0")
        options.add_argument("--single-process")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--homedir=/tmp")

        fb_id = os.getenv("FB_ID", "")
        fb_pass = os.getenv("FB_PASS", "")
        

        driver = webdriver.Chrome(
            driver_path,
            chrome_options=options
            )
        # 5の部分をランダムにする
        # driver.manage().timeouts().implicitlyWait(5, TimeUnit.SECONDS);

        
        driver.get("https://www.facebook.com")
        driver.find_element_by_id('email').send_keys(fb_id)
        driver.find_element_by_id('pass').send_keys(fb_pass)
        driver.find_elements_by_xpath("//input[@data-testid='royal_login_button']")[0].click()

        print("finish")
        return "aaa"
    except Exception as e:
        print(e, 'error occurred')
        return "bbb"

lambda_handler("foo", "bar")