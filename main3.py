import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.font_manager as fm
from pygbif import occurrences as occ
from ucimlrepo import fetch_ucirepo

# フォント設定
font_path = r"C:\Windows\Fonts\meiryo.ttc"
font_prop = fm.FontProperties(fname=font_path)
rcParams["font.family"] = font_prop.get_name()

# データの取得 (UCI Mushroom Dataset)
mushroom = fetch_ucirepo(id=73)

# UCIデータの前処理
X = mushroom.data.features
y = mushroom.data.targets
mr_data = pd.concat([X, y], axis=1)
mr_data.rename(columns={mr_data.columns[-1]: "edibility"}, inplace=True)

# Amanita属を推測する条件でフィルタリング (ツボとツバ)
amanita_uci = mr_data.loc[
    (mr_data["stalk-root"].isin(["b", "e"])) &  # ツボの条件 (根元が膨らんでいる)
    (mr_data["stalk-surface-below-ring"].isin(["k", "s"]))  # ツバの条件 (膜のような部分)
].copy()

# 胞子の色を日本語に変換
spore_color_mapping = {
    'k': '黒',
    'n': '茶色',
    'u': '紫',
    'h': '白',
    'w': '白',
    'r': '赤',
    'o': 'オレンジ',
    'y': '黄色',
    'b': '青',
}
amanita_uci['spore-print-color'] = amanita_uci['spore-print-color'].map(spore_color_mapping)
amanita_uci['source'] = 'UCI Dataset'

# edibility列を食用/毒性ありに変換
amanita_uci['edibility'] = amanita_uci['edibility'].map({'e': '食用', 'p': '毒性あり'})

# GBIFからAmanita属データを取得
gbif_data = occ.search(scientificName="Amanita", limit=50, hasCoordinate=True)
gbif_results = pd.DataFrame(gbif_data['results'])

# 必要な情報を抽出
gbif_filtered = gbif_results.loc[:, ["scientificName", "basisOfRecord", "issues"]].copy()
gbif_filtered.rename(columns={
    "scientificName": "scientific_name"
}, inplace=True)
gbif_filtered['source'] = 'GBIF'
gbif_filtered['edibility'] = '毒性あり'  # 仮の毒性情報を設定
gbif_filtered['spore-print-color'] = '白'  # 仮の胞子色を設定

# Amanita属データを統合
combined_data = pd.concat([amanita_uci, gbif_filtered], ignore_index=True)

# 統合データに欠損値がないか確認し、欠損値があれば削除
combined_data = combined_data.dropna(subset=['spore-print-color', 'edibility'])

# グラフ化
plt.figure(figsize=(12, 7))
sns.countplot(
    x="spore-print-color", 
    hue="edibility", 
    data=combined_data, 
    palette="Set2"
)

# タイトルとラベルを日本語で設定
plt.title("Amanita属: 胞子の色と毒性の関係", fontsize=16)
plt.xlabel("胞子の色", fontsize=12)
plt.ylabel("カウント", fontsize=12)
plt.legend(title="毒性", loc="upper right", fontsize=10)
plt.tight_layout()

# グラフ表示
plt.show()

# Amanita属のキノコ名をリスト表示 (重複排除)
unique_scientific_names = gbif_filtered['scientific_name'].dropna().unique()

# Amanita属のキノコ名を表示
print("Amanita属のキノコの名前:")
for name in unique_scientific_names:
    print(f"- {name}")
