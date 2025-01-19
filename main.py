# 傘の形状と胞子の色の関係

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

# cap-shapeとspore-print-colorを日本語に置き換える
cap_shape_mapping = {
    'x': '鐘形',
    'b': '凸形',
    'c': '皿形',
    'f': '扁平',
    'k': 'くさび形',
    's': '凹形',
    'u': '凸面',
}

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

# cap-shapeとspore-print-colorの値を日本語に変換
mr_data['cap-shape'] = mr_data['cap-shape'].map(cap_shape_mapping)
mr_data['spore-print-color'] = mr_data['spore-print-color'].map(spore_color_mapping)

# 日本語フォントを設定 (例: Windowsの場合、'MS Gothic'を使用)
plt.rcParams['font.family'] = 'MS Gothic'

# グラフ化 (cap-shape と spore-print-colorの関係)
plt.figure(figsize=(12, 7))
sns.countplot(x="cap-shape", hue="spore-print-color", data=mr_data, palette="Set2")

# タイトルとラベルを日本語で設定
plt.title("傘の形状と胞子の色の関係", fontsize=16)
plt.xlabel("傘の形状", fontsize=12)
plt.ylabel("カウント", fontsize=12)

# 凡例を見やすく調整
plt.legend(title="胞子の色", loc="upper left", bbox_to_anchor=(1, 1), fontsize=10)

# レイアウトの調整
plt.tight_layout()

# グラフ表示
plt.show()
