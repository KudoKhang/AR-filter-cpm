import os

import cv2
import numpy as np
from makeup import Makeup
from PIL import Image
import argparse
import warnings
warnings.filterwarnings('ignore')

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="cpu", type=str)
    parser.add_argument("--prn", default=True, type=bool)
    parser.add_argument("--input", type=str, default="tests/input.jpg", help="Path to input image (face have save 256 * 256)")
    parser.add_argument("--style", type=str, default="tests/fillter256.png", help="Path to sticker (h=w) in Face Texture")
    parser.add_argument("--savedir", type=str, default=".")
    args = parser.parse_args()
    print("           ⊱ ──────ஓ๑♡๑ஓ ────── ⊰")
    print("🎵 hhey, arguments are here if you need to check 🎵")
    for arg in vars(args):
        print("{:>15}: {:>30}".format(str(arg), str(getattr(args, arg))))
    print()
    return args

class AddSticker:
    def __int__(self):
        pass

    def process_sticker(self, path_sticker):
        sticker = cv2.imread(path_sticker)
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

    def check_input(self, img_path):
        if type(img_path) == str:
            if img_path.endswith(('.jpg', '.png', '.jpeg')):
                img = cv2.imread(img_path)
            else:
                raise Exception("Please input a image file")
        elif type(img_path) == np.ndarray:
            img = img_path
        return img

    def run(self, path_input: np.ndarray, path_sticker: np.ndarray, is_Save=True, savedir='.'):
        img_A = self.check_input(path_input)
        model = Makeup()
        model.prn_process(img_A)

        A_txt = model.get_texture()

        sticker, sticker_t = self.process_sticker(path_sticker)
        result = self.add(A_txt, sticker, sticker_t)
        output = model.render_texture(result)
        final = self.blend(output, img_A)
        if is_Save:
            fn_path = os.path.join(savedir, 'result.png')
            cv2.imwrite(fn_path, final)
            print('Save result 👉: ', fn_path)
        return final

if __name__ == "__main__":
    args = get_args()
    add_sticker = AddSticker()
    output = add_sticker.run(args.input, args.style)