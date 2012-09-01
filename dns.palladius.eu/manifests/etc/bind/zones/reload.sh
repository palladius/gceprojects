
ZONE=${1:-palladius.eu}
bianco Reloading zone $ZONE
if  ps aux|grep tail|grep /var/log >/dev/null ; then
	rosso "Already grepping logs..."
else
	green "Greeping logs:  tail -f /var/log/syslog"
	tail -f /var/log/syslog &
fi
#for ZONE in $1 ; do
	#sudo dnstouch $ZONE
	echodo sudo rndc reload $ZONE
#done
rm *.eu~ 2>/dev/null
rosso 'done (killall tail to remove this verbose stuff!)'
