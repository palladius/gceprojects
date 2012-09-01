
# TODO add firewall rule into python chain

gcutil addfirewall dns-allow --network=default --allowed="tcp:53,udp:53" --project_id=google.com:biglamp --allowed_tag_sources=dns
gcutil addfirewall dns-allow-target --allowed="tcp:53,udp:53" --project_id=google.com:biglamp --target_tags=dns
gcutil addfirewall dns-allow-all --allowed="tcp:53,udp:53" --project_id=google.com:biglamp

exit 0

# TODO2 DRY it removing the project id and taking it from python, something like this:

firewall_rules:
  name: dns-allow-all
  allowed: 
  - tcp:53
  - udp:53
  
  