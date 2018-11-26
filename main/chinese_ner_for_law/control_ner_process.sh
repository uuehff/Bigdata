#!/bin/bash
# by Paul Colby (http://colby.id.au), no rights reserved ;)

PREV_TOTAL=0
PREV_IDLE=0
NUM=700
while true; do
 CPU=(`cat /proc/stat | grep '^cpu '`) # Get the total CPU statistics.

#echo "${CPU[0]}";
# echo "${CPU[1]}";
# echo "${CPU[2]}";
# echo "${CPU[3]}";
# echo "${CPU[4]}";

 unset CPU[0] # Discard the "cpu" prefix.
 IDLE=${CPU[4]} # Get the idle CPU time.
  
 # Calculate the total CPU time.
 TOTAL=0
 for VALUE in "${CPU[@]}"; do
  let "TOTAL=$TOTAL+$VALUE"
 done

# echo $TOTAL;

 # Calculate the CPU usage since we last checked.
 let "DIFF_IDLE=$IDLE-$PREV_IDLE"
 let "DIFF_TOTAL=$TOTAL-$PREV_TOTAL"
 #获取不带小数的百分比
 #let "DIFF_USAGE=(1000*($DIFF_TOTAL-$DIFF_IDLE)/$DIFF_TOTAL+5)/10"
 #echo -en "\rCPU: $DIFF_USAGE% \b\b"

 #获取带小数的百分比
 let "DIFF_USAGE=1000*($DIFF_TOTAL-$DIFF_IDLE)/$DIFF_TOTAL"
 let "DIFF_USAGE_UNITS=$DIFF_USAGE/10"
 let "DIFF_USAGE_DECIMAL=$DIFF_USAGE"
 echo -en "\rCPU: $DIFF_USAGE_UNITS.$DIFF_USAGE_DECIMAL% \b\b\b\b"
 sleep 2
 echo -e "\n================="
 if [ "$DIFF_USAGE_UNITS" -lt 40 ]
 then
 	NUM=$(( $NUM + 1 ))
 	sed -i "s/select uuid,doc_content from judgment where id > `expr $NUM \* 1000` and id <= `expr $(( $NUM + 1 )) \* 1000` /select uuid,doc_content from judgment \
where id > `expr $(( $NUM + 1 )) \* 1000` and id <= `expr $(( $NUM + 2 )) \* 1000` /g" "readMysql_sparksql.py"
 	python readMysql_sparksql.py
 fi
 # Remember the total and idle CPU times for the next check.
 PREV_TOTAL="$TOTAL"
 PREV_IDLE="$IDLE"

 # Wait before checking again.
done

