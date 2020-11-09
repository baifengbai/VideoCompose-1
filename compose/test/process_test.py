"""
TDD
@Author: WSWSCSJ
"""
from compose.video import Video
from compose.audio import Audio
from compose.picture import Picture
from common.constants import *

from loguru import logger

class ProcessTest:
    failures = []

    def __init__(self, request):
        self.request = request

    @property
    def run(self):
        video_attributes = (
            "fps", "frames", "step", "length",
            "size", "video_format", "render"
        )
        audio_attributes = (
            "start", "end", "audio_format"
        )

        pictures_stream = []
        with open("/Users/chenxuejun/Downloads/test1.JPG", "rb") as _:
            pictures_stream.append(_.read())
        with open("/Users/chenxuejun/Downloads/test2.JPG", "rb") as _:
            pictures_stream.append(_.read())
        with open("/Users/chenxuejun/Downloads/test3.JPG", "rb") as _:
            pictures_stream.append(_.read())
        with open("/Users/chenxuejun/Downloads/starboy.mp3", "rb") as _:
            audio = _.read()
        size = Size.size
        color = Color.WHITE

        pictures = []
        for _ in pictures_stream:
            _ = Picture(_, color, size).picture
            if _ is not None:
                pictures.append(_)
            else:
                self.failures.extend(_.failures)
                return False
        for p in pictures:
            logger.debug(p.shape)
        audio = Audio(audio_stream=audio)
        video = Video(picture_set=pictures)
        succeed = video.produce and video.set_audio(audio.audio_file_clip)
        if not succeed:
            self.failures.extend(video.failures)
        else:
            succeed = video.video_stream
            logger.debug("file {}".format(video.composite_file_name))
        # del video
        # del audio
        if self.failures:
            logger.error(self.failure)
        return succeed

    @property
    def failure(self):
        return "\n".join(self.failures)

if __name__ == "__main__":
    logger.debug(type(ProcessTest("").run))