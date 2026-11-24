# 錢錢大冒險

小學生生活理財與投資教育雙關卡遊戲。直接用瀏覽器開啟 `index.html` 即可遊玩，無須安裝套件。

## 操作方式

- `←` / `→` 或 `A` / `D`：移動角色
- `↑` 或空白鍵：跳躍
- `E`：靠近木箱時開始本關理財挑戰
- 答對挑戰取得鑰匙後，往右走到出口進入下一關
- 手機可使用畫面上的左右移動按鈕與互動按鈕

## 關卡

1. 家庭補給島：安排零用錢、儲蓄與生活需要。
2. 小小商店島：認識成本、合理定價與投資風險。

每關滿分 100 分；完成第二關會顯示總分與學習進步成果。

## Blender 角色資產

- `assets/soft-explorer.blend`：可編輯的 Blender 場景
- `assets/soft-explorer.glb`：可匯入遊戲引擎的 3D 角色與鑰匙模型
- `assets/soft-explorer-sprite.png`：遊戲中使用的透明背景角色渲染圖
- `assets/soft-explorer.png`：角色展示渲染圖
- `make_assets.py`：使用 Blender 背景模式重新生成模型與圖片

本工作區未找到 `C:\Godot` 或 Godot 執行檔；目前遊戲以可直接執行的 HTML 版本交付。
