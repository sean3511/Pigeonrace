from PIL import Image
import os

# ===== 設定區 =====
input_dir = "A"
output_dir = "B"
target_width = 1280
# 指定圖片寬度
jpg_quality = 85       # 75~90
webp_quality = 80      # 60~85
png_optimize = True
# ==================

os.makedirs(output_dir, exist_ok=True)
valid_ext = (".jpg", ".jpeg", ".png", ".webp")

def fmt_size(n):
    for u in ["B","KB","MB","GB"]:
        if n < 1024:
            return f"{n:.1f}{u}"
        n /= 1024
    return f"{n:.1f}TB"

files = [f for f in os.listdir(input_dir) if f.lower().endswith(valid_ext)]
total = len(files)
saved_total = 0

for i, filename in enumerate(files, start=1):
    in_path = os.path.join(input_dir, filename)
    out_path = os.path.join(output_dir, filename)

    before = os.path.getsize(in_path)

    with Image.open(in_path) as img:
        w, h = img.size

        # 👉 等比縮小（不放大）
        if w > target_width:
            scale = target_width / w
            new_size = (target_width, int(h * scale))
            img = img.resize(new_size, Image.BICUBIC)

        ext = os.path.splitext(filename)[1].lower()

        # JPG 不支援 alpha
        if ext in (".jpg", ".jpeg") and img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # 👉 依格式最佳化輸出
        if ext in (".jpg", ".jpeg"):
            img.save(out_path, quality=jpg_quality, optimize=True, progressive=True)

        elif ext == ".png":
            img.save(out_path, optimize=png_optimize)

        elif ext == ".webp":
            img.save(out_path, quality=webp_quality, method=6)

    after = os.path.getsize(out_path)
    saved = max(before - after, 0)
    saved_total += saved

    print(f"[{i}/{total}] {filename}  {fmt_size(before)} → {fmt_size(after)}  省 {fmt_size(saved)}")

print(f"✅ 全部完成，共省下 {fmt_size(saved_total)}")
