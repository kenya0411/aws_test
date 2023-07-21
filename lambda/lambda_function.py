import boto3
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from utils.common import *



def lambda_handler(event, context):
    print("Lambda functionを開始")
    user = decrypt_secret('user')

    URL = "https://www.yahoo.co.jp/"

    options = webdriver.ChromeOptions()
    options.binary_location = "/opt/headless/headless-chromium"
    options.add_argument("--headless")
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--no-sandbox")

    print("Chromeを起動")
    browser = webdriver.Chrome(
        executable_path="/opt/headless/chromedriver",
        options=options
    )

    browser.get(URL)
    bucket_name = 'selenium-work-python'
    process_screenshot(browser, bucket_name, "1")


    search_box = browser.find_element_by_name('p')
    search_box.send_keys(user)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)

    process_screenshot(browser, bucket_name, "test")

    first_result_title = browser.find_element_by_css_selector('.sw-Card__title').text
    print(f"最初の検索結果のタイトル: {first_result_title}")

    browser.close()

    return {
        'statusCode': 200,
        'body': 'スクリーンショットの保存とアップロードが完了しました'
    }


def decrypt_secret(key):
    from base64 import b64decode
    ENCRYPTED = os.environ[key]
    # Decrypt code should run once and variables stored outside of the function
    # handler so that these are decrypted once per container
    DECRYPTED = boto3.client('kms').decrypt(
        CiphertextBlob=b64decode(ENCRYPTED),
        EncryptionContext={'LambdaFunctionName': os.environ['AWS_LAMBDA_FUNCTION_NAME']}
    )['Plaintext'].decode('utf-8')

    return DECRYPTED

