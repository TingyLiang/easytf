import tornado.web
import logging

logging.basicConfig(level=logging.INFO)


class ClusterHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        body = self.request["body"]
        print(body)
