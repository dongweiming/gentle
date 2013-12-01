#coding=utf-8
from __future__ import absolute_import
import os
import shutil
from fabric.state import env
from fabric.api import task
from .handler import YamlHandler
from .operations import publish, rsync, restart

__all__ = ['publish', 'p', 'rsync', 'rs', 'restart', 'rt', 'setconf', 'show',
           'showconf']

h = YamlHandler()
h.set_env(env)


@task(alias='set')
def setconf(key, value):
    '''Set gentle conf'''
    key = key.split('.')
    h.set_conf(value, key)


@task(alias='show')
def showconf():
    '''Show gentle settings'''
    h.show()
