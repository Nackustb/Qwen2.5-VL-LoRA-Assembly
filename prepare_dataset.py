# import os
# import pandas as pd
# from PIL import Image

# # 设定你的数据集路径
# DATASET_DIR = 'dataset'  # 替换为你的数据集路径
# IMAGES_DIR = os.path.join(DATASET_DIR, 'images')  # 图片存储路径
# CAPTION_FILE = os.path.join(DATASET_DIR, 'image_descriptions.xlsx')  # 文字描述文件
# SAVE_DIR = 'train_dataset'  # 处理后的数据存储目录
# MAX_DATA_NUMBER = 1000  # 限制最大处理数量

# # 检查是否已经处理过
# if not os.path.exists(SAVE_DIR):
#     os.makedirs(SAVE_DIR, exist_ok=True)

#     # 读取 CSV 文件 
#     df = pd.read_excel(CAPTION_FILE)


#     # 限制数据量
#     df = df[:MAX_DATA_NUMBER]  

#     # 初始化存储列表
#     image_paths = []
#     captions = []

#     for i, row in df.iterrows():
#         image_id = row['图片路径']  # 图片文件名
#         caption = row['图片描述']  # 文字描述
#         image_path = os.path.join(IMAGES_DIR, image_id)  # 获取原始图片路径

#         # 检查图片是否存在
#         if not os.path.exists(image_path):
#             print(f"⚠️ 警告: {image_path} 不存在，跳过该图片。")
#             continue

#         # 读取并保存图片到新目录
#         new_image_path = os.path.abspath(os.path.join(SAVE_DIR, image_id))
#         image = Image.open(image_path)
#         image.save(new_image_path)

#         # 存储路径和描述
#         image_paths.append(new_image_path)
#         captions.append(caption)

#         # 进度显示
#         if (i + 1) % 50 == 0:
#             print(f'Processing {i+1}/{len(df)} images ({(i+1)/len(df)*100:.1f}%)')

#     # 保存新的 CSV 文件
#     processed_df = pd.DataFrame({'image_path': image_paths, 'caption': captions})
#     processed_df.to_csv(os.path.join(SAVE_DIR, 'processed_dataset.csv'), index=False)

#     print(f'✅ 数据处理完成，共处理 {len(image_paths)} 张图片')

# else:
#     print(f'✅ {SAVE_DIR} 目录已存在，跳过数据处理步骤。')

import pandas as pd
import json
import os
from tqdm import tqdm

# 载入 Excel 文件
df = pd.read_excel('dataset/image_descriptions.xlsx')

# 可选：重命名列，避免中文出错（根据实际情况修改）
df = df.rename(columns={
    '图片路径': 'image_path',
    '图片描述': 'caption'
})

conversations = []

# 构建对话数据
for i in tqdm(range(len(df)), desc="生成对话数据"):
    image_path = os.path.abspath(df.iloc[i]['image_path'])
    caption = df.iloc[i]['caption']

    conversations.append({
        "id": f"identity_{i+1}",
        "conversations": [
            {
                "from": "user",
                "value": f"<|vision_start|>{image_path}<|vision_end|>"
            },
            {
                "from": "assistant",
                "value": caption
            }
        ]
    })

# 保存为 JSON 文件
with open('dataset/data_vl.json', 'w', encoding='utf-8') as f:
    json.dump(conversations, f, ensure_ascii=False, indent=2)

print("✅ JSON 文件已生成：dataset/data_vl.json")
print("数据集准备完成！")