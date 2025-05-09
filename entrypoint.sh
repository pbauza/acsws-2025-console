#!/bin/bash

# Set the CDB path
#echo "ACS_CDB=/home/almamgr/acsws-2025/ITS/test/DEPLOY" >> /alma/ACS-2025APR/ACSSW/config/.acs/.bash_profile.acs
echo "ACS_CDB=/home/almamgr/acsws-2025/ITS/test/SIM" >> /alma/ACS-2025APR/ACSSW/config/.acs/.bash_profile.acs
source /alma/ACS-2025APR/ACSSW/config/.acs/.bash_profile.acs
cd /home/almamgr/acsws-2025/ICD/src 
make clean all install
cd /home/almamgr/acsws-2025/pyConsole/src 
make clean all install

# start service in background here
echo "Starting ACS..."
acsStart

acs_running=1
acs_counter=$ACS_TIMEOUT
while [ $(acsStatus 2>/dev/null | grep -e "Manager process ID" -e "Naming service process ID" -e "Notify service process ID" -e "Logging service process ID" -e "IFR process ID" -e "Logging notify service process ID" -e "Archive notify service process ID" -e "Alarm notify service process ID" -e "ACS Log Service process ID" -e "ACS CDB process ID" -e "ACS Alarm Service process ID" | wc -l) -le 10 ]; do
    sleep 1
    let acs_counter=acs_counter-1
    echo "Waiting for ACS to start, timeout in $acs_counter seconds"
    if [ $acs_counter -eq 0 ]; then
        acs_running=0
        break
    fi
done

if [ $acs_running -eq 1 ]; then 
    sleep 20
    echo "ACS is now in a normal running state, starting ACS containers"
    acsStartContainer --py pyContainer 2>&1 | tee -a "/home/almamgr/acsws-2025/logs/pycontainer.log" &
    acsStartContainer --py pySimContainer 2>&1 | tee -a "/home/almamgr/acsws-2025/logs/pysimcontainer.log" &
    sleep 5
else
    echo "ACS seems not to be running, skipping starting of all ACS containers!"
fi

echo "Hit Ctrl+C to exit or run 'docker stop <container>'"
sleep infinity &
wait $!

echo "exited $0"
