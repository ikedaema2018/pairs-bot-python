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

class SetUp():

    def __init__(self):
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        self.fb_id = os.getenv("FB_ID", "")
        self.fb_pass = os.getenv("FB_PASS", "")

    def set_up_driver(self):
        options = webdriver.ChromeOptions()
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)

        if os.getenv("ENVIRONMENT", "") == "develop":
            print("dev")
            driver_path = "./binbin/chromedriver"
        else:
            print("pro")
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
        

        driver = webdriver.Chrome(
            driver_path,
            chrome_options=options
            )
        return driver

    def facebook_login(self, driver):
        driver.get("https://www.facebook.com")

        driver.find_element_by_id('email').send_keys(self.fb_id)
        driver.find_element_by_id('pass').send_keys(self.fb_pass)
        driver.find_elements_by_xpath("//input[@data-testid='royal_login_button']")[0].click()
        print("login_finish")


class PairsMain():
    def __init__(self, driver):
        self.driver = driver
        self.what_time_play = random.randint(3, 7)
        
    def random_play_module(self):
        for i in range(self.what_time_play):
            print(i)



def lambda_handler(event, context):

    try:
        set_up = SetUp()
        driver = set_up.set_up_driver()
        set_up.facebook_login(driver)

        pairs = PairsMain(driver)
        pairs.random_play_module()

        print("finish")

        return "aaa"
    except Exception as e:
        print(e, 'error occurred')
        return "bbb"

lambda_handler("foo", "bar")