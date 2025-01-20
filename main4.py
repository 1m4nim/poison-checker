from pygbif import occurrences as occ
import pandas as pd
from tqdm import tqdm  # tqdmをインポート

# GBIFからAmanita属のデータをページごとに取得
def fetch_all_gbif_data(scientific_name, limit=100):
    all_results = []
    offset = 0
    # 最初に取得したデータ数でプログレスバーの総数を設定
    first_batch = occ.search(scientificName=scientific_name, limit=limit, offset=0, hasCoordinate=True)
    total_results = first_batch['meta']['totalRecords'] if 'meta' in first_batch else first_batch['count']  # 'meta'ではなく'count'を使用
    # プログレスバーを設定
    with tqdm(total=total_results, desc="データ取得中") as pbar:
        while True:
            # 一度に取得するデータの制限を設定
            gbif_data = occ.search(scientificName=scientific_name, limit=limit, offset=offset, hasCoordinate=True)
            results = gbif_data['results']
            
            if not results:
                break  # データがない場合は終了
            
            all_results.extend(results)
            offset += limit  # 次のページに進む
            
            # プログレスバーを更新
            pbar.update(len(results))
    
    return pd.DataFrame(all_results)

# Amanita属のデータを取得
gbif_all_data = fetch_all_gbif_data("Amanita")
print(f"全件数: {len(gbif_all_data)}")  # 取得したデータの件数を表示

# 必要な情報を抽出
gbif_filtered = gbif_all_data.loc[:, ["scientificName", "basisOfRecord", "issues"]].copy()
gbif_filtered.rename(columns={
    "scientificName": "scientific_name"
}, inplace=True)

# 結果を表示
print("Amanita属のキノコ名:")
unique_scientific_names = gbif_filtered['scientific_name'].dropna().unique()
for name in unique_scientific_names:
    print(f"- {name}")
