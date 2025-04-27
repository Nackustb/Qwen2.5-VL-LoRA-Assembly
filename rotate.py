from PIL import Image
import os

def rotate_image(image_path, output_dir):
    # 打开图片并检查其长宽
    with Image.open(image_path) as im:
        orig_width, orig_height = im.size

        # 如果图片是竖着的，旋转 90 度
        if orig_height > orig_width:
            im = im.rotate(90, expand=True)  # expand=True 会调整图片大小以适应旋转后的尺寸

        # 确定保存路径
        output_image_path = os.path.join(output_dir, os.path.basename(image_path))
        im.save(output_image_path)

        print(f"图片已保存为: {output_image_path}")

if __name__ == "__main__":
    input_folder = "dataset/images"  # 输入图片文件夹
    output_folder = "dataset/rotated_images"  # 输出文件夹

    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 遍历输入文件夹中的所有图片
    for image_file in os.listdir(input_folder):
        image_path = os.path.join(input_folder, image_file)
        
        # 检查是否是图片文件
        if image_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            rotate_image(image_path, output_folder)

    print("所有图片处理完成！")
