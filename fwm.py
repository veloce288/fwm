/usr/bin/python

"""
Version: 0.2
Author: Aaron Maskens
Creation Date: 8/9/2015
Latest Revision Date:
Latest Revision:
"""

"""
ideas:
init - will take the config file and create directories for each firewall
     ./configs/fw1/alias1/
     ./configs/fw1/alias2/
     ./configs/fw2/alias1/
     ./configs/fw2/alias2/
     ./updates/*.txt
     ./updates/fw1/
     ./updates/fw2/
     
push - will apply any txt files as updates to any txt file present in ./updates/.
     - update is pushed to the fw or fwgrp denoted in the prefix of the txt file

pull - options are pull target alias
	 - pull target alias goes into timestamped file ./configs/fw1/alias1-timestamp1.txt
	 - options to do diff between alias and last time stamp? 
	 - output options
	 
Specify default config and have the option of specifying other ones?


"""
print "\nFirewall Manager, fwm.py, Version 0.2, author: Aaron Maskens\n"
# imported Libraries
import datetime
import getpass
import argparse
import re
import paramiko
import os

# Parse arguments passed from CLI
parser = argparse.ArgumentParser()
parser.add_argument('-u', action='store', dest='user', help='set username')
parser.add_argument('-t', action='store', dest='target_string', help='string of targets')
parser.add_argument('--init', action='store_true', help='initialize config file')
parser.add_argument('--push', action='store_true', help='push out updates to firewalls')
parser.add_argument('--pull', action='store', dest='alias', help='pulls output of specified command or set')
parser.add_argument('--stdout', action='store_true', help='output to stdout instead of to file')

# Declare global scope variables
cfgs = "configs"
upds = "updates"
results = parser.parse_args()
user = results.user
conf = []
passwd = ""
firewall = {}
command = {}
output = []
fwgrp = {}

if not user and (results.push or results.alias):
    print "Error, must specify user by using the user flag and parameter \"-u username\""
    exit(0)
elif user:
	passwd = getpass.getpass()


def parse_script_config():
    # Parse configuration file
    with open("fwm.conf") as f:
        conf = f.read().splitlines()
    for line in conf:
        fw_ip = re.match("(\w+)\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", line)
        if fw_ip:
            firewall[fw_ip.group(1)] = fw_ip.group(2)

        fwgrp_parse = re.match(r"fwgrp\s(\w+)\s(.*?)", line)
        if fwgrp_parse:
			fwgrp_list = []
			fwgrp[fwgrp_parse.group(1)] = fwgrp_parse.group(2).split(',')
        cmd = re.match("alias\s(\w+)\scommand\s\<(.*?)\>", line)
        if cmd:
			#
            command[cmd.group(1)] = cmd.group(2).replace(',', '\n')


def get_timestamp():
	d = datetime.datetime.now()
	return d.strftime('%Y-%m-%d_%Hh%Mm%Ss')

def initialize():
	# Based on script config, create directory structure
	# 
	
	parse_script_config()
	os.mkdir(cfgs)
	os.mkdir(upds)
	for fw,ip in firewall.iteritems():
		newdir1 = cfgs + '/' + fw
		os.mkdir(newdir1)		
		for a,c in command.iteritems():
			newdir2 = newdir1 + '/' + a
                        print newdir2
			os.mkdir(newdir2)
	
if results.init:
	initialize()

def exec_ssh_conn(cmds, targets):
	output = []
        firewalls = {}
        if targets == "all":
                # Setup paramiko ssh client
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy( paramiko.AutoAddPolicy())
			for k,v in firewall.items():
				ssh.connect(v, username=user,password=passwd)
				c = '\n'.join(cmds)
				stdin, stdout, stderr = ssh.exec_command(c)
				output = stdout.readlines()
		
				ssh.close()
				for line in output:
					line = line.strip('\n')
					print line
        else:
			# Check target for individual firewalls
			for k,v in firewall.items():
				if k == targets:
					ssh = paramiko.SSHClient()
					ssh.set_missing_host_key_policy( paramiko.AutoAddPolicy())
					ssh.connect(v, username=user,password=passwd)
					c = '\n'.join(cmds)
					stdin, stdout, stderr = ssh.exec_command(c)
					output = stdout.readlines()
		
					ssh.close()
					for line in output:
						line = line.strip('\n')
						print line
    
	print "END\n"
	
def push_update():
	parse_script_config()
	# Take txt files in update folder and push them as updates to firewalls
	# Then move the txt files into a date revisioned folder
	
	# Create a list of commands from any files in the updates directory ending in .txt
	old_paths = {}
	valid_updates = {}
	update_files = []
	update_files = os.listdir(upds)
	for f in update_files:
	    prefix_check = re.search("(\w+)_.*\.txt", f)
	    if prefix_check:
			valid_updates[prefix_check.group(1)] = f
			
	for prefix, upd in valid_updates.items():
		fwgrp_check = False
		cfg_path = upds + '/' + upd
		update_commands = []
		old_paths[upd] = cfg_path
		with open(cfg_path, 'r') as f:
			for line in f:
				cfg_parse = re.search("(\S.*\S)", line)
				if cfg_parse:
					update_commands.append(cfg_parse.group(1))
		
		for k,v in fwgrp.items():
			if k == prefix:
				# fwgrp
				fwgrp_check = True
				for fw in fwgrp[prefix]:
					exec_ssh_conn(update_commands, fw)
				
		if not fwgrp_check:
			exec_ssh_conn(update_commands, prefix)
		
	for n, old_pth in old_paths.items():
		os.rename(old_pth, 'configs/' + n + '_' + user + '_' + get_timestamp())
		
	# Now have commands put into update_commands list
	# Need to connect to firewalls and run each command in list
	# Need to capture output and put into a timestamped file
	

def pull_request(target, alias):
        pass

if results.push:
	push_update()
