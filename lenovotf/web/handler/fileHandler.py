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

FILE_DIR_PREFIX = "/data/tfcodes/upload/"


# FILE_DIR_PREFIX = "f:/test/"


class FileHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

    def post(self):
        for field_name, files in self.request.files.items():
            for info in files:
                filename, content_type = info["filename"], info["content_type"]
                body = info["body"]
                filename = re.sub("\\\\", "/", filename)
                filename = re.split("/", filename)[-1]
                file = FILE_DIR_PREFIX + filename
                logging.info("storing file:%s..." % file)
                if not os.path.exists(FILE_DIR_PREFIX):
                    os.system("mkdir -p %s" % FILE_DIR_PREFIX)
                with open(file, 'wb') as f:
                    f.write(body)
                # print(body)
                logging.info(
                    'POST "%s" "%s" %d bytes', filename, content_type, len(body)
                )
                # to avoid path which contains \ add get pure filename for source codes
                # code_file = re.sub("\\\\", "/")
                # code_file = code_file.split("/")[-1]

        self.write("OK")
