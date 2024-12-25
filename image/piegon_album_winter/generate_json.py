import os
import json
import sys

def generate_json_from_directory(directory):
    result = []
    
    for folder_name in os.listdir(directory):
        folder_path = os.path.join(directory, folder_name)
        
        if os.path.isdir(folder_path):
            images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
            if images:
                title = folder_name
                image = ','.join(images)
                thumbnail = images[0]  # 默認第一張圖作為縮圖
                
                result.append({
                    "title": title,
                    "image": image,
                    "thumbnail": thumbnail
                })
    
    # 將結果按 title 進行排序
    result.sort(key=lambda x: x['title'].lower())
    
    return result

def main():
    # 獲取當前運行的 .exe 文件所在的目錄
    if getattr(sys, 'frozen', False):
        directory = os.path.dirname(sys.executable)  # 使用 sys.executable
    else:
        directory = os.path.dirname(os.path.abspath(__file__))  # 使用原始腳本文件路徑
    
    json_data = generate_json_from_directory(directory)
    
    output_file = os.path.join(directory, 'data.json')  # 將文件名稱改為 data.json
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
    
    print(f"JSON data has been saved to {output_file}")

if __name__ == "__main__":
    main()
