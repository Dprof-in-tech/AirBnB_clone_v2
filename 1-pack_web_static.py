#!/usr/bin/python3
"""Fabric script that generates a '.tgz' archive from the contents of the
'web_static' folder of the AirBnB Clone repo
"""
from fabric.api import *
from datetime import datetime
import re


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
