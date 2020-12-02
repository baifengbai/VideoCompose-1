from django.http.response import FileResponse
from io import BytesIO

from compose.process import Process
from common.permission import *
from common.responses import *
from compose.handler import Handler

# Create your views here.

class VideoCompose(APIView):
    permission_classes = (NullPermission, )

    def post(self, request):
        process = Process(request)
        video_stream = process.run
        if video_stream:
            video = BytesIO(video_stream)
            return FileResponse(video, filename="video.mp4", as_attachment=True)
        return MESSAGE_RESPONSE(process.failure)

class TestRequest(APIView):
    permission_classes = (NullPermission, )

    def post(self, request):
        pictures = request.FILES.getlist("pictures")
        audio = request.FILES.getlist("audio")
        for pic in pictures:
            logger.debug(pic)
        logger.debug(type(pictures[0].read()))
        logger.debug(audio[0])
        logger.debug(request.data)
        return SUCCESS_RESPONSE()

class TestConnection(APIView):
    permission_classes = (NullPermission, )

    def get(self, request):
        logger.debug(request.path)
        return SUCCESS_RESPONSE()

    def post(self, request):
        configures = Handler(request)
        for key in configures.all:
            if key in configures.media_keys:
                continue
            logger.debug("{} >>> {}".format(key, getattr(configures, key)))
        return SUCCESS_RESPONSE()

class TestFileResponse(APIView):
    permission_classes = (NullPermission, )

    def get(self, request):
        file = open("/Users/chenxuejun/Downloads/test.MP4", "rb")
        file = BytesIO(file.read())
        response = FileResponse(file, filename="video.mp4", as_attachment=True)
        return response