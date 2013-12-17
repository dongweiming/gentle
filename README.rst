=================================
 gentle - Help you quickly deploy code to the test environment
=================================

:Version: 0.1
:Download: http://pypi.python.org/pypi/gentle
:Source: http://github.com/dongweiming/gentle
:Keywords: fabric, docopt, yaml, devops, python


--

What is a Gentle?
======

As a programmer, I thought There may be a step to deployed to the test
environment:

- Copy of your code to the test server, enter the username and password.
- Restart your test environment, such as nginx, superviosr.
- Local to see results, repeat 1-2

It is a waste of time...

Gentle can help you automated do that. The development process is:

- Switch to the directory you want to develop
- Initialization gentle:

  - configure the directory you want to sync (use rsync)
  - set the test environment server ip, port, username and password
  - configure every time you want to update the code in the service restart

- You only need coding and following this command::

    $gt publish

  If You are more lazyer, you can use::

    $gt p

That's all

Install
=====
    First You must install `sshpass`, IN fabric rsync_project need input
    password again. I use sshpass automation of this process

    In ubuntu direct use apt-get/aptitude::

      $sudo apt-get install sshpass

    Other platform, Go ``http://sourceforge.net/projects/sshpass`` donwload
    the lastest verison, then type the following command::

      $tar zxvf sshpass-1.05.tar.gz && cd sshpass-1.05
      $./configure && make && sudo make install

    Then install `gentle`, You only use::

      $sudo pip install gentle

    or::

      $git clone https://github.com/dongweiming/gentle
      $cd gentle
      $sudo python setup.py install

Get Started
=========

- **gt**

    After you install, you can use `gt` , Similar `fab` but very different.

- **init**

    When you start to use gentle for the current directory. You first init it::

      $cd /Your/app/directory
      $gt init

    It can add a file with name *.gentle.yaml' to this directory.

- **show**

   when complete initialization, you can show settings for default::

     $cat .gentle.yaml
     host: localhost:22
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

Parameter Description
~~~~~~~~~~~

:host:
  environment server, can use `user@host:port`, or `host`, or `host:port`,
  or hosts list: [`user@host1:port`, `user@host2:port`...]

:password:
  account's password.

:gateway:
  Gateway server(Jump server) use `user@host:port`, or `host`, or `host:port`

:gatewaypassword:
  Gateway server's password

:rsync:
  which dir that you want to sync.

:services:
  which services that you want to restart.

:username:
  which account to use.

:lpath:
  local path, you can use *$ROOT$* for current directory.

:rpath:
  remote path.

:command:
  How to restart service's command.

:priority:
  It for restart's order, it's bigger, and restart earlier.

:sudo:
  A bool for tell gentle use sudo or not.

:user:
  When use sudo which account to use. default it's username's value.

- **list help**

   You can use::

   $gt -h

- **list commands**

   You can type the following command to show available commands::

   $gt -l

- **output type**

   Gnetle is use fabric default output type. you can find available type which::

   $gt -h

   You can assign it::

   $gt --show=debug,user rs # Only show debug,user type
   $gt --hide=warning rs #Hide status,aborts,warnings three types
   $gt --show debug rs --only #Only show debug type

Command Description
~~~~~~~~~~~

:rsync/rs:
  Rsync your local dir to remote.

:restart/rt:
  Restart your services.

:pubish/p:
  Publish your app, It equal *rsync* + *restart*.

:showconf/show:
  Show gentle settings.

:setconf/set:
  Set gentle conf. You can directly edit. Gentle.yaml file, you can also choose this command::

    - gt set:key=services.nginx.rpath,value=/root
    - gt s:key=host,value=8.8.8.8:12345
    - gt s:key=rsync.rpath,value=/root

    dot is the separator.

Enjoy it
=======
