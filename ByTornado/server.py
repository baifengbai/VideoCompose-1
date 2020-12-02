import tornado.ioloop
import tornado.web
from tornado.web import MissingArgumentError

from loguru import logger

from compose.process import Process
from compose.handler import Handler

class VideoComposeHandler(tornado.web.RequestHandler):

    def get_argument_no_error(self, key):
        try:
            result = self.get_body_argument(key)
        except MissingArgumentError:
            return None
        except Exception as e:
            logger.error(e)
            return None
        else:
            return result

    def post(self):
        process = Process(self)
        video_stream = process.run
        if not video_stream:
            logger.error(process.failure)
        self.set_header('Content-Type', 'video/mp4')
        self.set_header('Content-Disposition', 'attachment; filename=video.mp4')
        self.write(video_stream)
        self.finish()

def make_app():
    return tornado.web.Application([
        (r"/api/video/", VideoComposeHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8989)
    tornado.ioloop.IOLoop.current().start()