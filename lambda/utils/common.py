# #ディレクトリやchoromeの情報をインポート
# import option as option
# driver = option.driver
import imaplib#メール用
import email#メール用
import datetime
import time#時間用
import pickle#商品登録用
from email.header import decode_header
# from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
# from urllib.parse import urlparse, parse_qs#クエリ取得用
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


url = "https://customer.neobingostyle.com/orders"

#---------------------------------------------
# メール情報を取得
#---------------------------------------------

def get_mail_content(config,search_words,mail_info):
    # IMAPサーバーと接続
    mail = imaplib.IMAP4_SSL(mail_info["mail_server"])
    mail._encoding = 'utf-8'  # ここでエンコーディングをUTF-8に設定

    # メールアカウントにログイン
    mail.login(mail_info["mail_id"], mail_info["mail_pass"])


    # 受信トレイを選択
    mail.select("inbox")



    # 検索条件に一致するメールを検索

    # date = (datetime.datetime.now() - datetime.timedelta(hours=2)).strftime("%d-%b-%Y")# 現在時刻から8時間前の日付を取得
    date = (datetime.datetime.now() - datetime.timedelta(hours=30)).strftime("%d-%b-%Y")# 現在時刻から8時間前の日付を取得

    # その日付以降のメールを検索
    # search_words = "出品サービスが購入されました"
    result, data = mail.uid('search', None, '(HEADER Subject "{}") SINCE {}'.format(search_words, date))


    # メールIDのリストを取得
    email_ids = data[0].split()
    return {
    "email_ids":email_ids,
    "mail":mail,
    }


#---------------------------------------------
# メール本文から商品IDを取得
#---------------------------------------------
def get_product_id_from_email(email_message):
    for part in email_message.walk():
        if part.get_content_type() == "text/plain":
            body = part.get_payload(decode=True).decode("utf-8")  # バイト列を文字列に変換
            start = body.find("トークルームNo：")
            if start != -1:
                start += len("トークルームNo：")
                end = body.find("\n", start)
                if end == -1:
                    end = len(body)
                return body[start:end]
    return None


#---------------------------------------------
# 一度登録した商品はスキップする為の関数
#---------------------------------------------
def skip_filename_dir(option,root_path,name):

    # スクリプトの実行ディレクトリを取得
    registered_directory = option.os.path.join(root_path+"/data", name)

    # ディレクトリが存在しない場合にディレクトリを作成
    if not option.os.path.exists(registered_directory):
        option.os.makedirs(registered_directory)

    # registeredディレクトリ内にファイルを保存
    registered_products_filename = option.os.path.join(registered_directory, name+"_products.pkl")
    return registered_products_filename

def save_registered_products(skip_filename,product_ids):
    with open(skip_filename, "wb") as f:
        pickle.dump(product_ids, f)

def load_registered_products(skip_filename):
    try:
        with open(skip_filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        # 初回起動時はファイルが存在しないので空のセットを返す
        return set()



#---------------------------------------------
# 商品が登録されているかどうか確認
#---------------------------------------------
def search_product(driver, mail,email_id):
    result, email_data = mail.uid('fetch', email_id, '(BODY.PEEK[])')
    raw_email = email_data[0][1].decode("utf-8", errors='ignore')
    # email_message = email.message_from_string(raw_email)
    email_message = email.message_from_bytes(email_data[0][1])

    # メール本文から商品IDを取得
    product_id = get_product_id_from_email(email_message)  # この関数は独自に定義する必要があります

    # 顧客管理システムに移動
    driver.get(url)
    time.sleep(2)  # ページの遷移を待つ

    # 西暦
    year_select = Select(driver.find_element(By.XPATH, '/html/body/main/section[2]/div[2]/ul/li[4]/select'))
    year_select.select_by_value("") 
    time.sleep(1)  # ページの遷移を待つ

    # 商品IDを検索用のinputに入力
    search_box = driver.find_element(By.XPATH, '/html/body/main/section[2]/div[2]/ul/li[1]/div/input')
    search_box.click()
    
    search_box.send_keys(product_id)

    time.sleep(1)  # ページの遷移を待つ
    print("Finished search_product")

    return product_id


#---------------------------------------------
# ココナラにログイン
#---------------------------------------------
#まだ未完成（二段階認証）
def coconala_login(driver,root_path,config):
    driver.get("https://coconala.com/mypage/received_orders/open")  # ここを実際のURLに置き換えてください
    time.sleep(2)  # ページの遷移を待つ

    try:
        # Googleでログイン
        login_link = driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div/div/a[1]')
        login_link.click()
        print("need to login coconala")
        time.sleep(6)  # ページの遷移を待つ
        driver.save_screenshot(root_path+'/data/img/1.png')

        try:
            try:
                login_account_element = driver.find_element(By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div/div/ul/li[3]/div')
            except NoSuchElementException:
                login_account_element = driver.find_element(By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div/div/ul/li[2]/div/div/div[2]')

            driver.execute_script("arguments[0].click();", login_account_element)
            print("selected account")
            time.sleep(6)  # ページの遷移を待つ
        except NoSuchElementException:
            print("no need to select account")
        driver.save_screenshot(root_path+'/data/img/2.png')

        # 要素が出てくるまで待つ
        wait = WebDriverWait(driver, 20)

        # ログインIDを入力
        login_id_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="identifierId"]|//*[@id="Email"]')))

        time.sleep(1) 
        driver.execute_script("arguments[0].value = arguments[1];", login_id_element, config.google_id)
        time.sleep(1)  
        print("12")

        login_id_element.send_keys(Keys.RETURN)
        time.sleep(5)  # ページの遷移を待つ
        print("3")
        driver.save_screenshot(root_path+'/data/img/3.png')

        # ログインPASSを入力
        login_pass_element = driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
        time.sleep(1) 
        driver.execute_script("arguments[0].value = arguments[1];", login_pass_element, config.google_pass)        
        login_pass_element.send_keys(Keys.RETURN)

        time.sleep(8)  # ページの遷移を待つ
        print("5")

        # 二段階認証を別の方法を試す
        try:
            other_button = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div[2]/div[2]/div[2]/div/div/button')
        except NoSuchElementException:
            other_button = driver.find_element(By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div/button')
        other_button.click()
        time.sleep(8)  # ページの遷移を待つ
        print("7")

        # Google 認証システム アプリから確認コードを取得する
        other_ellement = driver.find_element(By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/ul/li[2]/div/div[2]')
        driver.execute_script("arguments[0].click();", other_ellement)
        time.sleep(8)  # ページの遷移を待つ
        print("7")
        
        # 二段階認証のパスワードを入力
        second_pass = driver.find_element(By.XPATH, '//*[@id="totpPin"]')
        second_pass.send_keys(config.SecondLoginPass)
        second_pass.send_keys(Keys.RETURN)
        time.sleep(10)  # ページの遷移を待つ
        print("Finished to login coconala")


    except NoSuchElementException:
        time.sleep(1)  # ページの遷移を待つ
        print("already coconala logined")

        
#---------------------------------------------
# 顧客管理システムにログイン
#---------------------------------------------
def laravel_login(driver,root_path,laravel):
    driver.get("https://customer.neobingostyle.com/")  # ここを実際のURLに置き換えてください
    time.sleep(2)  # ページの遷移を待つ
    try:
        # ID入力
        login_id_element = driver.find_element(By.XPATH, '//*[@id="name"]')
        time.sleep(1)  # ページの遷移を待つ
        driver.execute_script("arguments[0].value = arguments[1];", login_id_element, laravel["id"])

        # パスワード入力
        login_pass_element = driver.find_element(By.XPATH, '//*[@id="password"]')
        time.sleep(1)  # ページの遷移を待つ
        driver.execute_script("arguments[0].value = arguments[1];", login_pass_element, laravel["pass"])
        
        # ログインボタンをクリック
        submit_button = driver.find_element(By.XPATH, '//*[@id="app"]/main/div/div/div/div/div[2]/form/div[4]/div/button')
        submit_button.click()
        print("Finished to login laravel")
    except NoSuchElementException:
        print("already laravel logined")

    time.sleep(2)  # ページの遷移を待つ
