import tornado.web
import re

import logging

try:
    from urllib.parse import unquote
except ImportError:
    # Python 2.
    from urllib import unquote

logging.basicConfig(level=logging.INFO)

FILE_DIR_PREFIX = "/data/codes/test/"
# FILE_DIR_PREFIX = "f:/test/"


class FileHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

    def post(self):
        for field_name, files in self.request.files.items():
            for info in files:
                filename, content_type = info["filename"], info["content_type"]
                body = info["body"]
                file = FILE_DIR_PREFIX + re.split("/", filename)[-1]
                with open(file, 'wb') as f:
                    f.write(body)
                # print(body)
                logging.info(
                    'POST "%s" "%s" %d bytes', filename, content_type, len(body)
                )

        self.write("OK")
