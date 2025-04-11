#!/bin/bash

#inportação dos scripts

cd /home/lloyd101/driveZone/pythontest
source ./main-functions.sh

echo "---- Script started at $(date) ----" >> /home/lloyd101/drivezone.txt

process(){
    adb wait-for-device

    echo "Let's start!"
    unlocking_device 
    sleep 3

    open_Game
    sleep 30
    
    echo "Begin 1st act!"
    first_ACT
	echo "End of Act"
    tap_back
    sleep 5

    echo "Begin 2nd act!"
    second_ACT
    sleep 4
	echo "End of act"
    echo "Time to close"
    closing
    echo "The end!"          
}

process
