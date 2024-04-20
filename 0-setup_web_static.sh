#!/usr/bin/env bash
# Script that sets up your web servers for the deployment of 'web_static'

# Check if 'nginx' is installed. If not, install
res=$(eval dpkg -s nginx | grep "Status: install ok installed")
if [ "$res" != "Status: install ok installed" ]
then
	sudo apt-get -y update;
	sudo apt-get install -y nginx;
	sudo service nginx start;
fi

mkdir -p /data/web_static/releases/test;
mkdir -p /data/web_static/shared;
echo "Testing Nginx configuration" >> /data/web_static/releases/test/index.html;
link0="/data/web_static/current"
# Remove symlink $link0 if it exists
if [ -h $link0 ]
then
	rm -rf $link0
fi

# Create symlink
ln -s /data/web_static/releases/test $link0;

# Change ownership of /data/ recursively
sudo chown -R ubuntu:ubuntu /data;

# 'Server' main context to configure server
echo "server {
	listen 80;
	listen [::]:80;

	root /data/web_static/releases/test;
	index index.html;

	location /hbnb_static {
	    alias /data/web_static/current;
    }
}" > /etc/nginx/sites-available/default

# Restart nginx to reconfigure server
service nginx restart;
