#!/usr/bin/python3
"""Fabric script (based on '3-deploy_web_static.py') that deletes
out-of-date archives, using the function 'do_clean'
"""
from os import listdir
from fabric.api import cd, lcd, env, run, local

env.hosts = ['52.87.219.245', '18.208.120.8']
env.user = 'ubuntu'


def do_clean(number=0):
    """Defines the clean-up process on the web servers

    Args:
        number (int) - the number of the archives, including the most recent,
                       to keep.
    """
    if (int(number) <= 1):
        number = 1
    else:
        number = int(number)

    # Retrieve and sort files in the 'versions' directory
    local_files = sorted(listdir('versions'))

    # Make sure 'versions' directory if not empty
    if len(local_files) == 0:
        return
    with lcd('versions'):
        [local_files.pop() for i in range(number)]
        [local('rm -rf ./{}'.format(tmp)) for tmp in local_files]

    with cd('/data/web_static/releases'):
        remote_files = run('ls -t ./').split()
        remote_files = [f for f in remote_files if 'web_static' in f]
        [remote_files.pop(0) for i in range(number)]
        [run('sudo rm -rf ./{}'.format(tmp)) for tmp in remote_files]
