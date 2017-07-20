Overview

Description: These scripts are usable to check ethernet errors via SNMP, both are usable in Nagios monitoring.
This scripts create files in /tmp to store last checked values, to have a value to compare in each runing time.

Requirements:
Python2.7
Python easysnmp

Usage:
Usage: check_if_in_errors.py -h [host] -c [community] -i [interface]
Usage: check_if_out_errors.py -h [host] -c [community] -i [interface]

Responses:
OK - Interface <name> is not increasing errors
Critical - Interface <name> is increasing errors
Unknown - Interface not found
