"""
@Author: WSWSCSJ
@Description: 替换target VideoFileClip audio attribute 为 target AudioFileClip
"""

import os
from sys import stdout
from uuid import uuid1
from moviepy.editor import AudioFileClip
from loguru import logger

from common.constants import *

class Audio:
    audio_stream = None
    failures = []

    @staticmethod
    def create_file_name(audio_format):
        _uuid = uuid1()
        name = AUDIO_PATH + str(_uuid).replace("-", "_") + "_audio." + audio_format
        return name

    def __init__(self, audio_stream, start=0, end=14, audio_format="mp3"):
        """
        :param audio_stream: Bytes Stream
        :param start: audio start point
        :param end: audio end point
        :param audio_format:
        """
        self.audio_stream = audio_stream
        self.start = start
        self.end = end
        self.audio_format = audio_format
        self.file_name = self.create_file_name(audio_format)

    @property
    def file_exists(self):
        return os.path.exists(self.file_name)

    @property
    def delete(self):
        """
        file should exists before self.delete
        :return: bool
        """
        succeed = True
        if not self.file_exists:
            succeed = False
            self.failures.append("delete audio file error: file not exists")
        else:
            os.remove(self.file_name)
        return succeed

    @property
    def audio_file_clip(self):
        if not self.file_exists:
            with open(self.file_name, "wb") as _:
                _.write(self.audio_stream)
        clip = AudioFileClip(self.file_name).subclip(self.start, self.end)
        return clip

    @property
    def failure(self):
        if not self.failures:
            return None
        return "\n".join(self.failures)

    def __del__(self):
        # logger.info(
        #     "\ndel audio {id} file {mark}\n".format(
        #         id=id(self), mark="succeed" if self.delete else "failed")
        # )
        stdout.write(
            "\ndel audio {id} file {mark}\n".format(
                id=id(self), mark="succeed" if self.delete else "failed")
        )

if __name__ == "__main__":
    with open(VIDEO_PATH+"starboy.mp3", "rb") as _:
        audio = Audio(_.read())
        logger.debug(type(audio.audio_file_clip))
        del audio