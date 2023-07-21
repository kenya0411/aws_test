
import os

# import imaplib#メール用
# import email#メール用
# import time#時間用
# import datetime
# import re#金額修正用
# import pickle#商品登録用
# from email.header import decode_header
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from urllib.parse import urlparse, parse_qs#クエリ取得用
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


root_path = os.path.abspath(os.path.dirname(__file__))

# 設定情報をインポート
# import utils.option
import config

#ディレクトリやchoromeの情報をインポート
import utils.option as option
driver = option.driver

# 関数をインポート
from utils.common import *


def login_metabusiness(driver,config):

    url ="https://business.facebook.com/latest/home"
    # url ="https://business.facebook.com/login/?next=https%3A%2F%2Fbusiness.facebook.com%2F%3Fnav_ref%3Dbizweb_landing_fb_login_button%26biz_login_source%3Dbizweb_landing_fb_login_button"
    driver.get(url)  # ここを実際のURLに置き換えてください
    time.sleep(2)  # ページの遷移を待つ
    try:
            # ここでスクリーンショットを取る
        ss_path = "data/screenshot/"
        driver.save_screenshot(ss_path+'start.png')
        # 要素が出てくるまで待つ
        wait = WebDriverWait(driver, 20)
        # ユーザ名とパスワードの入力フィールドを探します。
        username_field = driver.find_element(By.XPATH, '//*[@id="email"]')
        password_field = driver.find_element(By.XPATH, '//*[@id="pass"]')

        # 入力フィールドにユーザ名とパスワードを入力します。
        username_field.send_keys(config.facebook_info["face_id"])
        password_field.send_keys(config.facebook_info["face_pass"])
        # ここでスクリーンショットを取る
        driver.save_screenshot(ss_path+'1.png')
        # パスワード入力フィールドでEnterキーを押してログインします。
        password_field.send_keys(Keys.RETURN)

        time.sleep(7)  # ページの遷移を待つ
            # ここでスクリーンショットを取る
        driver.save_screenshot(ss_path+'2.png')
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


    except NoSuchElementException:
        time.sleep(1)  # ページの遷移を待つ
        print("already logined")
login_metabusiness(driver,config)
        
# #---------------------------------------------
# # メールを取得
# #---------------------------------------------
# search_words = "トークルームに連絡がありました"
# get_mail_content= get_mail_content(config,search_words,config.mail_reply_info)
# mail_info = {
# "mail" : get_mail_content['mail'],
# "email_ids" : get_mail_content['email_ids'],
# }

# #---------------------------------------------
# # 顧客管理システムに登録してあるかの確認
# #---------------------------------------------


# def is_product_found(driver):
#     try:
#         # "完了"という要素が存在するかを確認
#         # completion_message = driver.find_element(By.CSS_SELECTOR, 'div.no2 span')
#         completion_message = driver.find_element(By.XPATH, '/html/body/main/section[2]/div[4]/ul/li[2]/div[2]/div[5]/span')

#         # 'icon_list'という要素下に特定の画像要素が存在しないかを確認
#         image_elements = driver.find_elements(By.CSS_SELECTOR, 'ul.icon_list img')

#         # 取得したすべての画像のsrc属性を確認し、特定のURL部分（'specific_url_part'）を含むものがあるかどうか調査
#         image_exists = any('order_icon4.png' in image.get_attribute('src') for image in image_elements)
#         # "完了"というメッセージが存在し、かつ特定の画像が存在しなければ返事すべきと判断
        
#         return completion_message.text == "完了" and not image_exists
#     except NoSuchElementException:
#         # 上記いずれかの要素が見つからなければスルー
        
#         return False


# #---------------------------------------------
# # ココナラからテキストを取得
# #---------------------------------------------
# def get_product_info(driver,product_id):
#     # product_url = "https://coconala.com/talkrooms/11347063"
#     product_url = "https://coconala.com/talkrooms/" + product_id
#     driver.get(product_url)
#     time.sleep(1)  # ページの遷移を待つ

#     # 納品通知のあとのメッセージを取得
#     chat_contents = []

#     try:
#         element_selector = '//span[contains(@class,"d-messageInfo_label-isBold") and contains(text(), "正式な納品")]'
#         element = driver.find_elements(By.XPATH, element_selector)

#         def find_delivery_notice_in_message(chat_message):
#             delivery_notice_selector = './/div[1]/div[2]/div[1]/span'
#             delivery_notices = chat_message.find_elements(By.XPATH, delivery_notice_selector)
#             return delivery_notices[0].text if delivery_notices else None

     
#         # 納品通知のあとのメッセージを取得
#         chat_messages_selector = '//div[contains(@class,"d-talkroomMessage")]'
#         chat_messages = driver.find_elements(By.XPATH, chat_messages_selector)
#         found_delivery_notice = False

#         for chat_message in chat_messages:

#             delivery_notice = find_delivery_notice_in_message(chat_message)
        
#             if delivery_notice == "正式な納品":
#                 found_delivery_notice = True

#             if found_delivery_notice:
#                 # 納品通知以降のメッセージを追加
#                 try:
#                     class_name = chat_message.get_attribute('class')
#                     if "d-talkroomMessage-isOthers" in class_name:
#                         # ここで処理を書く
#                         chat_contents_selector = './/div[2]/p'
#                         chat_contents_elements = chat_message.find_elements(By.XPATH, chat_contents_selector)
#                         if chat_contents_elements:
#                             chat_content_text = chat_contents_elements[0].text
#                             # チャット内容が有料オプションの通知でないか確認
#                             if 'が追加でオプション購入されました。' not in chat_content_text:
#                                 chat_contents.append(chat_content_text)

#                         pass

#                 except NoSuchElementException:
#                     # Element not found
#                     pass
#     except NoSuchElementException:
#         return False
#     return chat_contents

# #---------------------------------------------
# # タスクを追加
# #---------------------------------------------
# # タスクが存在するかの確認
# def get_existing_tasks(headers, room_id):
#     response = requests.get(f"https://api.chatwork.com/v2/rooms/{room_id}/tasks", headers=headers)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         # print(f"エラーが発生しました: {response.status_code}")
#         # print(f"レスポンスの内容: {response.text}")
#         return None


# # 文字列の置換
# def replace_strings(content):
#     replacements = {
#         "れんれい": "Rise",
#         "レンレイ": "Rise",
#         "恋霊": "Rise",
#         "ココナラ": "アプリ",
#         "ここなら": "アプリ",
#         "coconala": "アプリ",
#         # 他の置換したい文字列を追加
#     }
#     for key, value in replacements.items():
#         content = content.replace(key, value)
#     return content

# # タスクの追加
# def add_task_chatwork(driver, product_id, chat_contents):
#     api_token = config.chatwork_api_token
#     room_id = "292738108"
#     # room_id = "239589713"#テスト環境
    
#     YOUR_ACCOUNT_ID = 3228397

#     # れんれい、レンレイの文字列をRiseに変更
#     chat_contents = [replace_strings(content) for content in chat_contents]

#     chat_content_text = ''.join(chat_contents)
    
#     # タスクの本文の設定
#     task_body = chat_contents
#     body_content = f"{product_id}\n\n{chat_content_text}"

#     headers = {"X-ChatWorkToken": api_token}

#     # メンバー一覧を取得
#     response = requests.get(f"https://api.chatwork.com/v2/rooms/{room_id}/members", headers=headers)
#     members = response.json()

#     # 自分以外のメンバーのIDを取得
#     assignee_ids = [str(member['account_id']) for member in members if member['account_id'] != YOUR_ACCOUNT_ID]

#     # 本日の日付を取得
#     today = dt.now()
#     current_day = today.replace(hour=0, minute=0, second=0)
#     limit = int(current_day.timestamp())

#     existing_tasks = get_existing_tasks(headers, room_id)
#     task_already_exists = False

#     # 既存のタスクがあるかどうかを確認
#     if existing_tasks is not None:
#         for task in existing_tasks:
#             # タスク内にproduct_idが含まれているか確認
#             if product_id in task['body'] and str(task['account']['account_id']) in assignee_ids:
#                 task_already_exists = True
#                 break

#     # タスクが存在しない場合は、新しいタスクを追加
#     if not task_already_exists:
#         for assignee_id in assignee_ids:
#             data = {
#                 "body": body_content,
#                 "to_ids": assignee_id,  # 各assignee_idにタスクを追加するためにこの行をアップデートしました
#                 "limit": limit
#             }

#             response = requests.post(f"https://api.chatwork.com/v2/rooms/{room_id}/tasks", headers=headers, data=data)

#             if response.status_code == 200:
#                 print(f"タスクが正常に追加されました。Assignee ID: {assignee_id}")  # 各Assignee IDを表示
#             else:
#                 print(f"エラーが発生しました: {response.status_code}")
#                 print(f"レスポンスの内容: {response.text}")
#     else:
#         print("タスクは既に存在します。追加されません。")

# #---------------------------------------------
# # main処理
# #---------------------------------------------
# def main(driver, mail_info):
# # def main(driver, mail):
#     print('start reply.py')
#     # 一度返信した商品はスキップする為の関数
#     skip_filename = skip_filename_dir(option,root_path,"reply")
#     registered_product_ids = load_registered_products(skip_filename)

#     # ログイン確認
#     # coconala_login(driver,root_path)
#     # laravel_login(driver,root_path,config.laravel)


#     for email_id in mail_info["email_ids"]:
#         print(email_id)
#         # メールを取得
#         product_id = search_product(driver, mail_info["mail"],email_id)

#         # 商品が早くに登録されていたらスキップ
#         if product_id in registered_product_ids:
#             print(f"Product {product_id} is already registered, skipping.")
#             continue

#         # 検索結果を確認
#         if is_product_found(driver):  # この関数も独自に定義する必要があります
           

#             #トーク内容を取得
#             chat_contents = get_product_info(driver,product_id) 
#             if chat_contents:

#                 add_task_chatwork(driver,product_id,chat_contents)  


#                 # 商品を登録したので保存
#                 registered_product_ids.add(product_id)
#                 save_registered_products(skip_filename,registered_product_ids)
#     print("all completed reply.py")


# #---------------------------------------------
# # 処理を実行
# #---------------------------------------------
# # main(driver, mail)
