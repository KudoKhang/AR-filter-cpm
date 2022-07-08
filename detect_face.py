from FaceBoxes import FaceBoxes
import cv2
import numpy as np

def draw(bbox, img):
    x1 ,y1, x2, y2 = np.uint32(bbox)
    cv2.rectangle(img, (x1 ,y1), (x2, y2), (255, 0, 255), 2)

# backup
# def parse_roi_box_from_bbox(bbox):
#     left, top, right, bottom = bbox[:4]
#     old_size = (right - left + bottom - top) / 2
#     center_x = right - (right - left) / 2.0
#     center_y = bottom - (bottom - top) / 2.0 + old_size * 0.14
#     size = int(old_size * 1.58)
#     roi_box = [0] * 4
#     roi_box[0] = center_x - size / 2
#     roi_box[1] = center_y - size / 2
#     roi_box[2] = roi_box[0] + size
#     roi_box[3] = roi_box[1] + size
#     return roi_box

def parse_roi_box_from_bbox(bbox):
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

def restore_img(img, img_ori, bbox):
    x1, y1, x2, y2 = np.uint32(bbox)
    size = (x2 - x1, y2 - y1)
    # img = cv2.resize(img, size)
    x1 , y1 = ((119 + 51) // 2), ((93 + 76) // 2)
    img_ori[y1: y1 + 256, x1: x1 + 256] = img
    return img_ori

face_bbox = FaceBoxes()
img = cv2.imread('tests/4.jpg')
img_origin = img.copy()
bbox = face_bbox(img)

def crop(bbox, img):
    x1, y1, x2, y2 = np.uint32(bbox)
    img = img[y1:y2, x1:x2]
    return img

for bb in bbox:
    bb = parse_roi_box_from_bbox(bb)
    # draw(bb, img)
    img = crop(bb, img_origin)
    print(img.shape)
    cv2.imshow('Result', img)
    cv2.waitKey(0)

# bbox = parse_roi_box_from_bbox(bb)
# img = crop(bbox, img)
# # img = restore_img(img, img_origin, bbox)
# # img = draw(bbox, img)
# cv2.imwrite('test.png', img)
# cv2.imshow('Result', img)
# print(bbox, bbox[2] - bbox[0], bbox[3] - bbox[1])
# cv2.waitKey(0)
