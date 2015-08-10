fwm.py expects a configuration file

The configuation file must be in the same directory as fwm.py and be named fwm.conf

The configuration file has a couple different sections. The first section specifies aliases for network firewall devices
shorter aliases are better. For example:
First section - specify your aliases for firewall or network device IP addresses
DEV1 1.2.3.4
DEV2 2.3.4.5

The next section optionally specifies groups of devices for the purposes of pushing updates out to a pre-selected group. These groups are specified by using the fwgrp keyword followed by a group alias and then the device aliases separated by commas. See below,

fwgrp DEVGRP DEV1,DEV2

Lastly the command section lets you preconfigure commands to be issued to devices and give the commands aliases.
This takes the form of 
alias "aliasname" command <"command syntax">
alias status command <get system status>

a command can also be a series of strings separated by commas,
For example
alias status command <config global-mode,get system-status>

To use fwm.py
simply place it in a directory you want to use for it setup your fwm.conf file specifying your firewalls and their IP's and run ./fwm.py --init for fwm.py to create a subdirectory tree to use.

Now you can use ./fwm.py --push to push updates to your firewalls. This works by creating a config to enter as a series of lines in a .txt file. This txt file must be prefixed with the alias in the fwm.conf file corresponding to the IP of the device the .txt file is destined for. The prefix can also be a fwgrp alias or it can be "all" to indicate that the update should be applied to all devices specified in the fwm.conf file.

sample fwm.conf file:

DEV1 1.2.3.4
DEV2 2.3.4.5
DEV3 3.4.5.6

fwgrp DEVPAIR DEV1,DEV2

alias status command <config mode global,show status>


Now to apply an update to say the firewalls DEV1 and DEV2 you would create txt file in the ./updates folder and name it as follows: DEVPAIR_addnewpolicy.txt

This txt file would then contain the lines necessary to perform the update.
So depending on your firewall vendor the syntax will vary to add a new policy but it could say something like:

config mode global
edit policy
add policy 4
set src "1.2.3.4"
set dst "5.5.5.5"
set svc "TCP/80"
set action allow
set comment "sample"
end

