#!/bin/bash
x=0
n=0
while [ $x==0 ]
do
    n=$(( n+1 ))
    if ps -ef | grep -v grep | grep gst_main_read.py;
    then break
    else 
        echo $n
        if [ $n -eq 5 ];
        then 
            python3 "/DriveF/gst_main_read.py"
            break
        fi  
    fi
done
