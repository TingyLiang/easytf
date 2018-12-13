# coding: utf-8
from fabric.api import local
import os
import shutil

DEFAULT_UNZIP_DIR = 'F:/test'


def list():
    local('ls -l')


def zip(path, filename):
    # path = 'F:/PythonWorkspace/easytf/util'
    files = os.listdir(path)
    files = ' '.join(files)
    if os.path.exists(path):
        # 第一个参数是归档文件名称，第二个参数是指定的格式，不仅是支持zip，第三个参数是要压缩文件/文件夹的路径
        return shutil.make_archive(filename, 'tar', base_dir=path)


def unzip(file, target_dir):
    # F:/PythonWorkspace/easytf/util/util.zip
    if os.path.exists(file):
        if target_dir is not None or target_dir != '' or target_dir != ' ':
            target_dir = DEFAULT_UNZIP_DIR
        shutil.unpack_archive(file, target_dir)
