import cv2
import numpy as np
import os
import json

class ConvertImage(object):
    def __init__(self, file_path):
        self.__file_path = file_path
        self.image_json = []
        self.request_base_dir = 'http://www.xiaomaidong.com/fuyuko/images/'
        self.small_url = ''
        self.middle_url = ''
        self.list_image(self.__file_path)


    def resize_picture(self, image, image_name):
        image_info = {}
        shape = np.shape(image)
        print(shape)
        small_shape = self.get_small_shape(shape)
        # small_image = cv2.resize(image, small_shape)

        # cv2.imshow(image_name, small_image)
        # cv2.imwrite(self.__small_path + '/' + image_name, small_image)
        middle_shape = self.get_middle_shape(shape)
        # middle_image = cv2.resize(image, middle_shape)
        # cv2.imwrite(self.__middle_path + '/' + image_name, middle_image)

        image_info['small'] = self.small_url + '/' + image_name
        image_info['middle'] = self.middle_url + '/' + image_name
        image_info['small_width'] = small_shape[0]
        image_info['small_height'] = small_shape[1]
        image_info['middle_width'] = middle_shape[0]
        image_info['middle_height'] = middle_shape[1]
        image_info['desc'] = image_name
        image_info['type'] = self.type
        self.image_json.append(image_info)
        print(image_name, ' process finish')

    def get_small_shape(self, shape):
        width = shape[1]
        height = shape[0]
        # 针对单反拍的照片，分辨率通常在5000以上
        if width >= 5000:
            return (width // 10, height // 10)

        # 针对航拍的照片
        elif 2000 < width < 5000:
            return (width // 8, height // 8)

        # 针对QQ空间下载的照片
        elif width <= 2000:
            return (width // 3, height // 3)

    def get_middle_shape(self, shape):
        width = shape[1]
        height = shape[0]

        if width > height:
            new_width = 1920
            height = new_width * (height / width)
            return (int(new_width), int(height))
        else:
            new_height = 1920
            width = new_height * (width / height)
            return (int(width), int(new_height))

    def list_image(self, path):
        waste_file = '.DS_Store'
        file_list = os.listdir(path)  # 该文件夹下所有的文件（包括文件夹）
        file_list.remove(waste_file)
        for files in file_list:
            img_dir = os.path.join(path, files)
            self.__small_path = os.path.join(img_dir, 'small')
            self.__middle_path = os.path.join(img_dir, 'middle')
            self.small_url = self.request_base_dir + files + '/small'
            self.middle_url = self.request_base_dir + files + '/middle'
            self.type = files
            img_list = os.listdir(img_dir)
            img_list.remove(waste_file)
            for img in img_list:
                if img.find('.') != -1:
                    image = cv2.imread(os.path.join(img_dir, img))
                    self.resize_picture(image, img)

        with open('image_json.json', 'w', encoding='utf-8') as w:
            json.dump(self.image_json, w)


if __name__ == '__main__':
    ci = ConvertImage("/Users/maicius/Pictures/2018宝宝/")
