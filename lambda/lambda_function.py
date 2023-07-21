import boto3
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
# testsss
    
def lambda_handler(event, context):
    print("Starting Lambda function")
    user = decrypt_secret('user')

    URL = "https://www.yahoo.co.jp/"

    options = webdriver.ChromeOptions()
    # headless-chromiumのパスを指定
    options.binary_location = "/opt/headless/headless-chromium"
    options.add_argument("--headless")
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--no-sandbox")

    print("Starting Chrome")
    browser = webdriver.Chrome(
        # chromedriverのパスを指定
        executable_path="/opt/headless/chromedriver",
        options=options
    )

    browser.get(URL)
    title = browser.title
    print(f"Page title: {title}")

    # 検索ボックスを見つける
    search_box = browser.find_element_by_name('p')  # Yahoo Japanの検索ボックスのname属性は'p'
    
    # 検索ボックスに「テスト」と入力
    search_box.send_keys(user)
    
    # 検索を実行
    search_box.send_keys(Keys.RETURN)
    
    # 検索結果が表示されるまで待つ
    time.sleep(2)

    # 最初の検索結果のタイトルを取得
    first_result_title = browser.find_element_by_css_selector('.sw-Card__title').text
    print(f"First result title: {first_result_title}")

    screenshot_path = "/tmp/screenshot.png"
    print(f"Saving screenshot to {screenshot_path}")
    browser.save_screenshot(screenshot_path)
    browser.close()

    # Check if screenshot was saved correctly
    if os.path.exists(screenshot_path):
        print("Screenshot saved successfully")
    else:
        print("Screenshot was not saved correctly")

    # S3にアップロード
    s3 = boto3.client('s3')
    bucket_name = 'selenium-work-python'  # ここにあなたのS3バケット名を入力してください
    print(f"Uploading screenshot to s3://{bucket_name}/data/screenshot/1.png")
    s3.upload_file(screenshot_path, bucket_name, 'data/screenshot/1.png')

    return {
        'statusCode': 200,
        'body': f'Screenshot saved at s3://{bucket_name}/data/screenshot/1.png'
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
