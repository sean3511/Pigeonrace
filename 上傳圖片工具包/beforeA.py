# -*- coding: utf-8 -*-
"""
beforeA.py   ---  BeforeA  ->  A

用途：
    把 BeforeA 資料夾裡「命名不規律」的圖片，自動找出檔名中的「連號欄位」，
    依連號順序重新命名成 01 / 02 / 03 ... 放進 A 資料夾。
    （副檔名維持原本的，不限於 jpg）

原理：
    1. 把每個檔名裡所有的數字都抓出來，例如
         "B 01   26-308567   12X16X1   6X8X1"
         ->  [01, 26, 308567, 12, 16, 1, 6, 8, 1]
    2. 逐一測試「第 N 個數字」這個欄位（左數 0,1,2... 與右數 -1,-2,...），
       看看哪一個欄位在所有檔案之間剛好構成一組不重複、幾乎連續的號碼。
       重複的欄位（貨號前綴 26、尺寸 12X16）會直接被淘汰。
    3. 分數最高的那個欄位就是「連號」，依它排序後重新命名。
    4. 完全找不到連號時，改用自然排序（natural sort）當備援，並印出警告。

註：資料夾一律以「這支 .py 檔所在的位置」為基準，
    所以在哪個目錄下執行都不會找不到 BeforeA。
"""

import os
import re
import shutil

# ===== 設定區 =====
input_dir   = "BeforeA"
output_dir  = "A"
mode        = "copy"    # "copy" = 保留原檔（建議） / "move" = 直接搬走
pad         = 0         # 0 = 自動（依檔案數決定 2 位或 3 位）；也可自己指定 2 / 3
dry_run     = False     # True = 只預覽不動檔案
overwrite_A = True     # A 資料夾已有檔案時是否照樣寫入
min_score   = 0.55      # 連號欄位的最低「連續度」門檻（0~1）
# ==================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VALID_EXT = (".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff", ".gif", ".heic")
NUM_RE = re.compile(r"\d+")


# ---------- 工具 ----------
def resolve(p):
    """相對路徑一律相對於這支 .py 所在的資料夾。"""
    return p if os.path.isabs(p) else os.path.join(BASE_DIR, p)


def find_dir_ci(parent, name):
    """在 parent 底下找 name 資料夾，找不到就用不分大小寫再找一次。"""
    p = os.path.join(parent, name)
    if os.path.isdir(p):
        return p
    try:
        for d in os.listdir(parent):
            if d.lower() == name.lower() and os.path.isdir(os.path.join(parent, d)):
                return os.path.join(parent, d)
    except OSError:
        pass
    return None


def natural_key(name: str):
    """自然排序：讓 file2 排在 file10 前面。"""
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", name)]


def tokens_of(stem: str):
    """回傳檔名中所有數字：[(值, 原始字串, 起始位置), ...]"""
    return [(int(m.group()), m.group(), m.start()) for m in NUM_RE.finditer(stem)]


def score_field(values, raws, idx):
    """
    評分某個數字欄位當「連號」的可能性。
    回傳 (分數, 連續度)；分數 < 0 表示不合格。
    """
    n = len(values)
    if n == 0:
        return -1.0, 0.0

    # 1) 連號必須不重複（貨號前綴、尺寸這類重複值會在這裡被淘汰）
    if len(set(values)) != n:
        return -1.0, 0.0

    span = max(values) - min(values) + 1
    cont = n / span                      # 連續度：1.0 = 完美連號 1..N

    # 合格條件：連續度夠高，或者號碼本身夠小（例如 1,2,3,10 這種有跳號的序號）
    small = max(values) <= max(n * 4, 20)
    if cont < min_score and not (small and cont >= 0.2):
        return -1.0, cont

    score = cont * 100.0
    if small:
        score += 5.0

    # 2) 從 0 或 1 開始的加分
    if min(values) in (0, 1):
        score += 15.0

    # 3) 固定位數（有補零）的加分，例如 01,02,...,36
    widths = {len(r) for r in raws}
    if len(widths) == 1:
        score += 8.0
    if any(len(r) > 1 and r[0] == "0" for r in raws):
        score += 8.0

    # 4) 數值範圍合理（連號通常不會是六位數貨號）
    if max(values) <= n * 3:
        score += 10.0
    elif max(values) > 10000:
        score -= 15.0

    # 5) 偏好靠前的欄位（人習慣把序號放前面）
    score -= abs(idx) * 1.5
    if idx < 0:
        score -= 2.0

    return score, cont


def detect_serial(files):
    """回傳 (取號函式, 說明字串)；找不到連號時回傳 (None, 原因)。"""
    toks = {f: tokens_of(os.path.splitext(f)[0]) for f in files}
    counts = [len(t) for t in toks.values()]
    if not counts or max(counts) == 0:
        return None, "檔名裡完全沒有數字"

    candidates = []
    max_len = max(counts)

    # 左數欄位 0..max_len-1，右數欄位 -1..-max_len
    for idx in list(range(max_len)) + [-(i + 1) for i in range(max_len)]:
        values, raws = [], []
        ok = True
        for f in files:
            t = toks[f]
            j = idx if idx >= 0 else len(t) + idx
            if j < 0 or j >= len(t):
                ok = False
                break
            values.append(t[j][0])
            raws.append(t[j][1])
        if not ok:
            continue
        s, cont = score_field(values, raws, idx)
        if s > 0:
            candidates.append((s, cont, idx, values))

    if not candidates:
        return None, "找不到任何不重複且連續的數字欄位"

    candidates.sort(key=lambda x: -x[0])
    best_score, cont, idx, values = candidates[0]

    def get_num(fname):
        t = toks[fname]
        j = idx if idx >= 0 else len(t) + idx
        return t[j][0]

    pos = f"左數第 {idx + 1} 個數字" if idx >= 0 else f"右數第 {-idx} 個數字"
    gaps = (max(values) - min(values) + 1) - len(values)
    desc = (f"連號欄位 = {pos}"
            f"（範圍 {min(values)}~{max(values)}，連續度 {cont:.0%}"
            f"{'，中間跳過 %d 號' % gaps if gaps else '，完整連號'}）")
    return get_num, desc


# ---------- 主程式 ----------
def main():
    src_dir = find_dir_ci(BASE_DIR, input_dir) if not os.path.isabs(input_dir) else input_dir
    if not src_dir or not os.path.isdir(src_dir):
        print(f"❌ 找不到來源資料夾：{resolve(input_dir)}")
        print(f"   （腳本位置：{BASE_DIR}）")
        return
    dst_dir = resolve(output_dir)

    files = sorted(
        (f for f in os.listdir(src_dir)
         if not f.startswith(".") and f.lower().endswith(VALID_EXT)),
        key=natural_key,
    )
    total = len(files)
    if total == 0:
        print(f"❌ {src_dir} 裡沒有可處理的圖片")
        return

    if os.path.isdir(dst_dir) and os.listdir(dst_dir) and not overwrite_A and not dry_run:
        print(f"⚠️  {dst_dir} 資料夾已經有東西了。")
        print("    請先清空，或把設定區的 overwrite_A 改成 True。")
        return

    # --- 找連號 ---
    get_num, desc = detect_serial(files)
    if get_num is None:
        print(f"⚠️  {desc} → 改用自然排序（依檔名順序），請自行確認順序是否正確")
        ordered = files
    else:
        print(f"🔎 {desc}")
        ordered = sorted(files, key=lambda f: (get_num(f), natural_key(f)))

    width = pad if pad > 0 else max(2, len(str(total)))

    # --- 產生對照 ---
    plan = []
    for i, f in enumerate(ordered, start=1):
        ext = os.path.splitext(f)[1].lower()
        if ext == ".jpeg":
            ext = ".jpg"
        plan.append((f, f"{i:0{width}d}{ext}"))

    # --- 檢查撞名 ---
    news = [n for _, n in plan]
    if len(set(news)) != len(news):
        print("❌ 產生的新檔名有重複，已中止（請檢查是否有同序號不同副檔名）")
        return

    print(f"📋 共 {total} 個檔案：{os.path.basename(src_dir)} → {os.path.basename(dst_dir)}"
          f"（{'預覽' if dry_run else mode}）")
    for old, new in plan:
        print(f"    {new}  ←  {old}")

    if dry_run:
        print("🟡 dry_run = True，未實際處理任何檔案")
        return

    os.makedirs(dst_dir, exist_ok=True)
    act = shutil.move if mode == "move" else shutil.copy2

    for i, (old, new) in enumerate(plan, start=1):
        act(os.path.join(src_dir, old), os.path.join(dst_dir, new))
        print(f"[{i}/{total}] {old} → {new}")

    print(f"✅ 全部完成，{total} 個檔案已放進 {dst_dir}（接著可以跑 01resize.py）")


if __name__ == "__main__":
    main()
