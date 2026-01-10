import os
import shutil

# ===== 設定區 =====
input_dir = "B"
output_dir = "C"
# ==================

os.makedirs(output_dir, exist_ok=True)
valid_ext = (".jpg", ".jpeg", ".png", ".webp", ".bmp")

files = [f for f in os.listdir(input_dir) if f.lower().endswith(valid_ext)]
total = len(files)

for i, filename in enumerate(files, start=1):
    src_path = os.path.join(input_dir, filename)

    stem, ext = os.path.splitext(filename)

    # 建立資料夾：C/01/
    dst_folder = os.path.join(output_dir, stem)
    os.makedirs(dst_folder, exist_ok=True)

    # 複製檔案：C/01/01.jpg
    dst_path = os.path.join(dst_folder, filename)

    shutil.copy2(src_path, dst_path)

    print(f"[{i}/{total}] 複製 {filename} → {dst_path}")

print("✅ 全部完成（僅建立資料夾並複製檔案）")
