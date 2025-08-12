# trajectory-heatmap-tool-mit
人流データのトラジェクトリー（軌跡）をヒートマップと動線グラフで可視化するPythonツールです。
イベント会場や施設内での滞留エリアや移動パターンの把握に役立ちます。

# 機能
- 位置データを基にした2Dヒートマップの作成
- 指定した複数IDの動線を色分けして重ねて表示
- 動線の開始地点にIDラベルを表示(任意）
- 動線に進行方向の矢印を付加
- 画像ファイルとして保存

# 動作環境
Python3系が必要です。  

必要なパッケージは以下のコマンドでインストールしてください。
```
pip install pandas matplotlib numpy
```


# フォルダ構成例
```
├── 1_flow/
│   └── overlap_graphs.py       # メインスクリプト
├── 2_data/
│   └── sample.csv              # 入力データ（縦持ち形式）
├── 3_output/
│   └──                        # 画像出力先
```

# 使い方
このスクリプトは、コマンドライン操作なしで、ファイルをダブルクリックするだけで実行できます。

- 2_data/sample.csv に人流データを用意してください。
- 必須カラム: id, time_step, x, y
- 例: ユニークなIDごとに時間順に座標データを縦持ち形式で記録
- 1_flow/overlap_graphs.py を実行すると、
- 3_output フォルダにヒートマップと動線を重ねた画像が出力されます。

# 入力データフォーマット例
2_data/sample.csv を参照ください。

## LICENSE
MIT License（詳細はLICENSEファイルをご参照ください）

#### 開発者： iwakazusuwa(Swatchp)

