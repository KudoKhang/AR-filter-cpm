import cv2
import numpy as np
import tensorflow as tf
import torch
import utils.net as net
from PIL import Image
from utils.api import PRN
from utils.render import prepare_tri_weights, render_by_tri, render_texture
from utils.utils import de_norm, to_tensor, to_var

class Makeup:
    def __init__(self):
        self.prn = PRN(is_dlib=True)

    def prn_process(self, face):
        # --- face
        self.face = cv2.resize(face, (256, 256))
        self.pos = self.prn.process(self.face)
        self.vertices = self.prn.get_vertices(self.pos)
        #         self.face = face/255
        self.h, self.w, _ = self.face.shape
        self.triangles = self.prn.triangles
        vis_colors = np.ones((self.vertices.shape[0], 1))
        face_mask = render_texture(self.vertices.T, vis_colors.T, self.triangles.T, self.h, self.w, c=1)
        self.face_mask = np.squeeze(face_mask > 0).astype(np.float32)
        self.weights, self.dst_triangle_buffer = prepare_tri_weights(self.vertices.T, self.triangles.T, self.h, self.w)

        uv_face_eye = np.array(Image.open("./PRNet/uv-data/uv_face_eyes.png"))[:, :, :3] / 255
        new_colors = self.prn.get_colors_from_texture(uv_face_eye)
        new_colors = (new_colors > 0).astype("uint8")
        mask_out_eye = render_by_tri(
            new_colors.T,
            self.triangles.T,
            self.weights,
            self.dst_triangle_buffer,
            self.h,
            self.w,
            c=3,
        )
        self.mask_out_eye = (mask_out_eye > 0).astype("uint8")  # [:, :, np.newaxis]
        tf.reset_default_graph()

    def get_texture(self):
        texture = cv2.remap(
            self.face,
            self.pos[:, :, :2].astype(np.float32),
            None,
            interpolation=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=(0),
        )
        return texture

    def render_texture(self, texture, patt_only=False):
        new_colors = self.prn.get_colors_from_texture(texture)
        new_image = render_by_tri(
            new_colors.T,
            self.triangles.T,
            self.weights,
            self.dst_triangle_buffer,
            self.h,
            self.w,
            c=3,
        )
        return new_image