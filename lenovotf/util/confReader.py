import configparser
import re
import os
import sys

CONF_PATH = os.path.dirname(os.path.abspath(__file__)) + "/../conf/app.conf"


def _getparser():
    parser = configparser.ConfigParser()
    parser.read(CONF_PATH)
    return parser


def get_web_server_url():
    return _getparser().get("web", "server_url")


def get_rpc_server_url():
    return _getparser().get("rpc", "server_url")


def get_pre_installed_depends():
    return re.split(",", _getparser().get("installed", "pre"))


def get(section, key):
    return _getparser().get(section, key)


if __name__ == '__main__':
    pass
