#!/bin/bash
x=0
n=0
while [ $x==0 ]
do
    n=$(( n+1 ))
    if ps -ef | grep -v grep | grep details_gst.py;
    then break
    else 
        echo $n
        if [ $n -eq 5 ];
        then 
            python3 "/DriveE/GST/Codes/details_gst.py"
            break
        fi  
    fi
done
