# coding: utf-8
from datetime import datetime
from fabric.api import *
import re
import logging

logging.basicConfig(level=logging.INFO)

# 登录用户和主机名：tf-build
env.user = 'root'
env.password = '123456'
env.hosts = ['172.17.171.190']  # 如果有多个主机，fabric会自动依次部署


# def pack():
#     ' 定义一个pack任务 '
#     # 打一个tar包：
#     tar_files = ['*.py', 'static/*', 'templates/*', 'favicon.ico']
#     local('rm -f example.tar.gz')
#     local('tar -czvf example.tar.gz --exclude=\'*.tar.gz\' --exclude=\'fabfile.py\' %s' % ' '.join(tar_files))


def deploy():
    ' 定义一个部署任务 '
    # 远程服务器的临时文件：
    remote_tmp_tar = '/tmp/example.tar.gz'
    tag = datetime.now().strftime('%y.%m.%d_%H.%M.%S')
    run('rm -f %s' % remote_tmp_tar)
    # 上传tar文件至远程服务器：
    put('shici.tar.gz', remote_tmp_tar)
    # 解压：
    remote_dist_dir = '/srv/www.example.com@%s' % tag
    remote_dist_link = '/srv/www.example.com'
    run('mkdir %s' % remote_dist_dir)
    with cd(remote_dist_dir):
        run('tar -xzvf %s' % remote_tmp_tar)
    # 设定新目录的www-data权限:
    run('chown -R www-data:www-data %s' % remote_dist_dir)
    # 删除旧的软链接：
    run('rm -f %s' % remote_dist_link)
    # 创建新的软链接指向新部署的目录：
    run('ln -s %s %s' % (remote_dist_dir, remote_dist_link))
    run('chown -R www-data:www-data %s' % remote_dist_link)
    # 重启服务：
    fcgi = '/etc/init.d/py-fastcgi'
    with settings(warn_only=True):
        run('%s stop' % fcgi)
    run('%s start' % fcgi)


def deploy_model():
    # TODO '模型部署上线'
    # 远程服务器的临时文件：
    remote_tmp_tar = '/tmp/example.tar.gz'
    tag = datetime.now().strftime('%y.%m.%d_%H.%M.%S')
    run('rm -f %s' % remote_tmp_tar)
    # 上传tar文件至远程服务器：
    put('shici.tar.gz', remote_tmp_tar)
    # 解压：
    remote_dist_dir = '/srv/www.example.com@%s' % tag
    remote_dist_link = '/srv/www.example.com'
    run('mkdir %s' % remote_dist_dir)
    with cd(remote_dist_dir):
        run('tar -xzvf %s' % remote_tmp_tar)
    # 设定新目录的www-data权限:
    run('chown -R www-data:www-data %s' % remote_dist_dir)
    # 删除旧的软链接：
    run('rm -f %s' % remote_dist_link)
    # 创建新的软链接指向新部署的目录：
    run('ln -s %s %s' % (remote_dist_dir, remote_dist_link))
    run('chown -R www-data:www-data %s' % remote_dist_link)
    # 重启服务：
    fcgi = '/etc/init.d/py-fastcgi'
    with settings(warn_only=True):
        run('%s stop' % fcgi)
    run('%s start' % fcgi)


def deploy_code(app_id, source_dir, cluster):
    # env.hosts = cluster
    '''deploy tf code from server to cluster
    Args:
        source_dir: the source code dir
        cluster:a list of the hosts to send code to
    '''
    remote_tmp_dir = '/tmp/codes/%s' % str(app_id)
    tag = datetime.now().strftime('%y.%m.%d_%H.%M.%S')
    run('rm -rf %s' % remote_tmp_dir)
    # put file to remote server
    run('mkdir -p %s' % remote_tmp_dir)
    put(source_dir, remote_tmp_dir)
    target_dir = '/data/codes/%s' % str(app_id)
    run('mkdir -p %s' % target_dir)
    run('chmod 722 -R %s' % target_dir)
    # print('target dir: %s' + '/%s' % (remote_tmp_dir, file))
    with cd(target_dir):
        run('tar -xzvf %s/%s' % (remote_tmp_dir, re.split('/', source_dir)[-1]))


def deploy_code(file, cluster):
    # env.hosts = cluster
    '''deploy tf code from server to cluster
    Args:
        file: the source code dir
        cluster:a list of the hosts to send code to
    '''
    remote_tmp_dir = '/tmp/codes/'
    tag = datetime.now().strftime('%y.%m.%d_%H.%M.%S')
    # run('rm -rf %s' % remote_tmp_dir)
    # put file to remote server
    name = file.split("/")[-1].split(".")[0]
    run("rm -f %s%s" % (remote_tmp_dir, name + ".zip"))
    run('mkdir -p %s' % remote_tmp_dir)
    logging.info("start to deploy code by fabric:")
    try:
        put(file, remote_tmp_dir)
    except ValueError as e:
        raise e
    except FileNotFoundError as e:
        raise e
    target_dir = '/data/codes/%s' % name
    run("rm -rf %s" % target_dir)
    run('mkdir -p %s' % target_dir)
    # run('chmod 722 -R %s' % target_dir)
    # print('target dir: %s' + '/%s' % (remote_tmp_dir, file)
    cluster = {
        'cluster': {'chief': ['192.168.11.39:2222'],
                    'ps': ['192.168.11.39:2223', '192.168.11.39:2224'],
                    'worker': ['192.168.11.39:2224', '192.168.11.39:2225']},
        'hosts': [{'host': '192.168.11.39:2222', 'task': {'type': 'chief', 'index': 0}},
                  {'host': '192.168.11.39:2224', 'task': {'type': 'worker', 'index': 0}},
                  {'host': '192.168.11.39:2225', 'task': {'type': 'worker', 'index': 1}}]
    }
    with cd(target_dir):
        run('unzip -q %s%s' % (remote_tmp_dir, name + ".zip"))
        # TODO 启动训练过程


        # cmd = "python  -w 127.0.0.1:2223,127.0.0.1:2224 " \
        #       "-c 127.0.0.1:2225 -t worker " \
        #       "-i 0 -m tf_dis/tf-estimator-cluster-app.py " \
        #       " -l /data/codes/tf-estimator-cluster-app_with_dependences/vendors/lib/python3.6/site-packages" %()
        import platform
        pyv = "2.7" if platform.python_version().startswith("2.7") else "3.6"
        pwd = run("pwd")
        logging.info("======current dir is " + pwd)
        path = "%s/vendors/lib/python3.6/site-packages" % pwd
        # 获取主类路径
        main_path = run("find  -name %s.py" % name)
        main_path = pwd + re.sub("\.", "", main_path, 1)
        main = "tf_dis/tf-estimator-cluster-app.py "
        import socket
        for host in cluster["hosts"]:
            if socket.gethostbyname(socket.gethostname()) == re.split(":", host['host'])[0]:
                logging.info("start training on host %s" % host['host'])
                cmd = "python  -w %s " \
                      "-c %s -t %s " \
                      "-i %s -m %s " \
                      " -l %s" % (
                          ",".join(cluster["cluster"]["worker"]), ",".join(cluster["cluster"]["chief"]),
                          ",".join(host["task"]["type"]), ",".join(host["task"]["index"]), main, path)
                logging.info("start training by executing cmd: %s" % cmd)
                run(cmd)
