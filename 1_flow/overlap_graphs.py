# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import math

# ファイル・フォルダ、プロットするID数の設定
INPUT_FOLDER = "2_data"
INPUT_FILENAME= "sample.csv"
OUTPUT_FOLDER = "3_output"
group_size = 5

# パスの取得
current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)

input_path = os.path.join(parent_dir, INPUT_FOLDER, INPUT_FILENAME)
print("INFO: 入力データファイルパス:", input_path)

output_fol_path = os.path.join(parent_dir, OUTPUT_FOLDER)
os.makedirs(output_fol_path, exist_ok=True)

# CSV読み込み（UTF-8 BOM付き想定）
df_result = pd.read_csv(input_path, encoding="utf-8-sig")  # ここをutf-8-sigに

# 背景ヒートマップ
L_Len = len(df_result)

xedges = np.linspace(0, 100, 51)
yedges = np.linspace(0, 100, 51)

position_x = df_result['x']
position_y = df_result['y']

H, xedges, yedges = np.histogram2d(position_x, position_y, bins=(xedges, yedges))
H = (H / L_Len) * 100

id_list = df_result['id'].drop_duplicates().tolist()  # リスト化
groups = [id_list[i:i + group_size] for i in range(0, len(id_list), group_size)]

# 動線の色設定
clrs = [
    'red', 'green', 'blue', 
    'purple', 'orange', 'gold', 
    'lime', 'navy', 'pink', 
    'cyan', 'brown'
]

# ヒートマップの上に動線をプロット
for grp_idx, id_group in enumerate(groups):
    fig, ax = plt.subplots(figsize=(14, 12), dpi=130)

    # 背景ヒートマップ
    img = ax.imshow(
        H.T,
        origin='lower',
        cmap='PuRd',
        extent=[0, 100, 0, 100],
        alpha=0.7,
        vmin=0.05
    )

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    cbar = plt.colorbar(img, ax=ax)
    cbar.set_label('Presence Percentage (%)')

    for color_idx, current_id in enumerate(id_group):
        data_a = df_result.query('id == @current_id').sort_values('time_step')
        data_b = data_a.reset_index(drop=True)

        if len(data_b) > 0:
            line_color = clrs[color_idx % len(clrs)]
            oldx, oldy = None, None

            # スタート地点の座標
            startx = data_b.loc[0, 'x']
            starty = data_b.loc[0, 'y']

            ax.text(
                startx,
                starty,
                str(current_id),
                fontsize=12,
                color=line_color,
                weight='bold',
                ha='center',
                va='center',
                bbox=dict(facecolor='white', alpha=0.5, edgecolor='none', boxstyle='round,pad=0.3')
            )

            for idx, row in data_b.iterrows():
                newx = row['x']
                newy = row['y']

                if oldx is not None:
                    if (not any(math.isnan(v) for v in [oldx, oldy, newx, newy])
                        and (oldx != newx or oldy != newy)):
                        
                        ax.plot(
                            [oldx, newx],
                            [oldy, newy],
                            color=line_color,
                            linewidth=2,
                            alpha=0.8
                        )

                        ax.annotate(
                            '',
                            xy=(newx, newy),
                            xytext=(oldx, oldy),
                            arrowprops=dict(
                                arrowstyle="->",
                                color=line_color,
                                lw=1,
                                mutation_scale=20
                            )
                        )

                oldx, oldy = newx, newy

    ax.set_title(f"ID Group {grp_idx + 1} Movement Paths", fontsize=16)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_xticks(np.arange(0, 110, 5))
    ax.set_yticks(np.arange(0, 110, 5))

    plt.tight_layout()

    out_path = os.path.join(output_fol_path, f"movement_group_{grp_idx + 1}.png")
    plt.savefig(out_path, dpi=130)
    plt.close(fig)  # 明示的に閉じる


# 画像のフォルダを開く
os.startfile(os.path.realpath(output_fol_path))
