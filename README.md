# ssh_remote

Connects to remote hosts through SSH, executes commands/scripts and then saves the output to logfiles.

Paramiko is used to open the SSH session

Hosts, logins and comands to be executed are parsed from json files and populated to dicts.

Logfiles are saved in the following format: YYYY-MM-DD_[hostname].txt
