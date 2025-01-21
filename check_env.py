import os

os.environ["GBIF_USER"] = "minami-yamasaki"
os.environ["GBIF_PWD"] = "nokonoko42"
os.environ["GBIF_EMAIL"] = "fancustard9@gmail.com"


# 環境変数が取得できているか確認
if gbif_user is None:
    print("GBIF_USER 環境変数が設定されていません。")
else:
    print(f"GBIF_USER: {gbif_user}")

if gbif_password is None:
    print("GBIF_PWD 環境変数が設定されていません。")
else:
    print(f"GBIF_PWD: {gbif_password}")

if gbif_email is None:
    print("GBIF_EMAIL 環境変数が設定されていません。")
else:
    print(f"GBIF_EMAIL: {gbif_email}")
