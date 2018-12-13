# coding: utf-8
import tensorflow as tf
from lenovotf.client import Client
import os
import tensorflow.estimator as es
import logging

logging.basicConfig(level=logging.INFO)


def train_and_evaluate(estimator, train_spec, eval_spec):
    mode = int(os.environ['RUN_MODE'])

    # 此处如果在工作节点上执行，则直接屏蔽生成资源等操作，直接进入训练流程
    if mode == 0:
        tf.estimator.train_and_evaluate(estimator, train_spec, eval_spec)
    else:
        client = Client()
        client.start()
        # 此处可能存在同步等待的问题
        success = client.new_cluster()
        if success:
            success = client.upload_data_and_code()
        if success:
            success = client.start_train()
        # if success:
        # tf.estimator.train_and_evaluate(estimator, train_spec, eval_spec)
        # TODO
        client.close()


# train_success: bool = True


def train(estimator, train_input_fn):
    mode = os.environ['RUN_MODE']
    if mode == 0:
        estimator.train(train_input_fn)
    else:
        client = Client()
        success = client.new_cluster()
        if success:
            success = client.upload_data_and_code()
        if success:
            success = client.start_train()
            estimator.train(train_input_fn)

    # global train_success
    # train_success = success


def evaluate(estimator, eval_input_fn):
    estimator.evaluate(eval_input_fn)


_USE_DEFAULT = object()


class RunConfig(object):
    def __init__(self,
                 model_dir=None,
                 tf_random_seed=None,
                 save_summary_steps=100,
                 save_checkpoints_steps=_USE_DEFAULT,
                 save_checkpoints_secs=_USE_DEFAULT,
                 session_config=None,
                 keep_checkpoint_max=5,
                 keep_checkpoint_every_n_hours=10000,
                 log_step_count_steps=100,
                 train_distribute=None,
                 device_fn=None,
                 protocol=None,
                 eval_distribute=None,
                 experimental_distribute=None):
        self.config = es.RunConfig(model_dir, tf_random_seed, save_summary_steps, save_checkpoints_steps,
                                   save_checkpoints_secs, session_config, keep_checkpoint_max,
                                   keep_checkpoint_every_n_hours, log_step_count_steps, train_distribute, device_fn,
                                   protocol, eval_distribute, experimental_distribute)
