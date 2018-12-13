# coding: utf-8
import zerorpc
import logging

logging.basicConfig(level=logging.INFO)

class WorkerRPCServer(object):
    """the rpc server run on workers"""

    def __init__(self, endpoint):
        super(WorkerRPCServer, self).__init__()
        self.server = None
        self.endpoint = endpoint

    def start_train(self, app_id, params):
        '''start training on a worker/ps/chief node'''
        # TODO 根据参数启动节点上的训练任务
        logging.info("ready to start training for app: %s" % app_id)

    def start(self):
        logging('starting WorkerRPCServer on %s' % self.endpoint)
        self.server = zerorpc.Server(WorkerRPCServer())
        self.server.bind(self.endpoint)
        # self.server.bind('tcp://0.0.0.0:4243')
        self.server.run()

    def stop(self):
        logging('stopping WorkerRPCServer on %s' % self.endpoint)
        self.server.close()
