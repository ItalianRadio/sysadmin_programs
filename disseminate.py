import subprocess # For reading values from shell script
import sys # For reading arguments

# Set default
default = "./load-monitor/*"

# Input $working_hosts into array
lines = [line.rstrip('\n') for line in open('working_hosts.txt')]

# See if there are args, the script name is an arg. If not, insert default
command = sys.argv[1] if sys.argv[1] != "" else default

# Set default of blank for host location
location = ""

# If the first arg is an int, will take in that many hosts manually
# Ex: ./disseminate.sh 2 $host1 $host2 $command
try:
	# Parse the input to see which form we need to take
	input = command.split(" ")
	
	# -l flag will check to see if we should append a location
	if input[0] == "-l":
		input.pop(0)
		location = input.pop(0)
		command = ' '.join(input)
	
	# This line will throw a 'ValueError' if the first arg is not an int
	host_num = int(input.pop(0)) # If it's not an int we run the command everywhere
	hosts = input[0:host_num]	
	command = ' '.join(input[host_num:])
	
	if len(hosts) != host_num:
		raise SyntaxError('There were ' + str(len(hosts)) + ' arguments when there should have been ' + str(host_num))
	
	start = 'echo Starting dissemination of ' + command + ' to ' + str(host_num) + ' host(s)...'
	subprocess.call(start, shell=True)
	
	# Created for checking against $working_hosts
	found = False 
	for count in range(0, host_num):
		for line in lines:
			if hosts[count] == line:
				found = True
				break
		if found:
			hostname = "wdavis@" + line + ":/home/wdavis/" + location
			e = 'echo Disseminating to ' + line + ':'
			subprocess.call(e, shell=True)
			subprocess.call(["scp", command, hostname])
		else:
			error = 'echo Invalid hostname: "' + hosts[count] + '"'
			subprocess.call(error, shell=True)
			break

# Scp all entries in ./load-monitor/ to all $working_hosts.txt
except ValueError:
	start = 'echo Starting dissemination of ' + command + '...'
	subprocess.call(start, shell=True)
	for line in lines:
		hostname = "wdavis@" + line + ":/home/wdavis/" + location
		e = 'echo Disseminating to ' + line
		subprocess.call(e, shell=True)
		subprocess.call(["scp", command, hostname])

# Make sure we catch a common error		
except SyntaxError as e:
	print("Incorrect number of arguments")
	print(e)
		
print ("Finished disseminating.")
