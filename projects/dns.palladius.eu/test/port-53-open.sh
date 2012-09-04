#!/bin/sh

# testing TCP/53
nc -z {{ip}} 53

# TODO udp 53
nc -zu {{ip}} 53
