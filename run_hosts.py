import subprocess # For reading values from shell script
import sys # For reading arguments

# Set default
default = "./loadMonitor.sh"

# Input $working_hosts into array
lines = [line.rstrip('\n') for line in open('working_hosts.txt')]

# See if there are args, the script name is an arg. If not, insert default
command = sys.argv[1] if sys.argv[1] != "" else default

# Output must be done thru shell cmds for thread safety
start = 'echo Started run_hosts...'
subprocess.call(start, shell=True)

# If the first arg is an int, will take in that many hosts manually
# Ex: ./run_hosts.sh 2 $host1 $host2 $command
try:
	# Parse the input to see which form we need to take
	input = command.split(" ")
	
	# This line will throw a 'ValueError' if the first arg is not an int
	host_num = int(input.pop(0)) # If it's not an int we run the command everywhere
	hosts = input[0:host_num]	
	command = ' '.join(input[host_num:])
	
	# Check to see if we have the correct number of args
	if len(hosts) != host_num:
		raise SyntaxError('There were ' + str(len(hosts)) + ' arguments when there should have been ' + str(host_num))
	
	found = False # Created for checking against $working_hosts
	for count in range(0, host_num):
		for line in lines:
			if hosts[count] == line:
				found = True
				break
		if found:
			hostname = "wdavis@" + line
			e = 'echo Running "' + command + '" at ' + line
			subprocess.call(e, shell=True)
			subprocess.call(["ssh", hostname, command])
		else:
			error = 'echo Invalid hostname: "' + str(hosts[count]) + '" Could not run'
			subprocess.call(error, shell=True)

# Run in all $working_hosts
except ValueError:
	for line in lines:
		hostname = "wdavis@" + line
		e = 'echo Running ' + command + ' at ' + line
		subprocess.call(e, shell=True)
		subprocess.call(["ssh", hostname, command])

# Make sure we catch a common error		
except SyntaxError as e:
	print("Incorrect number of arguments")
	print(e)
	
print ('Finished running...')