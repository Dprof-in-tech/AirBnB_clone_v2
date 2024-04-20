#!/usr/bin/python3
"""Fabric script that defines a function 'deploy'"""
from fabric.api import *
from datetime import datetime
from os import path
import re

env.hosts = ['52.87.219.245', '18.208.120.8']
env.user = 'ubuntu'


def do_pack():
    """Fab script to compress directory

    Return: path to created archive
    """
    # Get current time
    dt = datetime.isoformat(datetime.now())
    dt = re.split("[-T:.]", dt)
    archive_name = "./versions/web_static_" + dt[0] + dt[1] + dt[2]
    archive_name += dt[3] + dt[4] + dt[5] + '.tgz'

    # Create directory versions and compress web_static dir
    local('mkdir -p versions')
    result = local("tar -cvzf {} web_static".format(archive_name))

    # Check if archiving failed
    if (result.failed):
        return None

    return (archive_name)


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


def deploy():
    """Creates and distributes an archive to your my server"""
    archive_path = do_pack()
    if not path.exists(archive_path):
        return False

    ret = do_deploy(archive_path)
    return (ret)
