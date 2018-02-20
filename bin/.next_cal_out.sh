source ~/.CAL_LINE
NUM_LINE=`khal list --format "{title}" | wc -l`
khal list --format "{title} {start-time}" | sed -n ''"$CAL_LINE"'p'
((CAL_LINE=CAL_LINE%NUM_LINE))
((CAL_LINE++))
#echo $CAL_LINE $NUM_LINE
echo "CAL_LINE=$CAL_LINE" > ~/.CAL_LINE



