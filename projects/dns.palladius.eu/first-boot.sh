#!/bin/sh

VERSION=1.3

# on Ubuntu

apt-get install -y bind9 git apache2

git clone 
# cloning the repo into /etc/bind/, found here:
# http://stackoverflow.com/questions/2411031/git-how-do-i-clone-into-a-non-empty-directory

# cloning to other dir
git clone --no-checkout git://github.com/palladius/gceproject-dns.palladius.eu.git /etc/bind/bind.tmp
# moving .git/ dir 
mv /etc/bind/bind.tmp/.git /etc/bind/
# cleanup
rmdir /etc/bind/bind.tmp/
# pulling data from repo :)
cd /etc/bind/
git reset --hard HEAD 

service bind9 reload
# should have bind up and running

# cron, taken from github (brittle as it can move!)
curl https://raw.github.com/palladius/gceprojects/master/projects/dns.palladius.eu/files/etc/cron.d/pull-dns-and-reload-if-good > /etc/cron.d/pull-dns-and-reload-if-good

(
echo status: still have to add cron file
echo bind-palladius-conf-version: `cat /etc/bind/VERSION` 
echo boot-script-version: $VERSION
) >> /var/www/gce-data.yml

