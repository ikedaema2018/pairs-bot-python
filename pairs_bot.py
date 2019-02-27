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
            options.add_argument("--headless")
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
        self.kill_popup()
        time.sleep(5)
        self.random_play_module()

    def kill_popup(self):
        for i in range(3):
            try:
                time.sleep(random.randint(1, 3))
                modals = self.driver.find_element_by_xpath("//div[@class='box_modal_window modal_animation pickup_modal']")
                time.sleep(2)
                modals.find_element_by_tag_name("a").click()
            except Exception as e:
                print("no popup ")
                print(e)
                time.sleep(2)
                break


    def random_play_module(self):
        # TODO いくつかのモジュールを用意
        for i in range(self.what_time_play):
            pairs_comu = PairsComu(self.driver)
            pairs_comu.pairs_comu_main()

class PairsComu():
    def __init__(self, driver):
        self.driver = driver

    def comu_page_for_grid(self):
        self.driver.get("https://pairs.lv/#/community")


    class SeeMyComu():
        def __init__(self, driver):
            self.driver = driver

        def joined_comu_enter(self, comu_number):
            self.driver.find_elements(By.XPATH,
                                      "//ul[@class='my_community_list']/li")[comu_number].find_element_by_class_name(
                'community_link').click()
            time.sleep(random.randint(4, 8))

        def joined_comu_member_click(self):

            for _ in range(random.randint(3, 10)):

                time.sleep(random.randint(4, 8))
                joined_comu_members = self.driver.find_elements(By.XPATH, "//ul[@class='list_view_users']/li")
                what_time_click_joined_comu_member = random.randint(0, len(joined_comu_members) - 1)

                for _ in range(what_time_click_joined_comu_member):
                    print(len(joined_comu_members))
                    time.sleep(random.randint(3, 7))
                    click_member = random.randint(0, len(joined_comu_members) - 1)
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    joined_comu_members.pop(click_member).find_element_by_tag_name("a").click()
                    # TODO あとで0~20秒に
                    time.sleep(random.randint(2, 7))
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    self.driver.find_element_by_class_name("box_modal_personal_view").find_element_by_tag_name("a").click()
                    time.sleep(random.randint(2, 7))

                time.sleep(random.randint(0, 5))
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                self.driver.find_element_by_xpath(
                    "//a[@class='pager_next pager_item button_c button_white_a']").click()

        def see_my_comu_main(self):
            try:
                # TODO 2列目のゲームナンバーに行く処理も書く
                game_number = random.randint(0, 4)
                self.joined_comu_enter(game_number)
                time.sleep(random.randint(3, 6))
                self.joined_comu_member_click()
            except Exception as e:
                print(e, 'error occurred')
                time.sleep(30)



    def pairs_comu_main(self):
        self.comu_page_for_grid()
        time.sleep(3)
        game_number = random.randint(0, 4)

        see_comu = self.SeeMyComu(self.driver)
        see_comu.see_my_comu_main()

# TODO 全てのサブモジュールの共通関数を支配するクラスを作成



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
        time.sleep(30)
        return "failure"

lambda_handler("foo", "bar")