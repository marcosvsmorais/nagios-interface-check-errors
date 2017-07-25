#!/usr/bin/python

# -*- conding: utf-8 -*-

import sys
from easysnmp import snmp_get, snmp_set, snmp_walk

def check_if_in_errors(host,community,interface):
	
	system_items = snmp_walk('IF-MIB::ifName', hostname=host, community=community, version=2)

	found = False

	for item in system_items:
		if item.value == interface:
			oid=item.oid
			value=item.value
			oid_index=item.oid_index
			found = True

	if found:
		if_in_errors = snmp_get('IF-MIB::ifInErrors.'+oid_index, hostname=host, community=community, version=2)
		if_out_errors = snmp_get('IF-MIB::ifOutErrors.'+oid_index, hostname=host, community=community, version=2)
		file_name_in = "{}.{}.in_errors.txt".format(host,value)
		file_name_out = "{}.{}.out_errors.txt".format(host,value)

		try:
			# OPEN FILE
			fo = open("/tmp/"+file_name_in, "r+")
			fo2 = open("/tmp/"+file_name_out, "r+")
			# READ LAST VALUES
			last_value_in = long(fo.read())
			last_value_out = long(fo2.read())
			# PIC THE ACTUAL VALUE
			actual_value_in = long(if_in_errors.value)
			actual_value_out = long(if_out_errors.value)
			# COMPARE THE VALUES
			if actual_value_in > last_value_in or actual_value_out > last_value_out:
				# TRUNCATE FILE CONTENT AND WRITE NEW CONTENT
				fo.seek(0)
				fo.truncate()
				fo.write(str(actual_value_in))
				fo2.seek(0)
				fo2.truncate()
				fo2.write(str(actual_value_out))
				fo.close()
				fo2.close()
				# PRINT MESSAGE AND EXIT
				print "Critical - Interface {} is increasing errors".format(interface)
				sys.exit(2)
			else:
				# TRUNCATE FILE CONTENT AND WRITE NEW CONTENT
				fo.seek(0)
				fo.truncate()
				fo.write(str(actual_value_in))
				fo2.seek(0)
				fo2.truncate()
				fo2.write(str(actual_value_out))
				fo.close()
				fo2.close()
				# PRINT MESSAGE AND EXIT
				print "OK - Interface {} is not increasing errors".format(interface)
				sys.exit(0)
			

		except IOError:
			# CREATE FILE AND WRITE THE FIRST VALUE
			fo = open("/tmp/"+file_name_in, "w+")
			fo2 = open("/tmp/"+file_name_out, "w+")
			fo.write(if_in_errors.value)
			fo2.write(if_out_errors.value)
			# CLOSE FILE
			fo.close()
			fo2.close()
			# RETURN OK - FILE CREATED
			print "OK - Interface {} is not increasing errors".format(interface)
			sys.exit(0)
	else:
		print "Unknown - Interface not found"
		sys.exit(3)

def main():

	message_error = "Usage: check_if_in_errors.py -h [host] -c [community] -i [interface]"
	integer_error = "\n-h [host]: an integer is required"

	try:
		if sys.argv[1] == "-h":
			host = sys.argv[2]
		else:
			print message_error

		if sys.argv[3] == "-c":
			community = sys.argv[4]
		else:
			print message_error

		if sys.argv[5] == "-i":
			interface = sys.argv[6]
		else:
			print message_error

		if host != "" and community != "" and interface != "":
			check_if_in_errors(host,community,interface)

	except IndexError:
		print message_error

if __name__ == '__main__':
	main()