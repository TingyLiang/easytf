# coding: utf-8
import zerorpc
import logging

logging.basicConfig(level=logging.INFO)


class WorkerRPCClient:
    """the rpc client to connect server which run on workers"""

    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.client = None

    def start(self):
        logging.info('starting a rpc client to server: %s' % self.endpoint)
        self.client = zerorpc.Client()
        self.client.connect(self.endpoint)
        # c.connect('tcp://127.0.0.1:4243')

    def stop(self):
        logging.info('stopping a rpc client to server: %s' % self.endpoint)
        self.client.close()


if __name__ == '__main__':
    client = WorkerRPCClient('tcp://127.0.0.1:4243')
    client.start()


