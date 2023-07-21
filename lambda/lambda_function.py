import boto3
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import config
from utils.common import *

def headless_chrome(config):
    # 現在のスクリプトの絶対パスを取得
    current_path = os.path.abspath(os.path.dirname(__file__))

    # 親ディレクトリのパスを取得
    # parent_path = os.path.dirname(current_path)

    # ChromeDriverの絶対パスを作成
    driver_path = os.path.join(current_path+"/data", 'chromedriver')
    # driver_path = 'chromedriver'
    # 
    #seleniumのバージョンにより変更
    service = Service(executable_path=driver_path)

    options = Options()
    options.add_argument("--headless")  # Headlessモードを有効にする
    options.add_argument("--disable-gpu")  # GPUを使用しない
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('window-size=1200x600')

    if(config.os_ver == "win"):
        profile_directory = '/Users/user/AppData/Local/Google/Chrome/User Data/python'
    options.add_argument(f'--user-data-dir={profile_directory}')
    driver = webdriver.Chrome(service=service, options=options)#seleniumのバージョンにより変更
    return driver





def get_driver():
    ENV = decrypt_secret('ENV', 'LOCAL')
    if ENV == 'PROD':  # AWS環境
        options = webdriver.ChromeOptions()
        options.binary_location = "/opt/headless/headless-chromium"
        options.add_argument("--headless")
        options.add_argument('--single-process')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--no-sandbox")
        print("Chromeを起動")
        driver = webdriver.Chrome(
            executable_path="/opt/headless/chromedriver",
            options=options
        )
    else:  # ローカル環境
        driver = headless_chrome(config)
    
    return driver


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
