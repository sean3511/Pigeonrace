import os
from PIL import Image

def resize_and_compress_images_in_subfolders(target_dir):
    # 遍歷目標資料夾下的子資料夾
    for folder_name in os.listdir(target_dir):
        subfolder_path = os.path.join(target_dir, folder_name)
        if os.path.isdir(subfolder_path):  # 只處理子資料夾
            for filename in os.listdir(subfolder_path):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    file_path = os.path.join(subfolder_path, filename)

                    try:
                        # 開啟圖片
                        with Image.open(file_path) as img:
                            # 獲取圖片的原始尺寸
                            original_size = img.size
                            print(f"Processing {file_path} (Original size: {original_size})")

                            # 將解析度減半
                            new_size = (original_size[0] // 2, original_size[1] // 2)
                            resized_img = img.resize(new_size, Image.Resampling.LANCZOS)  # 使用 LANCZOS

                            # 直接覆蓋原始檔案
                            resized_img.save(file_path, quality=85, optimize=True)
                            print(f"Replaced original image at {file_path}")
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")

def delete_compressed_files_in_subfolders(target_dir):
    # 刪除所有子資料夾中以 "compressed_" 開頭的檔案
    for folder_name in os.listdir(target_dir):
        subfolder_path = os.path.join(target_dir, folder_name)
        if os.path.isdir(subfolder_path):  # 只處理子資料夾
            for filename in os.listdir(subfolder_path):
                if filename.startswith("compressed_"):
                    file_path = os.path.join(subfolder_path, filename)
                    try:
                        os.remove(file_path)
                        print(f"Deleted file: {file_path}")
                    except Exception as e:
                        print(f"Error deleting file {file_path}: {e}")

if __name__ == "__main__":
    # 指定目標資料夾
    target_directory = r"D:\piegonrace_git\image\piegon_album_winter"  # 請確保此路徑正確
    print(f"Starting image processing in subfolders of {target_directory}")

    # 刪除舊的 "compressed_" 文件
    delete_compressed_files_in_subfolders(target_directory)

    # 調整解析度並覆蓋原始圖片
    resize_and_compress_images_in_subfolders(target_directory)

    print("Image processing completed.")
