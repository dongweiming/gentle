#coding=utf-8
from __future__ import absolute_import


from fabric.api import local, run, sudo, task
from fabric.contrib.console import confirm
from fabric.state import env
from fabric.context_managers import cd, lcd, hide, settings
from fabric.colors import red, green, yellow

from .utils import repl_root
from .project import rsync_project


@task(alias='p', default=True)
def publish():
    '''Publish your app'''
    rsync()
    restart()


@task(alias='rs')
def rsync():
    '''Rsync your local dir to remote'''
    rsync_project(env.rsync['rpath'], repl_root(env.rsync['lpath']),
                  sshpass=True)


@task(alias='rt')
def restart():
    '''Restart your services'''
    for service, need_ops in env.services.iteritems():
        print(yellow(service) + ": " + green("start..."))
        try:
            rsync_project(need_ops['rpath'], need_ops['lpath'], sshpass=True)
            if need_ops['sudo']:
                sudo(need_ops['command'], pty=False,
                     user=need_ops['user'] if need_ops['user'] else env.user)
            else:
                run(need_ops['command'])
        except:
            print(red(service + ": fail..."))
            continue
        print(yellow(service) + ": " + green("end..."))
