
# this test must not fail:

#dig www.palladius.eu @__HOSTNAME__

assert '42.42.42.42' 'dig test.palladius.eu @__HOSTNAME__'
assert '192.168.108.42' 'dig test.hetzner.palladius.eu @__HOSTNAME__'