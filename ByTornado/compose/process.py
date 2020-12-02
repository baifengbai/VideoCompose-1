"""
@Author: WSWSCSJ
@Description: handle post request and compose video logic
"""
from loguru import logger

from compose.video import Video
from compose.audio import Audio
from compose.picture import Picture
from compose.handler import Handler

class Process:


    def __init__(self, request):
        self.request = request
        self.configures = None
        self.failures = []

    @property
    def run(self):
        """
        清洗和整理 APIView 传入的 request
        """
        try:
            self.configures = Handler(self.request)
        except Exception as e:
            self.failures.append(str(e))
            return False

        c = self.configures
        if not c:
            self.failures.append("handle request failed with empty configures")
            return False
        """
        将 request 的图片二进制流列表转成 picture.Picture 对象存入pictures
        """
        pictures = []
        for _ in c.pictures:
            _ = Picture(_, c.color, c.size)
            if _.picture is not None:
                pictures.append(_.picture)
            else:
                self.failures.extend(_.failures)
                return False
        """
        将 request 的音频二进制流转成 audio.Audio 对象
        根据 request 传递的参数动态设置 audio 和 video 对象
        """
        audio = Audio(audio_stream=c.audio)
        video = Video(picture_set=pictures)

        for key in c.all:
            if key in c.video_attributes:
                setattr(video, key, getattr(c, key))
            if key in c.audio_attributes:
                setattr(audio, key, getattr(c, key))

        succeed = video.produce and video.set_audio(audio.audio_file_clip)
        if not succeed:
            self.failures.extend(video.failures)
        else:
            succeed = video.video_stream
        del video
        del audio
        return succeed

    @property
    def failure(self):
        return "\n".join(self.failures)