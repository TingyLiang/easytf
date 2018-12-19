# coding: utf-8
import logging
import os
import uuid
import sys
import platform
import re

import lenovotf.rpc.central.client as cClient
import lenovotf.util.httpHelper as fuploader
import lenovotf.util.packagedepends as packagedepends
import configparser
import lenovotf.util.confReader as reader

'''the API client who connect API Server to execute commands from driver, include:
1. create a new cluster for user
2. upload train and evaluate data and user code 
3. execute training 
4. fetch logs for training 
5. upload model and provide service 
'''
logging.basicConfig(level=logging.INFO)  # 设置日志级别

CRNTRAL_ENDPOINT = reader.get_rpc_server_url()
GLOABLE_CONFIG_PATH = None


class Client:
    def __init__(self):
        self.cRpcClient = cClient.CentralRPCClient(CRNTRAL_ENDPOINT)
        self._app_id = str(uuid.uuid1())
        # self.cRpcClient.start()
        self.cluster = None

    def new_cluster(self):
        logging.info('preparing to get cluster resources from server...')
        # request = json.dump({})
        request = {}
        data = self.do_request(request)
        # TODO 解析集群信息
        # cluster = data
        logging.info('cluster info:' + str(data))
        self.cluster = {
            'cluster': {'chief': ['192.168.11.39:2222'],
                        'ps': ['192.168.11.39:2223', '192.168.11.39:2224'],
                        'worker': ['192.168.11.39:2224', '192.168.11.39:2225']},
            'hosts': [{'host': '192.168.11.39:2222', 'task': {'type': 'chief', 'index': 0}},
                      {'host': '192.168.11.39:2224', 'task': {'type': 'worker', 'index': 0}},
                      {'host': '192.168.11.39:2225', 'task': {'type': 'worker', 'index': 1}}]
        }
        return True

    def do_request(self, request):
        # data = json.dump({})
        data = {}
        return data

    def upload_data_and_code(self, entrance_class=sys.argv[0]):
        cdir = os.path.abspath(".")
        # 指定tf启动类作为参数
        installed = reader.get_pre_installed_depends()
        file = "F:\\PythonWorkspace\\tf-package-demo\\tf-estimator-cluster-app.zip"
        # file = packagedepends.package(entrance_class, excludes=installed)
        self.upload_data()
        self.upload_code(file)
        # self.cRpcClient.dis_code(file, self.cluster)
        return True

    def upload_data(self):
        logging.info('preparing to upload data...')
        # TODO  压缩数据,并上传到用户目录
        return True

    def upload_code(self, code_file, cluster):
        # 用户源码上传至服务器,服务端接口代码完成后进行部署
        logging.info('preparing to uploading code...')
        fuploader.upload_file([code_file])
        # self.cRpcClient.distribute_code(self._app_id, cluster)
        self.cRpcClient.dis_code(code_file, cluster)
        return True

    def start_train(self):
        logging.info('preparing to start training...')
        c = {
            'cluster': {'chief': ['localhost:2222'],
                        'ps': ['localhost:2223', 'localhost:2224'],
                        'worker': ['localhost:2224', 'localhost:2225']},
            'hosts': [{'host': 'localhost:2222', 'task': {'type': 'worker', 'index': 0}},
                      {'host': 'localhost:2224', 'task': {'type': 'worker', 'index': 1}}]
        }
        self.cRpcClient.train(sys.argv[0])
        # TODO 启动各节点训练脚本，开始训练
        return True

    def deploy_model(self):
        logging.info('preparing to deploy model...')
        # TODO 部署模型至服务器，启动模型服务
        return True

    def start(self):
        self.cRpcClient.start()

    def close(self):
        self.cRpcClient.stop()

    @property
    def app_id(self):
        return self._app_id


def _init_global_conf_path():
    abspath = os.path.abspath(__file__)
    ost = platform.system()
    # if ost == "Windows":

    # elif ost == "Linux":
    # else:
