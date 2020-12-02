"""
@Author: WSWSCSJ
video frames = picture1 * npf + render pictures1->2(len: frames)
               + picture2 * npf + render pictures2->3(len: frames)
               ...
               + render picturesn-1->n(len: frames) + picturen * npf
"""

import cv2
from uuid import uuid1
import os
from sys import stdout
from moviepy.editor import VideoFileClip, AudioFileClip
from loguru import logger

from compose.render import Render
from common.constants import *

class Video:

    @staticmethod
    def create_file_name(video_format):
        _uuid = uuid1()
        name = VIDEO_PATH + str(_uuid).replace("-", "_") + "_video." + video_format
        return name

    def __init__(
            self, picture_set, fps=25, frames=20, step=1, length=14,
            size=Size.size, video_format="MP4", render="default"
    ):
        """
        :param picture_set: [numpy.ndarray * N]
        :param fps:
        :param frames: number of rendered pictures
        :param step:
        :param length: length of composite video
        :param size: tuple (720, 1280)
        :param video_format:
        :param render: render function
        """
        self.picture_set = picture_set
        self.fps = fps
        self.frames = frames
        self.step = step
        self.length = length
        self.size = size
        self.video_format = video_format
        self.render = render
        self.file_name = self.create_file_name(video_format)
        self.composite_file_name = self.file_name.replace("_video.", "_composite_video.")
        self.video_stream = self.video_file_clip = None
        self.failures = []

    @property
    def file_exists(self):
        return os.path.exists(self.file_name)

    @property
    def composite_file_exists(self):
        return os.path.exists(self.composite_file_name)

    @property
    def delete(self):
        """
        files should exists before self.delete
        :return: bool
        """
        succeed = True
        if not self.file_exists:
            succeed = False
            self.failures.append("delete video file error: file not exists")
        else:
            os.remove(self.file_name)
        if not self.composite_file_exists:
            succeed = False
            self.failures.append("delete composite video file error: file not exists")
        else:
            os.remove(self.composite_file_name)
        return succeed

    @property
    def failure(self):
        if not self.failures:
            return None
        return "\n".join(self.failures)

    def set_audio(self, audio_file_clip):
        """
        :param audio_file_clip: Audio.audio_file_clip
        :return: bool
        """
        if not self.video_file_clip:
            self.failures.append("empty video file clip")
            return False
        if not isinstance(audio_file_clip, AudioFileClip):
            self.failures.append("audio file clip type error with '{type}'".format(type=type(audio_file_clip)))
            return False
        self.video_file_clip.audio = audio_file_clip
        self.video_file_clip.write_videofile(self.composite_file_name, audio_codec="aac")
        audio_file_clip.close()
        self.video_file_clip.close()
        if not self.composite_file_exists:
            self.failures.append("composite video not exists")
            return False
        with open(self.composite_file_name, "rb") as _:
            self.video_stream = _.read()
        return True

    def render_pictures(self, picture1, picture2):
        _Render = Render(
            pictures=[picture1, picture2],
            frames=self.frames,
            step=self.step,
            render=self.render
        )
        try:
            pictures = _Render()
        except Exception as e:
            self.failures.append(str(e))
            return None
        else:
            return pictures

    @property
    def produce(self):
        four_cc = cv2.VideoWriter_fourcc(*"MJPG")
        total_frames = self.fps * self.length
        npf = (total_frames - self.frames * (len(self.picture_set) - 1)) // len(self.picture_set)
        video = cv2.VideoWriter(self.file_name, four_cc, self.fps, self.size)
        for _ in range(len(self.picture_set) - 1):
            for n in range(npf):
                video.write(self.picture_set[_])
            rendered_pictures = self.render_pictures(self.picture_set[_], self.picture_set[_+1])
            if not rendered_pictures:
                return False
            for p in rendered_pictures:
                video.write(p)
        for n in range(npf):
            video.write(self.picture_set[-1])
        video.release()
        if not self.file_exists:
            self.failures.append("release fail")
            return False
        self.video_file_clip = VideoFileClip(self.file_name)
        return True

    def __del__(self):
        # logger.info(
        #     "delete video {id} files {mark} in {dir}\n".format(
        #         id=id(self), mark="succeed" if self.delete else "failed", dir=VIDEO_PATH)
        # )
        stdout.write(
            "delete video {id} files {mark} in {dir}\n".format(
                id=id(self), mark="succeed" if self.delete else "failed", dir=VIDEO_PATH)
        )