
# 🧠 Quantum Annealing for Vertex Cover Problem

本專案使用 **量子退火（Quantum Annealing）** 方法求解 **頂點覆蓋問題（Vertex Cover Problem）**，並可成功解出 `keller4.mis` 資料集，找到大小為 160 的最小覆蓋集。

---

## 📁 專案結構

```
.
├── main.py                     # 主程式：使用 D-Wave Ocean SDK 建立 QUBO 並模擬退火
├── dataset/                    # 存放測試資料集（例如 keller4.mis）
├── report.pdf                  # 報告檔案
└── README.md                   # 專案說明文件
```

---

## 🧪 使用技術

- Python 3.x
- NetworkX（圖資料處理）
- D-Wave Ocean SDK（量子退火模擬器）
- `dimod`, `dwave.samplers`, `dwavebinarycsp` 等

---

## 🚀 如何執行

### ✅ 1. 安裝依賴套件

手動安裝：

```bash
pip install dwave-ocean-sdk
pip install pyqubo
```

### ✅ 2. 執行程式

開啟 `main.ipynb` 並依序執行區塊，或將主流程轉成 `.py` 檔在 CLI 執行：

```bash
python main.py
```

---

## 🧪 如何進行實驗

### ✅ 匯入資料集

將 `.mis` 格式的圖檔（如 `keller4.mis`）放入 `dataset/` 資料夾內。  
支援 DIMACS MIS 格式（開頭 `p edge`, 接著多行 `e u v` 表示邊）。

### ✅ 執行參數調整（權重 A）

可修改程式中懲罰項係數 `A`：

```python
A = 3  # 懲罰違規邊的強度
B = 1   # 固定為 1，代表覆蓋點數的權重
```

可根據圖大小調整 A，推薦值如下：

| 節點數 | 推薦 A 值 |
|--------|-----------|
| 170    | 2 ~ 4     |
| 300    | 3 ~ 6     |
| 700    | 5 ~ 10    |
| 775    | 6 ~ 12    |
| 1500   | 8 ~ 15    |
| 3360   | 12 ~ 25   |

---

## ✅ 輸出格式

程式將輸出：

- 最小覆蓋集合的大小（如：160）
- 覆蓋的節點編號（可選擇輸出）
- 是否為合法覆蓋（覆蓋所有邊）

---

## 📌 成果驗證

本專案已成功驗證以下資料集（包含大型密集圖）：

- `keller4.mis` ✅（輸出點數 = 160，合法）
- `keller5.mis` ✅（輸出點數 = 751，合法）
- `keller6.mis` ✅（輸出點數 = 3318，合法）
- `p_hat300-1.mis` ✅（輸出點數 = 292，合法）
- `p_hat700-1.mis` ✅（輸出點數 = 689，合法）
- `p_hat1500-1.mis` ✅（輸出點數 = 1490，合法）
- 支援任意 `.mis` 格式圖
