# coding: utf-8
import os
import configparser
import re
import logging

logging.basicConfig(level=logging.INFO)

'''
To read the config file for a distributed tensorflow application and set its path environments params if it uses high level apis.
If low level apis are used, execution params will be returned 
'''


class AppConfiger:

    def __init__(self):
        self.configer = configparser.ConfigParser()

    def parser(self):
        return self.configer

    # set tf path environment if high level apis are used
    def set_tf_config(self, conf_path):
        # path = os.path.split(os.path.realpath(__file__))[0] + '/../conf/config'
        self.configer.read(conf_path)
        api_level = self.configer.get('api', 'level')
        assert (api_level is not None), 'api level is not set in configuration, pls check.'
        if api_level == 0:
            print
            'tensorflow api level: low ...'
        else:
            print
            'tensorflow api level: high ...'
        # install third party dependencies to set up environment
        depens = self.configer.get('dependency', 'require')
        self._install_depens(depens)

        data_input_dir = self.configer.get('path', 'train_input_dir')
        print('train data input path is: %s ' % data_input_dir)
        eval_input_dir = self.configer.get('path', 'eval_input_dir')
        print('eval data input path is: %s ' % eval_input_dir)
        model_dir = self.configer.get('path', 'model_dir')
        print('model path is: %s ' % model_dir)
        source_code_dir = self.configer.get('path', 'source_code_dir')
        print('source code path is: %s ' % source_code_dir)

    def _install_depens(self, depends):
        if depends is not None:
            depends = re.split(',', depends)
            logging.info('ready to install dependencies of your application...')
            for depend in depends:
                # execute install command
                logging.info('your app depends on module, try to install it : %s' % depends)
                os.system('pip install ' + depend)
