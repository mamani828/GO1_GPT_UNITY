#!/bin/bash

address_available()
{
    ping -c 1 $1 > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "IP is not reachable."
        return 1 #false
    else
        echo "IP is reachable."
        return 0 #true
    fi
}

SFTP_ADDRESS="192.168.12.1"
if ! address_available $SFTP_ADDRESS; then
    echo "Tried to reach dog but it is unavailable, is the robot on?"
    exit 1
fi

DIRECTORY_TO_UPLOAD="dog_py"
sftp -r $SFTP_ADDRESS << EOF
put -r $DIRECTORY_TO_UPLOAD
bye
EOF
echo "Flashed Go1."
