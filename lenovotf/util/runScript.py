from fabric.api import *
import logging
import os
import json

logging.basicConfig(level=logging.INFO)
'''
the util to run a tensorflow script on cluster nodes
'''


def run_tf_script(script, api_level, params):
    cluster = params["cluster"]
    task_type = params["task_type"]
    task_index = params["task_index"]
    if api_level is not None:
        if api_level == 0:
            # low level api
            #
            cmd = ""
            local(cmd)
        elif api_level == 1:
            # high level api
            strategy = params["strategy"]
            if strategy == 0:
                # mirroredStrategy . no os.environ settings needed
                pass
            elif strategy == 1:
                # collectiveAllReduceStrategy, os.environ settings are needed
                os.environ['TF_CONFIG'] = json.dumps(
                    {'cluster': cluster,
                     'task': {'type': task_type, 'index': task_index}
                     })
            elif strategy == 2:
                # ps server strategy, pass it now
                # TODO: to support ps strategy when using high level api
                pass
            else:
                logging.error("unsupported distribute strategy used,pls check again. ")
            cmd = "python " + script
            local(cmd)
        else:
            logging.error("unknown api level %s for tensorflow" % api_level)

    else:
        logging.error("tensorflow api level has not been specified.")
