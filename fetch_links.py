# -*- coding: utf-8 -*-

import os
from datetime import datetime
import time
import random
import sys
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

#自動ログイン開始
fb_id = os.getenv("FB_ID", "")
fb_pass = os.getenv("FB_PASS", "")

if os.getenv("ENVIRONMENT", "") == "develop":
    driver_path = "./binbin/chromedriver"
else:
    driver_path = "./bin/chromedriver"



def lambda_handler(event, context):
    options = webdriver.ChromeOptions()

    if os.getenv("ENVIRONMENT", "") == "develop":
        driver_path = "./binbin/chromedriver"
    else:
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

    driver = webdriver.Chrome(
        driver_path,
        chrome_options=options
        )

    driver.get("https://www.facebook.org")
    driver.find_element_by_id('email').send_keys(fb_id)
    driver.find_element_by_id('pass').send_keys(fb_pass)
    driver.find_element_by_id('u_0_2').click()

lambda_handler("foo", "bar")