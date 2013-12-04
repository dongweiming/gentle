#coding=utf-8
import os
import sys
from collections import OrderedDict
import yaml
from yaml.error import YAMLError, MarkedYAMLError
from fabric.colors import green, red
from fabric.utils import indent


class YamlHandler(object):

    def __init__(self):
        with open(os.path.join(os.getcwd(), '.gentle.yaml')) as f:
            try:
                self.yaml_data = yaml.load(f)
            except (YAMLError, MarkedYAMLError) as e:
                print('Your .gentle.yaml has error: \n' + str(e))
                sys.exit(1)

    def set_env(self, env):
        env.host_string = self.yaml_data['host']
        env.user = self.yaml_data['username']
        env.password = self.yaml_data['password']
        env.gateway = self.yaml_data['gateway']
        if env.gateway:
            env.passwords[env.gateway] = self.yaml_data['gatewaypassword']
        services = OrderedDict(sorted(
            self.yaml_data['services'].items(),
            key=lambda t: int(t[1]['priority'])))
        new_dict = dict(rsync=self.yaml_data['rsync'], services=services)
        env.update(new_dict)

    def set_conf(self, value, args):
        try:
            flag = False
            key = args[0]
            if key in ['username', 'host', 'password', 'gateway',
                       'gatewaypassword']:
                self.yaml_data[key] = value
                print(green('Set [{0}] to [{1}] Success'.format(key, value)))
                flag = True
            elif key == 'rsync':
                sub_type = args[1]
                if sub_type in ['lpath', 'rpath']:
                    self.yaml_data['rsync'][sub_type] = value
                    print(green('Set [{0}:{1}] to [{2}] Success'.format(
                        key, sub_type, value)))
                    flag = True
            elif key == 'services':
                sub_services, sub_type = args[1], args[2]
                if sub_services in self.yaml_data['services'] and \
                   sub_type in ['lpath', 'rpath', 'command', 'priority',
                                'sudo', 'user']:
                    self.yaml_data['services'][sub_services][sub_type] = value
                    print(green('Set [{0}:{1}:{2}] to [{3}] Success'.format(
                        key, sub_services, sub_type, value)))
                    flag = True
            if not flag:
                print(red('Not has key: ' + '.'.join(args)))
                sys.exit(1)
        except IndexError:
            print(red('You set conf error! Please check'))

        with open(os.path.join(os.getcwd(), '.gentle.yaml'), 'w') as f:
            f.write(yaml.dump(self.yaml_data, default_flow_style=False))

    def show(self):
        '''Show gentle settings'''
        with open(os.path.join(os.getcwd(), '.gentle.yaml')) as f:
            print(indent(f.read(), spaces=2))
