import os
from typing import Tuple

import PIL.Image
import cv2
import numpy as np
from PIL import Image


class ImageLoader:
    def __init__(self, main_path: str) -> None:
        images = [os.path.join(main_path, x) for x in os.listdir(main_path) if
                  '.jpg' in x]
        self.paths = images
        self.current_pos = 0
        self.current_image = None
        self.current_renamed_path = None
        self.was_current_image_processed = True

    def __len__(self):
        return len(self.paths)

    def __iter__(self):
        return self

    def __getitem__(self, item: int) -> str:
        return self.paths[item]

    def pick_next(self) -> str:
        self.current_pos += 1
        return self.paths[self.current_pos - 1]

    def cache_current_image(self, data: PIL.Image.Image, renamed_path: str) -> None:
        self.current_image = data
        self.current_renamed_path = renamed_path


def save_image(path: str, data: np.ndarray) -> None:
    image = PIL.Image.fromarray(data)
    image.save(path)
    print(f'saved: {path}')


def load_image(image_path: str) -> np.ndarray:
    raw_image = np.array(Image.open(image_path))
    if len(raw_image.shape) < 3:
        raw_image = cv2.imread(image_path)
    elif raw_image.shape[2] != 3:
        raw_image = np.array(Image.open(image_path).convert("RGB"))
    return raw_image


def rename_to_html_preferred_format(path: str) -> str:
    which_idx_is_static = path.split('/').index('static')
    return '/' + '/'.join(path.split('/')[which_idx_is_static:]).replace(' ', '%20')


def cut_to_square(data: np.ndarray, x_point: int, y_point: int) -> np.ndarray:
    """
    Cuts given image to square using (x, y) as an orientation point.

    """
    if data.shape[0] == data.shape[1]:
        return data
    smaller_dim = np.argmin(data.shape[:-1])
    bigger_dim = np.argmax(data.shape[:-1])
    out_image_side_len = data.shape[smaller_dim]

    min_boundary = data.shape[smaller_dim] // 2
    max_boundary = data.shape[bigger_dim] - min_boundary

    if smaller_dim:
        x_point = data.shape[smaller_dim] // 2
        y_point = int(
            fix_point_if_outside_boundary(y_point, min_boundary, max_boundary))
    else:
        y_point = data.shape[smaller_dim] // 2
        x_point = int(
            fix_point_if_outside_boundary(x_point, min_boundary, max_boundary))

    cut_image = data[
                max(0, y_point - out_image_side_len // 2): min(data.shape[0], y_point + out_image_side_len // 2),
                max(0, x_point - out_image_side_len // 2): min(data.shape[1], x_point + out_image_side_len // 2),
                :
                ]
    return cut_image


def fix_point_if_outside_boundary(point: int, min_bound: int, max_bound: int) -> int:
    return min(max_bound, max(min_bound, point))


def rescale_dims(image: np.ndarray, max_x: int, max_y: int) -> Tuple[int, int]:
    rescaled_x = image.shape[1]
    rescaled_y = image.shape[0]

    if rescaled_x > max_x:
        scale_factor = max_x / rescaled_x
        rescaled_x = int(rescaled_x * scale_factor)
        rescaled_y = int(rescaled_y * scale_factor)
    if rescaled_y > max_y:
        scale_factor = max_y / rescaled_y
        rescaled_x = int(rescaled_x * scale_factor)
        rescaled_y = int(rescaled_y * scale_factor)
    return rescaled_x, rescaled_y


def load_image_with_info(loader: ImageLoader) -> Tuple[np.ndarray, str]:
    if loader.was_current_image_processed:
        img_path = loader.pick_next()
        image = load_image(img_path)
        refactored_path = rename_to_html_preferred_format(img_path)
        loader.cache_current_image(image, refactored_path)
        loader.was_current_image_processed = False
        if image is None:
            loader.was_current_image_processed = True
            return load_image_with_info(loader)
    else:
        image = loader.current_image
        refactored_path = loader.current_renamed_path

    return image, refactored_path
