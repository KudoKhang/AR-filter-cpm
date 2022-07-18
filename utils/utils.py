import matplotlib.pyplot as plt
import numpy as np
import torch
import cv2
from torch.autograd import Variable

def get_prefix(path_input):
    if '/' in path_input:
        img_name = path_input.split('/')[-1].split('.')[0]
    else:
        img_name = path_input.split('.')[0]
    return img_name

def check_input(img_path):
    if type(img_path) == str:
        if img_path.endswith(('.jpg', '.png', '.jpeg')):
            img = cv2.imread(img_path)
        else:
            raise Exception("Please input a image file")
    elif type(img_path) == np.ndarray:
        img = img_path
    return img

def matplotlib_imshow(img, one_channel=False):
    if one_channel:
        img = img.mean(dim=0)
    img = img / 2 + 0.5  # unnormalize
    npimg = img.numpy()
    if one_channel:
        plt.imshow(npimg, cmap="Greys")
    else:
        plt.imshow(np.transpose(npimg, (1, 2, 0)))

def to_tensor(x, **kwargs):
    return x.transpose(2, 0, 1).astype("float32")

def ToTensor(pic):
    img = torch.from_numpy(np.array(pic, np.int16, copy=False))
    nchannel = 3
    img = img.view(pic.size[1], pic.size[0], nchannel)
    img = img.transpose(0, 1).transpose(0, 2).contiguous()
    if isinstance(img, torch.ByteTensor):
        return img.float()
    else:
        return img


def de_norm(x):
    out = (x + 1) / 2
    return out.clamp(0, 1)

def to_var(x, requires_grad=True):
    if not requires_grad:
        return Variable(x, requires_grad=requires_grad)
    else:
        return Variable(x)