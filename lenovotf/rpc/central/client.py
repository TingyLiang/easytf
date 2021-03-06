# coding: utf-8
import zerorpc
import logging

logging.basicConfig(level=logging.INFO)


class CentralRPCClient:
    """the rpc client to connect server run on central"""

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

    def train(self, app_id, train_params):
        self.client.do_train(app_id, train_params)

    def distribute_code(self, app_id, cluster):
        logging.info("asking server to distribute code of %s to workers:%s ..." % (app_id, cluster))
        file = "F:\\PythonWorkspace\\tf-package-demo\\tf-estimator-cluster-app.zip"
        self.client.do_disCode(file, cluster)

    def dis_code(self, file, cluster):
        logging.info("asking server to distribute code of %s to workers:%s ..." % (file, cluster))
        self.client.do_disCode(file, cluster)


if __name__ == '__main__':
    endpoint = 'tcp://172.17.171.108:14243'
    # endpoint = 'tcp://0.0.0.0:4243'
    # endpoint = 'tcp://10.244.0.1:4243'
    # endpoint = 'tcp://127.0.0.1:4243'
    client = CentralRPCClient(endpoint)
    client.start()
    file = "tf-estimator-cluster-app.zip"
    client.dis_code(file, ['172.17.171.190'])
    # # client.rain(123, {})
    # client.distribute_code("ac0534fe-fd23-11e8-8ec9-309c23c29f89", ['172.17.171.190'])
    # client.stop()
