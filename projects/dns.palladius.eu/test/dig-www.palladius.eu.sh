#!/bin/sh

# {{header}}
# {{foo}}
# description: {{description}}

# this test must not fail:


#dig www.palladius.eu @{{hostname}}

function assert_equal() {
  RESULT="$1"
  PROG="$2"
  if "$PROG" | grep "$RESULT" ; then # perfectible!
    echo "OK   '$2' from: $1"
  else
    echo "FAIL '$2' <> `$1`"
    exit 42
  fi
}

assert '42.42.42.42'    'dig test.palladius.eu @{{hostname}}'
assert '192.168.108.42' 'dig test.hetzner.palladius.eu @{{hostname}}'

exit 0