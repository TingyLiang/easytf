# coding: utf-8
import zerorpc
import logging
import sys
import lenovotf.util.deployHelper as dhelper

logging.basicConfig(level=logging.INFO)

server = None
gendpoint = None


class CentralRPCServer(object):
    """the rpc server run on central"""

    def __init__(self, endpoint):
        super(CentralRPCServer, self).__init__()
        self.endpoint = endpoint

    def do_train(self, app_id, train_params):
        '''start distribute training, include:
         1. start training on every worker/ps/chief nodes
         '''
        logging.info("ready to start training for app: %s" % app_id)
        # TODO 根据参数启动各节点训练任务

    def do_dis_code(self, app_id, cluster):
        logging.info("start to distribute codes to nodes...")
        source_dir = '/data/tfcode/%s' % app_id
        target_dir = '/data/tfcode/%s' % app_id
        dhelper.deploy_code(source_dir, cluster, target_dir)
        logging.info("end to distribute codes to nodes...")

    def _send_code_to(self, app_id, host):
        logging.info("sending code of app, ID: " + str(app_id) + ' to host ' + host)

    def deploy_model(self, app_id):
        logging.info("ready to start deploying model for app: %s" % app_id)
        # TODO 模型上线


def start(endpoint):
    global gendpoint
    global server
    gendpoint = endpoint
    logging.info('starting WorkerRPCServer on ' + endpoint)
    server = zerorpc.Server(CentralRPCServer(endpoint))
    server.bind(endpoint)
    # self.server.bind('tcp://0.0.0.0:4243')
    server.run()


def stop(self):
    logging('stopping WorkerRPCServer on %s' % self.endpoint)
    server.close()
    global gendpoint
    gendpoint = None


if __name__ == '__main__':
    endpoint = 'tcp://0.0.0.0:14243'
    if len(sys.argv) > 1:
        # print(sys.argv[1])
        start(sys.argv[1])
    else:
        start(endpoint)
