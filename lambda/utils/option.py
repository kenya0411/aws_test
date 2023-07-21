# option.py
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from time import sleep
# import config


# Chromeの情報
# options = Options()
# options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# # 現在のスクリプトの絶対パスを取得
# current_path = os.path.abspath(os.path.dirname(__file__))

# # 親ディレクトリのパスを取得
# parent_path = os.path.dirname(current_path)

# # ChromeDriverの絶対パスを作成
# driver_path = os.path.join(parent_path+"/data", 'chromedriver')
# # driver_path = 'chromedriver'
# # 
# #seleniumのバージョンにより変更
# service = Service(executable_path=driver_path)

# try:
#     # WebDriverのインスタンスを生成
#     # driver = webdriver.Chrome(executable_path=driver_path, options=options)
#     driver = webdriver.Chrome(service=service, options=options)#seleniumのバージョンにより変更
# except Exception as e:
#     print("WebDriverエラー:", str(e))
#     # もしエラーが出た場合はwebdriver_managerでChromeDriverをインストール
    
#     driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)



#---------------------------------------------
# Headless Chrome
#---------------------------------------------


# def headless_chrome(service,config):
#     options = Options()
#     options.add_argument("--headless")  # Headlessモードを有効にする
#     options.add_argument("--disable-gpu")  # GPUを使用しない
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     options.add_argument('window-size=1200x600')

#     if(config.os_ver == "win"):
#         profile_directory = '/Users/user/AppData/Local/Google/Chrome/User Data/python'
#     options.add_argument(f'--user-data-dir={profile_directory}')

#     driver = webdriver.Chrome(service=service, options=options)#seleniumのバージョンにより変更


#     return driver

# driver = headless_chrome(service,config)


def headless_chrome():
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service#seleniumのバージョンにより変更
    # 現在のスクリプトの絶対パスを取得
    current_path = os.path.abspath(os.path.dirname(__file__))

    # 親ディレクトリのパスを取得
    parent_path = os.path.dirname(current_path)

    # ChromeDriverの絶対パスを作成
    driver_path = os.path.join(parent_path+"/data", 'chromedriver')
    # driver_path = 'chromedriver'

    #seleniumのバージョンにより変更
    service = Service(executable_path=driver_path)

    options = Options()
    options.add_argument("--headless")  # Headlessモードを有効にする
    options.add_argument("--disable-gpu")  # GPUを使用しない
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('window-size=1200x600')
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
        driver = headless_chrome()
    
    return driver