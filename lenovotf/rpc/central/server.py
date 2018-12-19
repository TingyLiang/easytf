# coding: utf-8
import zerorpc
import logging
import sys
import lenovotf.util.deployHelper as dhelper
import os
import re
import lenovotf.util.confReader as reader

logging.basicConfig(level=logging.INFO)

server = None
gendpoint = None
WEB_SERVER_CODE_DIR = "/data/tfcodes/upload/"


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
        # TODO 根据参数启动各节点训练任务，启动前需要对sy.path进行设置，将打包的依赖添加到应用的path中

    def do_dis_code(self, app_id, cluster):
        '''deprecated,根据appid 和集群信息分发代码'''
        # TODO 对源码进行二次打包
        logging.info("start to distribute codes to nodes...")
        source_dir = '/data/tfcode/%s' % app_id
        target_dir = '/data/tfcode/%s' % app_id
        cmd = "fab -f ../../util/deployHelper.py deploy_code:%s,%s,%s" % (app_id, source_dir, cluster)
        os.system(cmd)
        # dhelper.deploy_code(source_dir=source_dir, cluster=cluster, app_id=app_id)
        logging.info("end to distribute codes to nodes %s..." % cluster)

    def do_disCode(self, filename, cluster):
        '''根据源码文件和集群信息分发代码'''
        # 对源码进行二次打包，这里文件名是用户环境源码文件完整路径，需要进行处理
        filename = re.sub("\\\\", "/", filename)
        # XXX.zip
        filename = re.split("/", filename)[-1]
        logging.info("repackaging codes for file %s...." % filename)
        fullname = reader.get("web", "upload_store_path") + filename
        pkcmd = "python ./repackage.py %s" % fullname
        os.system(pkcmd)

        # {
        #     'cluster': {'chief': ['192.168.11.39:2222'],
        #                 'ps': ['192.168.11.39:2223', '192.168.11.39:2224'],
        #                 'worker': ['192.168.11.39:2224', '192.168.11.39:2225']},
        #     'hosts': [{'host': '192.168.11.39:2222', 'task': {'type': 'chief', 'index': 0}},
        #               {'host': '192.168.11.39:2224', 'task': {'type': 'worker', 'index': 0}},
        #               {'host': '192.168.11.39:2225', 'task': {'type': 'worker', 'index': 1}}]
        # }
        hosts = cluster['hosts']
        host_list = []
        for host in hosts:
            host_list.append(re.split(":", host['host'])[0])
        # self.upload_code(file, cluster)
        logging.info("start to distribute source code：%s to nodes%s" % (fullname, host_list))
        re_packed_name = re.split("\.", fullname)[0] + "_with_dependences.zip"
        cmd = "fab -f ./deployHelper.py deploy_code:%s,%s" % (re_packed_name, cluster)
        os.system(cmd)
        # dhelper.deploy_code(source_dir=source_dir, cluster=cluster, app_id=app_id)
        logging.info("end to distribute codes %s to nodes %s..." % (re_packed_name, host_list))


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
