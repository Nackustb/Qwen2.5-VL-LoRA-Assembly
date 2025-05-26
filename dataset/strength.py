import os
from PIL import Image, ImageEnhance
import numpy as np
import random

input_dir = 'images'
output_dir = 'images_augmented'
os.makedirs(output_dir, exist_ok=True)

def add_noise(img):
    np_img = np.array(img)
    noise = np.random.randint(0, 30, np_img.shape, dtype='uint8')
    np_img = np.clip(np_img + noise, 0, 255).astype('uint8')
    return Image.fromarray(np_img)

def random_augment(img):
    choice = random.choice(['brightness', 'contrast', 'noise'])
    if choice == 'brightness':
        enhancer = ImageEnhance.Brightness(img)
        return enhancer.enhance(random.uniform(0.7, 1.3))
    elif choice == 'contrast':
        enhancer = ImageEnhance.Contrast(img)
        return enhancer.enhance(random.uniform(0.7, 1.3))
    elif choice == 'noise':
        return add_noise(img)

def main():
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            path = os.path.join(input_dir, filename)
            img = Image.open(path).convert('RGB')
            base_name = os.path.splitext(filename)[0]

            for i in range(5):  # 5次增强
                aug_img = random_augment(img)
                save_path = os.path.join(output_dir, f'{base_name}_aug{i+1}.jpg')
                aug_img.save(save_path)

if __name__ == '__main__':
    main()
