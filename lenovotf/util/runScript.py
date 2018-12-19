from optparse import OptionParser
import lenovotf.util.confReader as reader
import os
import json
import re
import sys
import logging

'''the script to run a tensorflow script'''
parser = OptionParser(usage="%prog [options]")
parser.add_option("-p", "--ps", action="store", type="string", dest="ps",
                  help="comma separated ps server list to run the training")
parser.add_option("-w", "--worker", action="store", type="string", dest="worker",
                  help="comma separated worker list to run the training")
parser.add_option("-c", "--chief", action="store", type="string", dest="chief",
                  help="chief worker to run the training")

parser.add_option("-t", "--task_type", action="store", type="string", dest="task_type",
                  help=" type of the current task such as worker, chief, ps etc.")
parser.add_option("-i", "--index", action="store", type="string", dest="index",
                  help="index of the current task")
parser.add_option("-m", "--main", action="store", type="string", dest="main_script",
                  help="entrance class of tensorflow app")
parser.add_option("-l", "--lib", action="store", type="string", dest="lib",
                  help="path of dependency")

if __name__ == '__main__':
    (options, args) = parser.parse_args()
    # api_level = reader.get("api", "level")
    api_level = "1"
    if api_level == "0":
        pass
    elif api_level == "1":
        cluster = {}
        task = {}
        if options.ps:
            cluster["ps"] = re.split(",", options.ps)
        if options.worker:
            cluster["worker"] = re.split(",", options.worker)
        if options.chief:
            cluster["chief"] = re.split(",", options.chief)
        if options.task_type and options.index:
            # 'task': {'type': 'worker', 'index': 1}
            task["type"] = options.task_type
            task["index"] = int(options.index)

        os.environ["TF_CONFIG"] = json.dumps({
            'cluster': cluster,
            'task': task
        })

        os.environ["RUN_MODE"] = "0"
        # print(os.path.abspath(__file__))
        # 安装依赖,并运行脚本
        # sys.path.append()
        if options.lib:
            sys.path.append(options.lib)
        else:
            logging.error("pls specify the lib path of dependency of this app...")
            sys.exit(-1)
        if options.main_script:
            # cmd = "python " + "../../tf_dis/tf-estimator-cluster-app.py"
            cmd = "python " + options.main_script
            os.system(cmd)
        else:
            logging.error("no main script specified for the app, pls check")
            sys.exit(-1)
    else:
        raise ValueError("unknown tensorflow api level config, pls check it again")
