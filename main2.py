import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# データの読み込み (UCI Mushroom Dataset)
from ucimlrepo import fetch_ucirepo
mushroom = fetch_ucirepo(id=73)

# データの取得
X = mushroom.data.features
y = mushroom.data.targets

# 特徴量とターゲットデータを結合
mr_data = pd.concat([X, y], axis=1)

# 列名を確認
mr_data.rename(columns={mr_data.columns[-1]: "edibility"}, inplace=True)

# spore-print-colorを日本語に置き換える
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

# spore-print-colorの値を日本語に変換
mr_data['spore-print-color'] = mr_data['spore-print-color'].map(spore_color_mapping)

# 日本語フォントを設定 (例: Windowsの場合、'MS Gothic'を使用)
plt.rcParams['font.family'] = 'MS Gothic'

# グラフ化 (spore-print-color と edibilityの関係)
plt.figure(figsize=(12, 7))
sns.countplot(x="spore-print-color", hue="edibility", data=mr_data, palette="Set2")

# タイトルとラベルを日本語で設定
plt.title("胞子の色と毒性の関係", fontsize=16)
plt.xlabel("胞子の色", fontsize=12)
plt.ylabel("カウント", fontsize=12)

# 凡例を見やすく調整
plt.legend(title="毒性", loc="upper left", bbox_to_anchor=(1, 1), fontsize=10)

# レイアウトの調整
plt.tight_layout()

# グラフ表示
plt.show()
