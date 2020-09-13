import numpy as np
import cairo 
from scipy import ndimage

def surface_to_np(surface):
    buf = surface.get_data()
    shape = (surface.get_height(), surface.get_width(), 4)
    np_img = np.ndarray(shape = shape, dtype = np.uint8, buffer = buf).astype(np.int32)
    np_img = np_img[:, :, :3].swapaxes(0, 1)
    return np_img

def PIL_to_np(PIL_img):
    np_img = np.array(PIL_img).astype(np.int32)
    np_img = np_img.swapaxes(0, 1)
    return np_img

def img_diff(img_1, img_2):
    return np.sqrt(np.sum((img_1 - img_2) ** 2, axis = -1))

def get_gradient(img):
    img_np_int = PIL_to_np(img.convert(mode = 'I'))
    gradient_x = ndimage.sobel(img_np_int, 0)
    gradient_y = ndimage.sobel(img_np_int, 1)
    return gradient_x, gradient_y