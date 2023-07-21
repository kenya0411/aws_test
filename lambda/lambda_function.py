import boto3
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from utils.common import *
from utils.option import *




def lambda_handler(event, context):
    print("Lambda functionを開始")
    user = decrypt_secret('user')

    URL = "https://www.yahoo.co.jp/"

    browser = get_driver()



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


def decrypt_secret(key, encryption_context=None):
    from base64 import b64decode
    ENCRYPTED = os.environ[key]

    if encryption_context is None:
        encryption_context = {'LambdaFunctionName': os.environ['AWS_LAMBDA_FUNCTION_NAME']}

    DECRYPTED = boto3.client('kms').decrypt(
        CiphertextBlob=b64decode(ENCRYPTED),
        EncryptionContext=encryption_context
    )['Plaintext'].decode('utf-8')

    return DECRYPTED
