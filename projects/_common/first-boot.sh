###############################################################################
# this is common to all machines
#
# TODO: run before the other
#
# IS THIS USED AT ALL? I DONT THINK SO
###############################################################################

#set -e
# get project from metadata :)
touch gce-openproject-common-begin.touch
apt-get update
apt-get install -y apache2

# yml file for conf
(
echo '### This comes from common boot script'
echo project: PROJECT_TODO 
) >> /var/www/gce-data.yml

touch gce-openproject-common-end.touch
