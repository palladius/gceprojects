GCE Projects
============

Trying to create a common pattern for my GCE projects, lets see what I come out 
with.


The idea is to be able to autoprivision these packages based on PUBLIC sources 
in this project and PRIVATE sources in my Google Storage.
And all could be glued with some cool python/ruby code.

Every project has to have a project.yml that my help a possible 'capistrano'-ish
to deploy everything automagically, possibly on Google Compute Engine.

Features
--------

Supports Google Compute Engine and Google Storage, atm.

* YML configuration
* GCE create/configure machines from YML
* auto init script

Usage
-----

  bin/provision.py dns.palladius.eu # provisions my personal DNS

TODO
----

* GCE Firewall configuration from YML 

Thanks
======

My mum, as usual, who made me who I am :)

* https://developers.google.com/compute/