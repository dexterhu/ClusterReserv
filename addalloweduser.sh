#!/bin/bash
# configure sshd on a cluster node to allow specific users
# args are a list of users ( the root is always in the allowed list)
# this should be run by root 

allowedusers="AllowUsers root"
for i in $*
do 
allowedusers="$allowedusers $i"
done

echo $allowedusers

# grep sshd_config file to remove a line that starts AllowUsers
existing=$(grep AllowUsers < /etc/ssh/sshd_config | wc -l)

if [ "$existing" -gt "0" ]; then
        echo "replace existing allowed users"
	sed -i "s/^.*AllowUsers.*\$/$allowedusers/" /etc/ssh/sshd_config 1>/dev/null 2>&1
else
	echo "add new allowed users"
     	echo $allowedusers >> /etc/ssh/sshd_config
fi

service ssh restart

