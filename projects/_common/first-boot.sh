###############################################################################
# this is common to all machines
#
# TODO: run before the other
###############################################################################

#set -e
# get project from metadata :)
touch gce-openproject-common-begin.touch
apt-get update
apt-get install apache2

# yml file for conf
(
echo '### This comes from common boot script'
echo project: PROJECT_TODO 
) >> /var/www/gce-data.yml

touch gce-openproject-common-end.touch
