import tornado.ioloop
import tornado.web
from lenovotf.web import FileHandler

try:
    from urllib.parse import unquote
except ImportError:
    # Python 2.
    from urllib import unquote


# class MainHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.write("Hello, world")

def make_app():
    return tornado.web.Application([
        (r"/post", FileHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
