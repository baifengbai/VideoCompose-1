"""
@Author: WSWSCSJ
@Description: 接受 numpy.ndarray 类型的图片变量,使用线性代数矩阵计算实现视频帧专场
"""
import numpy as np


def argument_detection(pictures):
    if not isinstance(pictures, list):
        raise TypeError("pictures must be list object")
    if len(pictures) != 2:
        raise ValueError("pictures limit 2")
    p1 = pictures[0]
    p2 = pictures[-1]
    if not isinstance(p1, np.ndarray) or not isinstance(p2, np.ndarray):
        raise TypeError("picture must be numpy.ndarray type object")
    if p1.ndim != 3 or p2.ndim != 3:
        raise ValueError("picture must be 3 dimension")


def default_cover(pictures, frames=10, step=1):
    argument_detection(pictures)
    rendered_pictures = []
    p1 = pictures[0].astype(np.float64)
    p2 = pictures[-1].astype(np.float64)
    rendered_pictures.extend([p1.copy().astype(np.uint8)] * (frames // (step * 2)))
    rendered_pictures.extend([p2.copy().astype(np.uint8)] * (frames // (step * 2)))
    return rendered_pictures


def right_straight_cover(pictures, frames=10, step=1):
    argument_detection(pictures)
    rendered_pictures = []
    p1 = pictures[0].astype(np.float64)
    p2 = pictures[-1].astype(np.float64)
    target = p1.copy()
    index_step = target.shape[1]*step//frames
    for i in range(frames//step):
        target[:, :(i+1)*index_step, :] = p2[:, :(i+1)*index_step, :]
        rendered_pictures.extend([target.copy().astype(np.uint8)]*step)
    return rendered_pictures


def left_straight_cover(pictures, frames=10, step=1):
    argument_detection(pictures)
    rendered_pictures = []
    p1 = pictures[0].astype(np.float64)
    p2 = pictures[-1].astype(np.float64)
    target = p1.copy()
    index_step = target.shape[1] * step // frames
    for i in range(frames // step):
        target[:, (frames - i - 1) * index_step:, :] = p2[:, (frames - i - 1) * index_step:, :]
        rendered_pictures.extend([target.copy().astype(np.uint8)] * step)
    return rendered_pictures


def up_straight_cover(pictures, frames=10, step=1):
    argument_detection(pictures)
    rendered_pictures = []
    p1 = pictures[0].astype(np.float64)
    p2 = pictures[-1].astype(np.float64)
    target = p1.copy()
    index_step = target.shape[0] * step // frames
    for i in range(frames // step):
        target[(frames - i - 1) * index_step:, :, :] = p2[(frames - i - 1) * index_step:, :, :]
        rendered_pictures.extend([target.copy().astype(np.uint8)] * step)
    return rendered_pictures


def down_straight_cover(pictures, frames=10, step=1):
    argument_detection(pictures)
    rendered_pictures = []
    p1 = pictures[0].astype(np.float64)
    p2 = pictures[-1].astype(np.float64)
    target = p1.copy()
    index_step = target.shape[0] * step // frames
    for i in range(frames // step):
        target[:(i + 1) * index_step, :, :] = p2[:(i + 1) * index_step, :, :]
        rendered_pictures.extend([target.copy().astype(np.uint8)] * step)
    return rendered_pictures


def center_straight_cover(pictures, frames=10, step=1):
    argument_detection(pictures)
    rendered_pictures = []
    p1 = pictures[0].astype(np.float64)
    p2 = pictures[-1].astype(np.float64)
    target = p1.copy()
    h_index_step = target.shape[0] * step // (frames * 2)
    w_index_step = target.shape[1] * step // (frames * 2)
    for i in range(frames // step):
        target[(frames * 2 - i - 1) * h_index_step:, :, :] = p2[(frames * 2 - i - 1) * h_index_step:, :, :]
        target[:(i + 1) * h_index_step, :, :] = p2[:(i + 1) * h_index_step, :, :]
        target[:, (frames * 2 - i - 1) * w_index_step:, :] = p2[:, (frames * 2 - i - 1) * w_index_step:, :]
        target[:, :(i + 1) * w_index_step, :] = p2[:, :(i + 1) * w_index_step, :]
        rendered_pictures.extend([target.copy().astype(np.uint8)] * step)
    return rendered_pictures


def border_straight_cover(pictures, frames=10, step=1):
    argument_detection(pictures)
    rendered_pictures = []
    p1 = pictures[-1].astype(np.float64)
    p2 = pictures[0].astype(np.float64)
    target = p1.copy()
    h_index_step = target.shape[0] * step // (frames * 2)
    w_index_step = target.shape[1] * step // (frames * 2)
    for i in range(frames // step):
        target[(frames * 2 - i) * h_index_step:, :, :] = p2[(frames * 2 - i) * h_index_step:, :, :]
        target[:i * h_index_step, :, :] = p2[:i * h_index_step, :, :]
        target[:, (frames * 2 - i) * w_index_step:, :] = p2[:, (frames * 2 - i) * w_index_step:, :]
        target[:, :i * w_index_step, :] = p2[:, :i * w_index_step, :]
        rendered_pictures.extend([target.copy().astype(np.uint8)] * step)
    return rendered_pictures[::-1]


def faded_cover(pictures, frames=10, step=1):
    argument_detection(pictures)
    rendered_pictures = []
    p1 = pictures[0].astype(np.float64)
    p2 = pictures[-1].astype(np.float64)
    target = p1.copy()
    short = (p2-p1)*step/frames
    for i in range(frames//step):
        target = target + short
        temp = [target.astype(np.uint8)] * step
        rendered_pictures.extend(temp)
    return rendered_pictures

class Render:

    renders = {
        "default": default_cover,
        "right_straight": right_straight_cover,
        "left_straignt": left_straight_cover,
        "up_straight": up_straight_cover,
        "down_straight": down_straight_cover,
        "center_straight": center_straight_cover,
        "border_straight": border_straight_cover,
        "faded": faded_cover,
    }

    def __init__(self, pictures, frames, step, render):
        """
        :param pictures: [numpy.ndarray, numpy.ndarray]
        :param frames: Integer
        :param step: Integer
        :param render: String
        """
        self.pictures = pictures
        self.frames = frames
        self.step = step
        self.render = render

    def __call__(self, *args, **kwargs):
        """
        以key: value形式将计算方法function存在Render.renders中,凭名称调用对应函数
        """
        function = self.renders.get(self.render, default_cover)
        return function(self.pictures, self.frames, self.step)