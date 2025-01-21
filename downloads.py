import os
import time
import requests
import zipfile
import logging
from pygbif import occurrences as occ  # pygbifライブラリのインポート

# ログの設定
logging.basicConfig(level=logging.DEBUG)

# 環境変数の設定（必要に応じて変更）
os.environ["GBIF_USER"] = "minami-yamasaki"
os.environ["GBIF_PWD"] = "nokonoko42"
os.environ["GBIF_EMAIL"] = "fancustard9@gmail.com"

# GBIFのダウンロードリクエストを送信
def request_gbif_download(scientific_name):
    try:
        # フィルター条件を直接設定
        download_key = occ.download(
            [
                'scientificName = {}'.format(scientific_name),  # 学名でフィルタリング
                'hasCoordinate = true'  # 座標情報が存在するもの
            ]
        )
        logging.info(f"ダウンロードリクエストが送信されました。ダウンロードキー: {download_key}")
        return download_key
    except Exception as e:
        logging.error(f"ダウンロードリクエスト中にエラーが発生しました: {e}")
        return None

# ダウンロードステータスを確認
def check_download_status(download_key):
    download_key = download_key[0]  # タプルからキーを取得
    while True:
        try:
            # ステータスを確認
            status = occ.download_meta(key=download_key)
            logging.info(f"ステータス: {status['status']}")

            if status['status'] == 'SUCCEEDED':
                logging.info("ダウンロード準備完了！")
                return status['downloadLink']  # ダウンロードリンクを取得
            elif status['status'] == 'FAILED':
                logging.error("ダウンロードに失敗しました。")
                return None

            time.sleep(60)  # 1分ごとにステータスを確認
        except Exception as e:
            logging.error(f"ステータス確認中にエラーが発生しました: {e}")
            return None

# データをダウンロードして保存
def download_gbif_data(download_link, output_file):
    try:
        # ダウンロード
        response = requests.get(download_link, stream=True)
        with open(output_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        logging.info(f"データを保存しました: {output_file}")
    except Exception as e:
        logging.error(f"データダウンロード中にエラーが発生しました: {e}")

# ZIPファイルを解凍
def extract_zip_file(zip_file, extract_to):
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        logging.info(f"データを解凍しました: {extract_to}")
    except Exception as e:
        logging.error(f"解凍中にエラーが発生しました: {e}")

# メイン処理
if __name__ == "__main__":
    # check_env.pyで設定された環境変数を読み込む
    gbif_user = os.getenv("GBIF_USER")
    gbif_password = os.getenv("GBIF_PWD")

    if not gbif_user or not gbif_password:
        logging.error("環境変数が設定されていないか、無効です。")
        exit(1)

    # 学名を指定
    scientific_name = "Amanita"

    # ダウンロードリクエストを送信
    download_key = request_gbif_download(scientific_name)
    
    if download_key:
        # ダウンロードステータスを確認
        download_link = check_download_status(download_key)
        
        if download_link:
            # データをダウンロード
            output_zip = "gbif_amanita_data.zip"
            download_gbif_data(download_link, output_zip)
            
            # データを解凍
            extract_folder = "gbif_data"
            extract_zip_file(output_zip, extract_folder)
