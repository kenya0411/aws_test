import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from utils.common import *
from utils.option import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def lambda_handler(event, context):

    print("Lambda functionを開始")

    URL = "https://www.yahoo.co.jp/"

    driver = get_driver()
    bucket_name = 'selenium-work-python'

    login_metabusiness(driver,bucket_name)

    # driver.get(URL)
    # process_screenshot(driver, bucket_name, "1")


    # # search_box = browser.find_element_by_name('p')
    # search_box = driver.find_element(By.NAME, 'p')
    # search_box.send_keys('こんにちは')
    # search_box.send_keys(Keys.RETURN)
    # time.sleep(2)

    # process_screenshot(driver, bucket_name, "test")
    # first_result_title = driver.find_element(By.CSS_SELECTOR, '.sw-Card__title').text
    # # first_result_title = driver.find_element_by_css_selector('.sw-Card__title').text
    # print(f"最初の検索結果のタイトル: {first_result_title}")


    return {
        'statusCode': 200,
        'body': 'スクリーンショットの保存とアップロードが完了しました'
    }



def login_metabusiness(driver,bucket_name):

    url ="https://business.facebook.com/latest/home"
    driver.get(url)  # ここを実際のURLに置き換えてください
    time.sleep(2)  # ページの遷移を待つ

    try:
        process_screenshot(driver, bucket_name, "1")
        print(decrypt_secret('base32_key'))
        print('SecondLoginPass----start')
        
        SecondLoginPass = SecondLoginPass_win(decrypt_secret('base32_key'))
        print(SecondLoginPass)
        print('SecondLoginPass----end')

        # 要素が出てくるまで待つ
        wait = WebDriverWait(driver, 20)
        # ユーザ名とパスワードの入力フィールドを探します。
        username_field = driver.find_element(By.XPATH, '//*[@id="email"]')
        password_field = driver.find_element(By.XPATH, '//*[@id="pass"]')
        process_screenshot(driver, bucket_name, "2")

        # 入力フィールドにユーザ名とパスワードを入力します。
        username_field.send_keys(11)
        password_field.send_keys(22)
        # ここでスクリーンショットを取る
        process_screenshot(driver, bucket_name, "3")

        # パスワード入力フィールドでEnterキーを押してログインします。
        password_field.send_keys(Keys.RETURN)

        time.sleep(7)  # ページの遷移を待つ
            # ここでスクリーンショットを取る
        auth_field = driver.find_element(By.XPATH, '//*[@id="approvals_code"]')
        auth_field.send_keys(config.SecondLoginPass)
        auth_field.send_keys(Keys.RETURN)
        driver.save_screenshot(ss_path+'3.png')
        
        time.sleep(3)  # ページの遷移を待つ
        driver.save_screenshot(ss_path+'4.png')

        submit_button = driver.find_element(By.XPATH, '//*[@id="checkpointSubmitButton"]')
        submit_button.click()
        driver.save_screenshot(ss_path+'5.png')


        print("Finished to login metabusiness suite")
        driver.close()


    except NoSuchElementException:
        time.sleep(1)  # ページの遷移を待つ
        print("already logined")


def SecondLoginPass_win(base32_key):
    import subprocess
    # oathtool_path = 'tools/oath-toolkit/oathtool.exe'
    oathtool_path = '/opt/usr/local/bin/oathtool'
    result = subprocess.run([oathtool_path, '--totp', '--base32', base32_key], capture_output=True, text=True)
    print("stderr:", result.stderr)  # エラーメッセージを表示
    return result.stdout.strip()

# def generate_otp(base32_key):
#     import pyotp
#     totp = pyotp.TOTP(base32_key)
#     SecondLoginPass = totp.now()  # Generates the current OTP
#     return SecondLoginPass