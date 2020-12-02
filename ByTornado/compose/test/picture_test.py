"""
@Author: WSWSCSJ
@Description: 单例模式将图片二进制流convert为numpy.ndarray
"""

import cv2
import numpy as np
from loguru import logger

from common.constants import Color, Size, VIDEO_PATH

class Picture:
    failures = []

    def __init__(self, content, color=Color.WHITE, size=Size.P720):
        """
        :param color: 填充reshape后图片至目标尺寸的颜色
        """
        self.picture_stream = content
        self.color = color
        self.size = size
        self.picture = self.convert()
        self.picture = self.reshape()

    def __call__(self, *args, **kwargs):
        return self.picture

    @property
    def failure(self):
        if not self.failures:
            return None
        return "\n".join(self.failures)

    def convert(self):
        """
        convert bytes type picture_stream to numpy.ndarray type cv2.image object
        """
        return cv2.imdecode(
            np.frombuffer(self.picture_stream, np.uint8),
            cv2.IMREAD_COLOR
        )

    def reshape(self):
        """
        shape irregular size picture to target size picture
        example: 500 x 500 to 720 x 1280
        Variables:
            Ho: 目标尺寸的高度
            Wt: 目标尺寸的宽度
            Hp: 当前图片的高度
            Wp: 当前图片的宽度
            Ht: 原始比例缩放后目标图片的高度
            short: 缩放后需填充至目标高度的缺口高度
        """
        if not hasattr(self.picture, "shape"):
            self.failures.append("picture format error")
            return None
        Ho = self.size[1]
        Wt = self.size[0]
        Hp = self.picture.shape[0]
        Wp = self.picture.shape[1]
        Ht = int(Hp * Wt / Wp)
        _picture = cv2.resize(
            self.picture, (Wt, Ht),
            interpolation=cv2.INTER_LINEAR
        )
        short = (Ho - Ht) // 2 if (Ho - Ht) % 2 == 0 else (Ho - Ht + 1) // 2
        if short <= 0:
            self.failures.append("picture doesn't fit the size of target video")
            return None
            # raise ValueError("picture doesn't fit the size of target video")
        picture = cv2.copyMakeBorder(
            _picture,
            short, Ho - Ht - short, 0, 0,
            cv2.BORDER_CONSTANT,
            value=self.color
        )
        return picture

if __name__ == "__main__":
    with open(VIDEO_PATH+"test1.JPG", "rb") as _:
        logger.debug(Picture(_.read()).picture.shape)