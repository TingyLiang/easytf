# coding: utf-8
import logging
import os
import uuid

import lenovotf.rpc.central.client as cClient
import lenovotf.util.fileUploader as fuploader
import lenovotf.util.zipHelper as zipHelper

'''the API client who connect API Server to execute commands from driver, include:
1. create a new cluster for user
2. upload train and evaluate data and user code 
3. execute training 
4. fetch logs for training 
5. upload model and provide service 
'''
logging.basicConfig(level=logging.INFO)  # 设置日志级别

# TODO 此处应该读取配置文件，暂时硬编码
CRNTRAL_ENDPOINT = "tcp://171.17.17.108:14243"


class Client:
    def __init__(self):
        self.cRpcClient = cClient.CentralRPCClient(CRNTRAL_ENDPOINT)
        self._app_id = str(uuid.uuid1())
        self.cluster = None

    def new_cluster(self):
        logging.info('preparing to get cluster resources from server...')
        # request = json.dump({})
        request = {}
        data = self.do_request(request)
        # TODO 解析集群信息
        # cluster = data
        logging.info('cluster info:' + str(data))
        return True

    def do_request(self, request):
        # data = json.dump({})
        data = {}
        return data

    def upload_data_and_code(self):
        pardir = os.path.abspath(".")
        file = zipHelper.zip('.', str(self._app_id))
        self.upload_data()
        self.upload_code(pardir + "/" + file)
        return True

    def upload_data(self):
        logging.info('preparing to upload data...')
        # TODO  压缩数据,并上传到用户目录
        return True

    def upload_code(self, code_file):
        # 用户源码上传至服务器
        logging.info('preparing to uploading code...')
        fuploader.upload_file([code_file])
        # TODO  通过服务器分发代码
        self.cluster = ["172.17.171.190"]
        self.cRpcClient.distribute_code(self._app_id, self.cluster)
        return True

    def start_train(self):
        logging.info('preparing to start training...')
        self.cRpcClient.do_train(app_id=self._app_id, train_params={})
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

    @app_id.setter
    def app_id(self, app_id):
        self._app_id = app_id
