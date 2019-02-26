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

    def pairs_login(self, driver):
        driver.get("https://pairs.lv/#/login")


class PairsMain():
    def __init__(self, driver):
        self.driver = driver
        self.what_time_play = random.randint(3, 7)
        time.sleep(3)
        self.driver.get("https://pairs.lv/#/search/grid/2")
        time.sleep(5)

    def kill_popup(self):
        for i in range(3):
            try:
                time.sleep(random.randint(1, 3))
                self.driver.find_elements_by_class_name('modal_close')[0].click()
            except Exception as e:
                print("no popup ")
                print(e)
                break


    def random_play_module(self):
        for i in range(self.what_time_play):
            self.kill_popup()
            pairs_comu = PairsComu(self.driver)
            pairs_comu.pairs_comu_main()

class PairsComu():
    def __init__(self, driver):
        self.driver = driver

    def comu_page_for_grid(self):
        self.driver.find_elements_by_link_text("コミュニティを探す")[0].click()

    def joined_comu_enter(self, comu_number):
        self.driver.find_elements(By.XPATH,
                                  "//ul[@class='my_community_list']/li")[comu_number].find_element_by_class_name('community_link').click()

    def pairs_comu_main(self):
        self.comu_page_for_grid()
        time.sleep(3)
        game_number = random.randint(0, 4)
        
        self.joined_comu_enter(game_number)
        time.sleep(random.randint(3, 6))



def lambda_handler(event, context):

    try:
        set_up = SetUp()
        driver = set_up.set_up_driver()
        set_up.facebook_login(driver)
        set_up.pairs_login(driver)

        pairs = PairsMain(driver)
        pairs.random_play_module()

        print("finish")

        return "success"
    except Exception as e:
        print(e, 'error occurred')
        return "success"

lambda_handler("foo", "bar")