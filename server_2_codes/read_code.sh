#!/bin/bash
x=0
n=0
while [ $x==0 ]
do
    n=$(( n+1 ))
    if ps -ef | grep -v grep | grep read_code.py;
    then break
    else 
        echo $n
        if [ $n -eq 5 ];
        then 
            python3 "/DriveD/GST/Codes/read_code.py"
            break
        fi  
    fi
done
