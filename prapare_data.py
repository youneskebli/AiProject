
from PIL import Image
import os
import numpy as np
import cv2

def scale_image(input_image_path,input_label_path,
                output_label_path,
                width=None,
                height=None
                ):
    original_image = Image.open(input_image_path)
    original_label = Image.open(input_label_path)
    w, h = original_image.size
    print('The original image size is {wide} wide x {height} '
          'high'.format(wide=w, height=h))
    original_label = original_label.resize((w, h), Image.ANTIALIAS)
    original_label.save(output_label_path)
    scaled_label = Image.open(output_label_path)
    width, height = scaled_label.size
    print('The scaled label size is {wide} wide x {height} '
          'high'.format(wide=width, height=height))

def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result

def scale_image_WithPadding(input_image_path,
                output_image_path,
                width=None,
                height=None
                ):
    original_image = Image.open(input_image_path)
    original_image = original_image.convert('RGB')
    max_size = (width, height)
    original_image.thumbnail(max_size, Image.ANTIALIAS)
    w, h = original_image.size
    print(w, h)
    if w < width:
        left = round(width - w)
        right = width - w - left
        top = round(height - h)
        bottom = height - h - top
        original_image = add_margin(original_image, 0, right, 0, left, (0, 0, 0))
    if h < height:
        top = round(height - h)
        bottom = height - h - top
        original_image = add_margin(original_image, top, 0, bottom, 0, (0, 0, 0))
    w2, h2 = original_image.size
    print((w2, h2))
    original_image.save(output_image_path)

def digitize_image(input_image_path,
                output_image_path,
                width=None,
                height=None
                ):
    original_image = Image.open(input_image_path)
    original_image = original_image.convert('RGB')#RGM-A to RGB
    arr = np.array(original_image)
    arr[np.all(arr!=[255, 255, 0],axis=2)] = [0,0,0]
    median_blur= cv2.medianBlur(arr, 5)
    median_blur= cv2.medianBlur(median_blur, 5)
    median_blur= cv2.medianBlur(median_blur, 3)
    median_blur= cv2.medianBlur(median_blur, 3)
    median_blur[np.all(median_blur!=[255, 255, 0],axis=2)] = [0,0,0]  
    
    im = Image.fromarray(median_blur)
    
    im.save(output_image_path)  

lst_1  = "/google-images-download-master/images/All/RawImage"
lst_2 = "/google-images-download-master/images/All/RawLabel"
lst_3 = "/google-images-download-master/images/All/ResizeLabel"
    
if __name__ == '__main__':  
        #determine the most common image size
    for count, filename in enumerate(os.listdir(lst_1)):         
        if 'png' not in filename or filename == 'image_8.jpg':
            continue
        scale_image(input_image_path = lst_1 + '/'+ filename,
                input_label_path = lst_2 + '/' + filename[:-4]+'_post.png',
                output_label_path = lst_3 + '/' + filename[:-4]+'_post.png',
                height = 480, width = 720)
        