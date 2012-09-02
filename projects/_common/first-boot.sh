###############################################################################
# this is common to all machines
#
# TODO: run before the other
###############################################################################

apt-get update
apt-get install apache2
touch gce-openproject.touch

# yml file for conf
(
echo '### This comes from common boot script'
echo project: PROJECT_TODO 
) >> /var/www/gce-data.yml
