#!/bin/bash

# Run the script like this cat /some/script | ssh user@server


#all_user=($(ldapsearch -xZZ -LLL -h  gra-ldap-slave.computecanada.ca  -b "dc=computecanada,dc=ca" "gidNumber=6007165"  | grep memberUid  | awk '{print $2}'))
CCUSERLIST=($(ldapsearch -xZZ -LLL -h  $LDAP_URL  -b "dc=computecanada,dc=ca" "gidNumber=6007165"  | grep memberUid  | awk '{print $2}'))
CCUSERLIST=$(echo ${CCUSERLIST[*]} | tr " " ",")

if [ -z ${CCGROUP+x} ]; then
  CCGROUP=bourque
fi
echo ++ sshare go ++

#sshare -l -A $CCGROUP -u $CCUSERLIST

sshare -P -l -u $CCUSERLIST | grep "\-$CCGROUP\|TRESRunMins"

echo ++ sshare stop ++

echo ++ sdiag  go ++


sdiag | awk '/^Agent queue size/{print $NF}'


echo ++ sdiag stop ++

echo ++ partition-stats go ++
partition-stats -v

echo  ++ partition-stats stop ++
