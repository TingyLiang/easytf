import tornado.web
import re
from fabric.api import *
import os

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
                filename = re.split("/", filename)[-1]
                cdir = FILE_DIR_PREFIX + re.sub(".tar", "", filename) + "/"
                file = cdir + filename
                logging.info("storing file:%s..." % file)
                os.system("mkdir -p %s" % cdir)
                with open(file, 'wb') as f:
                    f.write(body)
                # print(body)
                logging.info(
                    'POST "%s" "%s" %d bytes', filename, content_type, len(body)
                )

        self.write("OK")
