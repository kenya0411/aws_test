import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from utils.common import *
from utils.option import *




def lambda_handler(event, context):

    print("Lambda functionを開始")

    URL = "https://www.yahoo.co.jp/"

    browser = get_driver()


    browser.get(URL)
    bucket_name = 'selenium-work-python'
    process_screenshot(browser, bucket_name, "1")


    # search_box = browser.find_element_by_name('p')
    search_box = browser.find_element(By.NAME, 'p')
    search_box.send_keys('こんにちは')
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)

    process_screenshot(browser, bucket_name, "test")
    first_result_title = browser.find_element(By.CSS_SELECTOR, '.sw-Card__title').text
    # first_result_title = browser.find_element_by_css_selector('.sw-Card__title').text
    print(f"最初の検索結果のタイトル: {first_result_title}")

    browser.close()

    return {
        'statusCode': 200,
        'body': 'スクリーンショットの保存とアップロードが完了しました'
    }



