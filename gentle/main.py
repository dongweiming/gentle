"""This is gentle command line

Usage:
  gt [(--show=<type> | --hide=<type>) [--only]] COMMAND...
  gt (-l | --list)
  gt --version
  gt init

Arguments:
  <type>               message output type
                       [chioces: 'status', 'aborts', 'warnings', 'running',
                       'stdout', 'stderr', 'debug', 'user']
                       [aliases:
                           'everything':
                               ['warnings', 'running', 'user', 'output'],
                           'output': ['stdout', 'stderr'],
                           'commands': ['stdout', 'running']

  COMMAND              gentle command

Options:
  -h --help            show this help message and exit
  --version            show version and exit
  -l --list            show available commands
  --hide=<type>        setting hide output type
  --show=<type>        setting show output type
  --only               If use, only hide/show this one type
  init                 initialize the current directory

"""
from __future__ import absolute_import

import os
import sys

__version__ = '0.1'
choices = {'status': 1,
           'aborts': 2,
           'warnings': 3,
           'running': 4,
           'stdout': 5,
           'stderr': 6,
           'debug': 7,
           'user': 8}
aliases = {'everything': ['warnings', 'running', 'user', 'output'],
           'output': ['stdout', 'stderr'],
           'commands': ['stdout', 'running']}

here = os.path.abspath(os.path.dirname(__file__))

from docopt import docopt
from fabric import state
from fabric.tasks import execute
from fabric.task_utils import crawl
from fabric.colors import red, green
from fabric.utils import warn, indent
from fabric.main import (load_fabfile, parse_arguments, show_commands,
                         disconnect_all)


def set_output(output_type, hide, only):
    '''Set state.output bool value'''
    output_list = output_type.split(',')
    # set output default all not match
    for k in choices.keys():
        state.output[k] = hide
    # when use mutli type, only set this match
    if len(output_list) > 1:
        for o in output_list:
            if o in choices:
                state.output[o] = not hide
            else:
                # when has unkown type
                print(red(o + ' is a Unknown type, Ignore it!'))
    else:
        # when only has the type
        t = output_list[0]
        # when in aliases
        if t in aliases:
            for a in aliases[t]:
                state.output[a] = not hide
        # when in choices
        elif t in choices:
            # when force only one type to match
            if only:
                state.output[t] = not hide
            else:
                num = choices[t]
                for type, type_num in choices.iteritems():
                    if type_num <= num:
                        state.output[type] = not hide
        else:
            print(red(t + ' is a Unknown type, Ignore it!'))


def init():
    '''Initialize the current directory'''
    template = '''host: localhost:22
password: 123456
gateway:
gatewaypassword:
rsync:
  lpath: $ROOT
  rpath: /root
services:
  nginx:
    command: /etc/init.d/nginx restart
    lpath: $ROOT/nginx.conf
    priority: 3
    rpath: /etc/nginx/nginx.conf
    sudo: true
    user: root
  supervisor:
    command: supervisorctl -c /etc/supervisor/supervisord.conf restart all
    lpath: $ROOT/supervisord.conf
    priority: 2
    rpath: /etc/supervisor/supervisord.conf
    sudo: true
    user: root
username: root
'''
    with open(os.path.join(os.getcwd(), '.gentle.yaml'), 'w') as f:
        f.write(template)
    print(green('Initialize Success'))
    sys.exit(0)


def gentleman():
    args_dict = docopt(__doc__, version=__version__)
    arguments = args_dict['COMMAND']
    if not os.path.exists(os.path.join(os.getcwd(), '.gentle.yaml')):
        if arguments != ['init']:
            print(red('This is not a gentle directory, Make sure this is the correct'  # noqa
                  'directory, and use `gt init` Initialization'))
            return sys.exit(1)
        else:
            init()
    arguments = args_dict['COMMAND']
    try:
        # state.env.update(load_settings(state.env.rcfile))
        fabfile = os.path.join(here, 'gt')
        state.env.real_fabfile = fabfile
        default = None
        if fabfile:
            docstring, callables, default = load_fabfile(fabfile)
            state.commands.update(callables)

        commands_to_run = parse_arguments(arguments)
        unknown_commands = []
        for tup in commands_to_run:
            if crawl(tup[0], state.commands) is None:
                unknown_commands.append(tup[0])

        if args_dict['--list']:
            show_commands(docstring, 'normal', 1)
        for type in ['show', 'hide']:
            t = args_dict['--' + type]
            if t is not None:
                hide = True if type == 'hide' else False
                set_output(t, hide=hide, only=args_dict['--only'])

        # Abort if any unknown commands were specified
        if unknown_commands:
            warn("Command(s) not found:\n%s" % indent(unknown_commands))
            show_commands(None, 'normal', 1)

        for name, args, kwargs, arg_hosts, arg_roles, arg_exclude_hosts in \
            commands_to_run:
            execute(
                name,
                hosts=arg_hosts,
                roles=arg_roles,
                exclude_hosts=arg_exclude_hosts,
                *args, **kwargs)

        if state.output.status:
            print("\nDone.")
    except SystemExit:
        raise
    except KeyboardInterrupt:
        if state.output.status:
            sys.stderr.write("\nStopped.\n")
        sys.exit(1)
    except:
        sys.excepthook(*sys.exc_info())
        sys.exit(1)
    finally:
        disconnect_all()
    sys.exit(0)

if __name__ == "__main__":
    gentleman()
