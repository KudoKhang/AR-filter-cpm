import os
import cv2
import numpy as np
from modules.makeup import Makeup
import warnings
warnings.filterwarnings('ignore')
from FaceBoxes import FaceBoxes

class AddSticker:
    def __int__(self):
        pass

    def check_input(self, img_path):
        if type(img_path) == str:
            if img_path.endswith(('.jpg', '.png', '.jpeg')):
                img = cv2.imread(img_path)
            else:
                raise Exception("Please input a image file")
        elif type(img_path) == np.ndarray:
            img = img_path
        return img

    def process_sticker(self, path_sticker):
        sticker = self.check_input(path_sticker)
        sticker = cv2.resize(sticker, (256, 256))
        sticker_g = cv2.cvtColor(sticker, cv2.COLOR_BGR2GRAY)
        _, sticker_t = cv2.threshold(sticker_g, 10, 255, cv2.THRESH_BINARY_INV)
        return sticker, sticker_t

    def add(self, img, sticker, sticker_t):
        sticker_no_focus = cv2.add(img, sticker, mask=sticker_t)
        return sticker_no_focus + sticker

    def blend(self, result, ori):
        result = result.astype("uint8")
        result_g = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        _, result_t = cv2.threshold(result_g, 5, 255, cv2.THRESH_BINARY_INV)
        ori_no_focus = cv2.bitwise_and(ori, ori, mask=result_t)
        final = cv2.add(result, ori_no_focus)
        return final

    def transform_to_square_bbox(self, bbox):
        left, top, right, bottom = bbox[:4]
        old_size = (right - left + bottom - top) / 2
        center_x = right - (right - left) / 2.0
        center_y = bottom - (bottom - top) / 2.0 + old_size * 0.03
        size = int(old_size * 1.25)
        roi_box = [0] * 4
        roi_box[0] = center_x - size / 2
        roi_box[1] = center_y - size / 2
        roi_box[2] = roi_box[0] + size
        roi_box[3] = roi_box[1] + size
        return roi_box

    def crop(self, bbox, img):
        x1, y1, x2, y2 = np.uint32(bbox)
        img = img[y1:y2, x1:x2]
        return cv2.resize(img, (256, 256))

    def process_input(self, path_input):
        face_bbox = FaceBoxes()
        img = self.check_input(path_input)
        img_origin = img.copy()
        bbox = face_bbox(img)
        return img, img_origin, bbox

    def restore_img(self, img, img_ori, bbox):
        x1, y1, x2, y2 = np.uint32(bbox)
        size = (x2 - x1, y2 - y1)
        img = cv2.resize(img, size)
        img_ori[y1: y2, x1: x2] = img
        return img_ori

    def save_result(self, path_input, savedir, result):
        if '/' in path_input:
            img_name = path_input.split('/')[-1].split('.')[0]
        else:
            img_name = path_input.split('.')[0]
        if not os.path.exists(savedir):
            os.mkdir(savedir)
        fn_path = os.path.join(savedir, f'{img_name}.png')
        cv2.imwrite(fn_path, result)
        print('Save result 👉: ', fn_path)

    def run(self, path_input, path_sticker, is_Save=True, savedir='output'):
        img_A, img_A_origin, bbox = self.process_input(path_input)
        model = Makeup()
        for bb in bbox:
            bb = self.transform_to_square_bbox(bb)
            img_A = self.crop(bb, img_A_origin)
            model.prn_process(img_A)
            A_txt = model.get_texture()
            sticker, sticker_t = self.process_sticker(path_sticker)
            result = self.add(A_txt, sticker, sticker_t)
            output = model.render_texture(result)
            final = self.blend(output, img_A)
            final_of_final = self.restore_img(final, img_A_origin, bb)
        if is_Save:
            self.save_result(path_input, savedir, final_of_final)
        return final_of_final