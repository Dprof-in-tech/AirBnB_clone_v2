#!/usr/bin/python3
"""Fabric script that generates a '.tgz' archive from the contents of the
'web_static' folder of the AirBnB Clone repo
"""
from fabric.api import *
from os import path
import re

env.hosts = ['52.87.219.245', '18.208.120.8']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """Deploys an archive to my web server

    Return:
        False if the file at @archive_path doesn't exist, or True on success
    """

    try:
        # Check if @archive_path exists
        if not path.exists(archive_path):
            return False

        # Transfer the archive from local to remote
        put(archive_path, '/tmp/')

        # Get the name of the file
        file = re.split("/", archive_path)[-1]
        tmp_path = ('/tmp/' + file)

        # Get filename without the extension
        # filename = re.split(".", file)[0]
        filename = file[:-4]

        # Uncompress the archive to the remote folder

        dest = "/data/web_static/releases/" + filename
        aa = run('ls /')
        print(type(aa))
        run('sudo mkdir -p {}'.format(dest))
        run('sudo tar -xzf {} -C {}'.format(tmp_path, dest))

        # Move extracted files in .../web_static to correct dir
        run('sudo mv {}/web_static/* {}/'.format(dest, dest))

        # Delete the archive from the web server
        run('sudo rm -rf {}'.format(tmp_path))

        # Delete symbolic link and recreate a new one linked to the
        # new version of code
        run('sudo rm -rf /data/web_static/current')
        new_symlink = '/data/web_static/releases/' + filename
        run('sudo ln -s {} /data/web_static/current'.format(new_symlink))
    except Exception as e:
        return False

    return True
