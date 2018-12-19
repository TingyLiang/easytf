"""Usage: python httpHelper.py [--put] file1.txt file2.png ...
Demonstrates uploading files to a server, without concurrency. It can either
POST a multipart-form-encoded request containing one or more files, or PUT a
single file without encoding.
See also file_receiver.py in this directory, a server that receives uploads.
"""

import mimetypes
import os
import sys
from functools import partial
from uuid import uuid4
import lenovotf.util.AppConfiger as configer

try:
    from urllib.parse import quote
except ImportError:
    # Python 2.
    from urllib import quote

from tornado import gen, httpclient, ioloop
from tornado.options import define, options
import logging

logging.basicConfig(level=logging.INFO)
import lenovotf.util.confReader as reader

SERVER_URL = reader.get_web_server_url()


# SERVER_URL = "http://localhost:8888"


# Using HTTP POST, upload one or more files in a single multipart-form-encoded
# request.
@gen.coroutine
def multipart_producer(boundary, filenames, write):
    boundary_bytes = boundary.encode()
    for filename in filenames:
        filename_bytes = filename.encode()
        mtype = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        buf = (
                (b"--%s\r\n" % boundary_bytes)
                + (
                        b'Content-Disposition: form-data; name="%s"; filename="%s"\r\n'
                        % (filename_bytes, filename_bytes)
                )
                + (b"Content-Type: %s\r\n" % mtype.encode())
                + b"\r\n"
        )
        yield write(buf)
        with open(filename, "rb") as f:
            while True:
                # 16k at a time.
                chunk = f.read(16 * 1024)
                if not chunk:
                    break
                yield write(chunk)

        yield write(b"\r\n")

    yield write(b"--%s--\r\n" % (boundary_bytes,))


# Using HTTP PUT, upload one raw file. This is preferred for large files since
# the server can stream the data instead of buffering it entirely in memory.
@gen.coroutine
def post(filenames, server_url):
    client = httpclient.AsyncHTTPClient()
    boundary = uuid4().hex
    headers = {"Content-Type": "multipart/form-data; boundary=%s" % boundary}
    producer = partial(multipart_producer, boundary, filenames)
    response = yield client.fetch(
        server_url + "/post",
        method="POST",
        headers=headers,
        body_producer=producer,
    )

    logging.info(response)


@gen.coroutine
def raw_producer(filename, write):
    with open(filename, "rb") as f:
        while True:
            # 16K at a time.
            chunk = f.read(16 * 1024)
            if not chunk:
                # Complete.
                break

            yield write(chunk)


@gen.coroutine
def put(filenames, server_url):
    client = httpclient.AsyncHTTPClient()
    for filename in filenames:
        mtype = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        headers = {"Content-Type": mtype}
        producer = partial(raw_producer, filename)
        # "http://localhost:8888/%s"
        url_path = quote(os.path.basename(filename))
        response = yield client.fetch(
            server_url + url_path,
            method="PUT",
            headers=headers,
            body_producer=producer,
        )
        print(response)


def upload_file(filenames):
    define("put", type=bool, help="Use PUT instead of POST", group="file uploader")
    # Tornado configures logging from command line opts and returns remaining args.
    # filenames = ['F:/PythonWorkspace/easytf/util/utils.tar.gz']
    if not filenames:
        print("Provide a list of filenames to upload.", file=sys.stderr)
        sys.exit(1)
    # method = put if options.put else post
    method = post
    print(SERVER_URL)
    ioloop.IOLoop.current().run_sync(lambda: method(filenames, SERVER_URL))


def deploy_to_cluster(cluster):
    pass


if __name__ == "__main__":
    define("put", type=bool, help="Use PUT instead of POST", group="file uploader")

    # Tornado configures logging from command line opts and returns remaining args.
    filenames = options.parse_command_line()
    # filenames = ['F:/PythonWorkspace/easytf/test/fab_test.py']
    filenames = ['F:/PythonWorkspace/tf-package-demo/tf_dis/e820066e-fd0d-11e8-85a6-309c23c29f89.tar']
    if not filenames:
        print("Provide a list of filenames to upload.", file=sys.stderr)
        sys.exit(1)

    # method = put if options.put else post
    method = post
    server_url = "http://172.171.17.108:8080"
    logging.info("starting tornado web client at:%s" % server_url)
    ioloop.IOLoop.current().run_sync(lambda: method(filenames, server_url))
