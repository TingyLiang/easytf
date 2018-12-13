# coding: utf-8
import tensorflow as tf
from lenovotf.client import Client


def run(main=None, argv=None):
    client = Client()
    success = client.new_cluster()
    if success:
        success = client.upload_data_and_code()
    if success:
        success = client.start_train()
    if success:
        tf.app.run(main, argv)
