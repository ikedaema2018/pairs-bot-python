# -*- coding: utf-8 -*-

import os
from datetime import datetime
import time
import random
import sys
import json
from selenium.webdriver import Firefox, FirefoxOptions
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

def scraping():
    print(os.getenv("FB_ID", ""))
    print(os.getenv("FB_PASS", ""))
    I=1
    options = FirefoxOptions()
    # ヘッドレスモードを有効にする（次の行をコメントアウトすると画面が表示される）。
    # options.add_argument('-headless')
    # FirefoxのWebDriverオブジェクトを作成する。
    driver = Firefox(options=options, log_path=os.path.devnull)
    driver.get("https://www.facebook.org")
    driver.find_element_by_id('email').send_keys(fb_id)
    driver.find_element_by_id('pass').send_keys(fb_pass)
    driver.find_element_by_id('u_0_3').click()
    assert "Facebook" in driver.title
        
scraping()