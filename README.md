fwm.py expects a configuration file

The configuation file must be in the same directory as fwm.py and be named fwm.conf

The configuration file has a couple different sections. The first section specifies aliases for network firewall devices
shorter aliases are better. For example:
# First section - specify your aliases for firewall or network device IP addresses
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

