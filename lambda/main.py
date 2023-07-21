import os

# 実行する関数
import lambda_function as lamb


# 関数
# import config
# import utils.option as option
# driver = option.driver
# from utils.common import *

# ルートパス
root_path = os.path.abspath(os.path.dirname(__file__))

lamb.lambda_handler("driver","register.mail_info");

# ログイン確認
# coconala_login(driver,root_path,config)
# laravel_login(driver,root_path,config.laravel)

# 実行用関数
# register.main(driver,register.mail_info);
# register.main(driver,register.mail_info);
# reply.main(driver,reply.mail_info);

