# coding: utf-8
from datetime import datetime
from fabric.api import *
import re

# 登录用户和主机名：tf-build
env.user = 'root'
env.password = '123456'
env.hosts = ['172.17.171.108']  # 如果有多个主机，fabric会自动依次部署


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
    env.hosts = cluster
    '''deploy tf code from server to cluster
    Args:
        source_dir: the source code dir
        cluster:a list of the hosts to send code to
        target_dir: target code dir to save code on each node
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
